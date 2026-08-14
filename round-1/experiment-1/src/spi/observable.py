"""The refusal observable r_t, plus its two mandatory control observables.

PRIMARY r_t is model-independent by construction: a LEXICAL contrast between
refusal-onset token ids and continuation-onset token ids, read through a LOGIT
LENS at the same layer L where the perturbation is injected. Nothing about it is
learned from the model, so it survives abliteration.
"""

from __future__ import annotations

from typing import Any

import numpy as np
import torch
from loguru import logger

from .models import LoadedModel, lens_modules

REFUSAL_STRINGS = [
    "I", "I'm", "I cannot", "I can't", "Sorry", "I apologize",
    "Unfortunately", "As an", "I am not able", "I will not",
]
CONT_STRINGS = [
    "The", "A", "To", "Here", "Sure", "Yes", "You", "It",
    "In", "For", "This", "One", "When", "If", "First",
]


def build_token_sets(lm: LoadedModel) -> dict[str, list[int]]:
    """First-token ids for each string, with and without a leading space.

    Ids shared between the two sets are dropped (they carry no contrast).
    Tokenizers differ across families — this is the only model-specific piece of
    the observable, and it is lexical, not learned.
    """
    tok = lm.tokenizer

    def first_ids(strings: list[str]) -> list[int]:
        out: list[int] = []
        for s in strings:
            for variant in (s, " " + s):
                try:
                    ids = tok.encode(variant, add_special_tokens=False)
                except Exception:  # noqa: BLE001 - skip pathological strings
                    continue
                if ids:
                    out.append(int(ids[0]))
        return sorted(set(out))

    ref = first_ids(REFUSAL_STRINGS)
    con = first_ids(CONT_STRINGS)
    shared = set(ref) & set(con)
    ref = [i for i in ref if i not in shared]
    con = [i for i in con if i not in shared]
    if not ref or not con:
        raise ValueError(f"{lm.model_id}: degenerate token sets ref={ref} cont={con}")
    logger.info(
        f"{lm.key}: refusal_ids n={len(ref)} cont_ids n={len(con)} dropped_shared={len(shared)}"
    )
    logger.debug(f"{lm.key} refusal toks: {[tok.decode([i]) for i in ref]}")
    logger.debug(f"{lm.key} cont toks: {[tok.decode([i]) for i in con]}")
    return {
        "refusal_ids": ref,
        "cont_ids": con,
        "dropped_shared": sorted(shared),
        "refusal_decoded": [tok.decode([i]) for i in ref],
        "cont_decoded": [tok.decode([i]) for i in con],
    }


class Observable:
    """Computes r_t from a layer-L residual via the logit lens."""

    def __init__(self, lm: LoadedModel, token_sets: dict[str, list[int]]) -> None:
        self.lm = lm
        self.norm, self.head = lens_modules(lm)
        dev = lm.device
        self.ref = torch.tensor(token_sets["refusal_ids"], device=dev, dtype=torch.long)
        self.con = torch.tensor(token_sets["cont_ids"], device=dev, dtype=torch.long)

    @torch.no_grad()
    def from_resid(self, h: torch.Tensor) -> torch.Tensor:
        """h: (B, D) layer-L residual at the last position -> r: (B,) float32."""
        logits = self.head(self.norm(h.to(next(self.head.parameters()).dtype)))
        logits = logits.float()
        a = torch.logsumexp(logits.index_select(-1, self.ref), dim=-1)
        b = torch.logsumexp(logits.index_select(-1, self.con), dim=-1)
        return (a - b).float()

    @torch.no_grad()
    def from_logits(self, logits: torch.Tensor) -> torch.Tensor:
        """Same contrast computed on FINAL-layer logits (secondary column)."""
        logits = logits.float()
        a = torch.logsumexp(logits.index_select(-1, self.ref), dim=-1)
        b = torch.logsumexp(logits.index_select(-1, self.con), dim=-1)
        return (a - b).float()


class RandomAxisObservable:
    """CONTROL 1 — a random readout axis, fixed seed, several independent draws.

    r^rand_t = <resid_L, u> / ||u||. Must NOT reproduce any safety ordering.
    """

    def __init__(self, hidden: int, device: str, n_draws: int = 3, seed: int = 1234) -> None:
        g = torch.Generator(device="cpu").manual_seed(seed)
        u = torch.randn((n_draws, hidden), generator=g)
        u = u / u.norm(dim=-1, keepdim=True)
        self.u = u.to(device)
        self.n_draws = n_draws

    @torch.no_grad()
    def from_resid(self, h: torch.Tensor) -> torch.Tensor:
        """h: (B, D) -> (n_draws, B)."""
        return (self.u.float() @ h.float().T)


class DiffMeansObservable:
    """SECONDARY (descriptive only) — projection onto the harmful/benign
    difference-in-means unit vector at layer L.

    Explicitly NOT used for any headline claim: it is near-constant by
    construction on an abliterated model, which is exactly the confound the
    lexical r_t avoids.
    """

    def __init__(self, d_unit: torch.Tensor) -> None:
        self.d = d_unit.float()

    @torch.no_grad()
    def from_resid(self, h: torch.Tensor) -> torch.Tensor:
        return h.float() @ self.d


# --------------------------------------------------------------------------- #
# CONTROL 2 — syntactic (POS) observable.
# --------------------------------------------------------------------------- #

FUNCTION_WORDS = {
    "the", "a", "an", "of", "to", "in", "and", "or", "but", "for", "with", "on",
    "at", "by", "from", "as", "is", "was", "are", "were", "be", "been", "being",
    "that", "this", "these", "those", "it", "its", "he", "she", "they", "them",
    "his", "her", "their", "we", "us", "our", "you", "your", "i", "my", "me",
    "not", "no", "so", "if", "then", "than", "when", "while", "which", "who",
    "into", "over", "under", "about", "after", "before", "up", "down", "out",
    "there", "here", "all", "some", "any", "each", "both", "more", "most",
    "such", "can", "will", "would", "could", "should", "may", "might", "must",
    "do", "does", "did", "has", "have", "had", "am",
}

VERB_SUFFIXES = ("ing", "ed", "ise", "ize", "ate", "ify")


def coarse_pos(token_str: str) -> str:
    """Regex/stopword tagger mapped to {NOUN, VERB, FUNC, PUNCT, OTHER}.

    Used when nltk data is unavailable; `tag_with_nltk` is preferred and the
    choice is logged into method_out.json.
    """
    s = token_str.strip()
    if not s:
        return "OTHER"
    low = s.lower()
    if not any(c.isalnum() for c in s):
        return "PUNCT"
    if low in FUNCTION_WORDS:
        return "FUNC"
    if low.endswith(VERB_SUFFIXES):
        return "VERB"
    if s[0].isalpha():
        return "NOUN"
    return "OTHER"


def tag_with_nltk(tokens: list[str]) -> tuple[list[str], str]:
    """Try nltk POS tagging; fall back to the regex tagger. Returns (tags, method)."""
    try:
        import nltk

        try:
            nltk.data.find("taggers/averaged_perceptron_tagger_eng")
        except LookupError:
            nltk.download("averaged_perceptron_tagger_eng", quiet=True)
        tagged = nltk.pos_tag([t.strip() or "_" for t in tokens])
        out = []
        for _, tag in tagged:
            if tag.startswith("NN"):
                out.append("NOUN")
            elif tag.startswith("VB"):
                out.append("VERB")
            elif tag in {".", ",", ":", "``", "''", "(", ")", "#", "$"}:
                out.append("PUNCT")
            elif tag in {"DT", "IN", "CC", "PRP", "PRP$", "TO", "MD", "WDT", "WP", "WRB", "EX", "PDT"}:
                out.append("FUNC")
            else:
                out.append("OTHER")
        logger.info("POS tagging: nltk averaged_perceptron")
        return out, "nltk_averaged_perceptron"
    except Exception as exc:  # noqa: BLE001 - regex fallback by design
        logger.warning(f"nltk POS tagging unavailable ({exc}); using regex/stopword tagger")
        return [coarse_pos(t) for t in tokens], "regex_stopword_fallback"


class POSProbeObservable:
    """CONTROL 2 — a syntactic observable trained on layer-L residuals.

    Multinomial logistic probe over coarse POS of the NEXT token; the observable
    is log-odds(NOUN vs FUNC). If the safety ordering appears here too, we
    measured generic mixing, not a safety-specific basin -> DISCONFIRM.
    """

    def __init__(self, w: np.ndarray, b: np.ndarray, classes: list[str], device: str,
                 tagger: str, train_acc: float, n_train: int) -> None:
        self.classes = classes
        self.tagger = tagger
        self.train_acc = train_acc
        self.n_train = n_train
        self.i_noun = classes.index("NOUN")
        self.i_func = classes.index("FUNC")
        self.W = torch.tensor(w, dtype=torch.float32, device=device)  # (C, D)
        self.b = torch.tensor(b, dtype=torch.float32, device=device)  # (C,)

    @torch.no_grad()
    def from_resid(self, h: torch.Tensor) -> torch.Tensor:
        z = h.float() @ self.W.T + self.b
        return z[:, self.i_noun] - z[:, self.i_func]


@torch.no_grad()
def train_pos_probe(lm: LoadedModel, layer: int, text: str, max_tokens: int = 5000,
                    chunk: int = 512) -> POSProbeObservable | None:
    """Collect layer-L residuals over WikiText and fit the POS probe."""
    from sklearn.linear_model import LogisticRegression

    tok = lm.tokenizer
    ids = tok.encode(text, add_special_tokens=False)[: max_tokens + 1]
    if len(ids) < 200:
        logger.error("POS probe: not enough tokens")
        return None
    tok_strs = [tok.decode([i]) for i in ids]
    tags, tagger = tag_with_nltk(tok_strs)

    feats: list[np.ndarray] = []
    labels: list[str] = []
    layers = lm.layer_modules
    buf: dict[str, torch.Tensor] = {}

    def hook(_m: Any, _i: Any, o: Any) -> None:
        buf["h"] = (o[0] if isinstance(o, tuple) else o).detach()

    handle = layers[layer].register_forward_hook(hook)
    try:
        for start in range(0, len(ids) - 1, chunk):
            seg = ids[start : start + chunk]
            if len(seg) < 8:
                break
            inp = torch.tensor([seg], device=lm.device)
            lm.model(input_ids=inp, use_cache=False)
            h = buf["h"][0].float().cpu().numpy()  # (S, D)
            for j in range(len(seg) - 1):
                nt = tags[start + j + 1]
                if nt in ("NOUN", "VERB", "FUNC", "PUNCT"):
                    feats.append(h[j])
                    labels.append(nt)
            del h
    finally:
        handle.remove()
        buf.clear()

    if len(feats) < 200 or len(set(labels)) < 2:
        logger.error(f"POS probe: insufficient training data n={len(feats)}")
        return None
    X = np.stack(feats).astype(np.float32)
    y = np.array(labels)
    if "NOUN" not in set(y) or "FUNC" not in set(y):
        logger.error("POS probe: NOUN or FUNC class absent")
        return None
    # Standardise before fitting: raw residuals are large and wildly unequal in
    # scale across dimensions, which makes lbfgs crawl (minutes per model) and
    # leaves the probe badly conditioned. The scaler is folded back into (W, b)
    # afterwards, so the returned probe still applies directly to raw residuals
    # and nothing downstream needs to know.
    mu = X.mean(axis=0)
    sd = X.std(axis=0)
    sd[sd < 1e-6] = 1.0
    Xs = (X - mu) / sd
    clf = LogisticRegression(max_iter=300, C=1.0, tol=1e-3)
    clf.fit(Xs, y)
    acc = float(clf.score(Xs, y))
    classes = [str(c) for c in clf.classes_]
    W = clf.coef_ / sd[None, :]                       # (C, D) applied to raw h
    b = clf.intercept_ - (clf.coef_ / sd[None, :]) @ mu
    logger.info(
        f"{lm.key}: POS probe trained n={len(y)} classes={classes} train_acc={acc:.3f} "
        f"tagger={tagger} n_iter={getattr(clf, 'n_iter_', ['?'])[0]}"
    )
    return POSProbeObservable(
        W.astype(np.float32), b.astype(np.float32),
        classes, lm.device, tagger, acc, len(y),
    )

#!/usr/bin/env python3
"""The regeneration harness.

Template language
-----------------
    {{ptr:ALIAS#/rfc6901/pointer|fmt}}

ALIAS resolves through a FROZEN registry -- `render_registry.json`, written by
stage 2 and holding one {alias: {path, sha256}} entry per source file. `fmt` is
one of the names in FORMATS below. Anything else in the template is literal
text, and the NO_BARE_NUMERAL lint refuses to let a digit through unless it
matches an explicitly itemised allow-list entry.

This file is executable on its own:

    python render.py --template prose_template.md --out prose_bundle.md

and importable, which is how stage 2 drives the five assertions.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
REGISTRY_PATH = HERE / "render_registry.json"

PLACEHOLDER = re.compile(r"\{\{ptr:([A-Za-z0-9_]+)#([^|}]+)\|([a-z0-9_]+)\}\}")

# Digits that are legitimately literal in the template source. Every entry is
# itemised in the stage-2 output; nothing is suppressed silently.
BARE_NUMERAL_ALLOWLIST = [
    ("section_number", re.compile(r"§\s*\d+(?:\.\d+)*")),
    ("arxiv_id", re.compile(r"arXiv:\s*\d{4}\.\d{4,5}(?:v\d+)?")),
    ("bib_marker", re.compile(r"\[\d{1,2}(?:\s*,\s*\d{1,2})*\]")),
    ("year", re.compile(r"\b(?:19|20)\d{2}\b")),
    ("model_or_repo_name", re.compile(
        r"[A-Za-z][A-Za-z0-9]*(?:[-_.][A-Za-z0-9]+)*[-_.]\d+(?:[.p]\d+)*[A-Za-z-]*"
        r"|\b[A-Za-z]+\d+(?:\.\d+)?[Bb]\b")),
    ("layer_index", re.compile(r"\bL\s*=\s*\d+|layer\s+L\b")),
    ("table_or_figure_number", re.compile(r"(?:Table|Figure)\s+\d+")),
    ("latex_subscript", re.compile(r"_\{?\\?[a-zA-Z]*\d+\}?|\\alpha_\{?50\}?|"
                                   r"\\alpha_\{50\}")),
    ("axis_or_check_label", re.compile(r"\bcheck\s*\d\b|\bR[1-4]\b|\bC[1-5]\b|"
                                       r"\bH1b?\b|\bH[23]\b")),
    ("markdown_or_latex_scaffolding", re.compile(r"10\^\{?[+-]?\}?|\\times|\\%")),
    ("hash_algorithm_name", re.compile(r"sha256|SHA-?256|RFC\s*6901")),
    ("confidence_level_convention", re.compile(r"95\\?%\s*CI|95\\?% confidence")),
]


# ---------------------------------------------------------------------------
# formats
# ---------------------------------------------------------------------------
def _f(nd: int):
    def g(v):
        return f"{float(v):.{nd}f}"
    return g


def _ci(nd: int):
    def g(v):
        lo, hi = float(v[0]), float(v[1])
        return f"[{lo:.{nd}f}, {hi:.{nd}f}]"
    return g


def _sci(v):
    s = f"{float(v):.1e}"
    mant, expo = s.split("e")
    return f"{mant}e-{abs(int(expo)):02d}" if int(expo) < 0 else f"{mant}e+{int(expo):02d}"


FORMATS = {
    "int": lambda v: f"{int(round(float(v)))}",
    "int_comma": lambda v: f"{int(round(float(v))):,}",
    "f1": _f(1), "f2": _f(2), "f3": _f(3), "f4": _f(4), "f6": _f(6),
    "pct1": lambda v: f"{100.0 * float(v):.1f}\\%",
    "pct0": lambda v: f"{100.0 * float(v):.0f}\\%",
    "ci2": _ci(2), "ci3": _ci(3), "ci4": _ci(4),
    "sci": _sci,
    "signed3": lambda v: f"{float(v):+.3f}",
    "signed4": lambda v: f"{float(v):+.4f}",
    "str": lambda v: str(v),
    "usd": lambda v: f"\\${float(v):.4f}",
    "minutes": lambda v: f"{float(v) / 60.0:.1f}",
}


# ---------------------------------------------------------------------------
def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def resolve_pointer(doc, pointer: str):
    if pointer == "":
        return doc
    if not pointer.startswith("/"):
        raise ValueError(f"pointer must start with '/': {pointer!r}")
    cur = doc
    for raw in pointer[1:].split("/"):
        tok = raw.replace("~1", "/").replace("~0", "~")
        cur = cur[int(tok)] if isinstance(cur, list) else cur[tok]
    return cur


class Renderer:
    def __init__(self, registry_path: Path = REGISTRY_PATH,
                 overrides: dict | None = None) -> None:
        self.registry = json.loads(Path(registry_path).read_text())
        self.docs: dict[str, object] = {}
        self.overrides = overrides or {}
        self.resolved: list[dict] = []

    def _doc(self, alias: str):
        if alias not in self.docs:
            entry = self.registry.get(alias)
            if entry is None:
                raise KeyError(f"unknown alias {alias!r}; registry holds "
                               f"{sorted(self.registry)}")
            p = Path(entry["path"])
            got = sha256_file(p)
            if got != entry["sha256"]:
                raise ValueError(f"alias {alias}: sha256 drift\n  frozen {entry['sha256']}"
                                 f"\n  on disk {got}")
            self.docs[alias] = json.loads(p.read_text())
        return self.docs[alias]

    def value(self, alias: str, pointer: str):
        key = f"{alias}#{pointer}"
        if key in self.overrides:
            return self.overrides[key]
        return resolve_pointer(self._doc(alias), pointer)

    def render(self, template: str) -> str:
        self.resolved = []

        def sub(m: re.Match) -> str:
            alias, pointer, fmt = m.group(1), m.group(2), m.group(3)
            if fmt not in FORMATS:
                raise KeyError(f"unknown format {fmt!r}; known: {sorted(FORMATS)}")
            v = self.value(alias, pointer)
            out = FORMATS[fmt](v)
            self.resolved.append({"alias": alias, "pointer": pointer, "fmt": fmt,
                                  "raw": v, "rendered": out})
            return out

        return PLACEHOLDER.sub(sub, template)


# ---------------------------------------------------------------------------
def unresolved_placeholders(text: str) -> list[str]:
    return re.findall(r"\{\{[^}]*\}\}", text)


def bare_numerals(template: str) -> list[dict]:
    """Digits in the TEMPLATE SOURCE that are neither inside a placeholder nor
    covered by an itemised allow-list entry."""
    spans = [m.span() for m in PLACEHOLDER.finditer(template)]
    for _, rx in BARE_NUMERAL_ALLOWLIST:
        spans.extend(m.span() for m in rx.finditer(template))
    out = []
    for m in re.finditer(r"\d[\d,.]*", template):
        s, e = m.span()
        if any(a <= s and e <= b for a, b in spans):
            continue
        line = template[:s].count("\n") + 1
        out.append({"line": line, "text": m.group(0),
                    "context": template[max(0, s - 60):e + 40].replace("\n", " ")})
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--template", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--registry", default=str(REGISTRY_PATH))
    a = ap.parse_args()
    r = Renderer(Path(a.registry))
    text = Path(a.template).read_text()
    rendered = r.render(text)
    left = unresolved_placeholders(rendered)
    if left:
        raise SystemExit(f"unresolved placeholders: {left[:5]}")
    Path(a.out).write_text(rendered)
    print(f"rendered {len(r.resolved)} pointers -> {a.out}")


if __name__ == "__main__":
    main()

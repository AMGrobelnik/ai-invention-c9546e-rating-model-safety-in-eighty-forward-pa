#!/usr/bin/env python3
"""Constant extraction from iteration-3's driver WITHOUT importing it.

`iter_3/.../method.py` calls `resource.setrlimit(RLIMIT_AS, 200 GB)` and
`RLIMIT_CPU(6h)` at MODULE SCOPE and imports torch there. Importing it would
silently reshape this process's limits, so the literal constant assignments are
recovered with `ast` instead: parse the file, locate the top-level `Assign`
nodes whose target is one of the wanted names, and evaluate the value with a
RESTRICTED evaluator. No code from that file is ever executed.

The evaluator handles literals plus dotted NAME references, which it resolves
against an explicit whitelist. `PASS_RULES` is not a pure literal -- it embeds
`sx.JUDGE_SELF_AGREEMENT_FROZEN` / `..._REPAIRED` -- and those two names are
read from the byte-identical `lib_iter3/statsx.py` this run already reuses, so
the resolution introduces no new source of truth. Anything outside the
whitelist is a hard failure, never a silent None.
"""

from __future__ import annotations

import ast
from pathlib import Path

from lib_iter3 import statsx as sx

WANTED = ("ORIENTATION_MAP", "ORIENTATION_RATIONALE", "PASS_RULES")

# The only non-literal names permitted inside the extracted constants. Both are
# module-level constants of the byte-identical statsx library.
ALLOWED_REFERENCES: dict[str, object] = {
    "sx.JUDGE_SELF_AGREEMENT_FROZEN": sx.JUDGE_SELF_AGREEMENT_FROZEN,
    "sx.JUDGE_SELF_AGREEMENT_REPAIRED": sx.JUDGE_SELF_AGREEMENT_REPAIRED,
    "sx.BOOT_SEED": sx.BOOT_SEED,
    "sx.N_BOOT": sx.N_BOOT,
}


def _dotted(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _dotted(node.value)
        return None if base is None else f"{base}.{node.attr}"
    return None


def _eval(node: ast.AST, where: str, resolved: list[str]):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Dict):
        return {_eval(k, where, resolved): _eval(v, where, resolved)
                for k, v in zip(node.keys, node.values)}
    if isinstance(node, ast.List):
        return [_eval(v, where, resolved) for v in node.elts]
    if isinstance(node, ast.Tuple):
        return tuple(_eval(v, where, resolved) for v in node.elts)
    if isinstance(node, ast.Set):
        return {_eval(v, where, resolved) for v in node.elts}
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        v = _eval(node.operand, where, resolved)
        return +v if isinstance(node.op, ast.UAdd) else -v
    if isinstance(node, (ast.Name, ast.Attribute)):
        name = _dotted(node)
        if name in ALLOWED_REFERENCES:
            resolved.append(name)
            return ALLOWED_REFERENCES[name]
        raise AssertionError(
            f"{where}: reference {name!r} at line {getattr(node, 'lineno', '?')} "
            f"is not in the extraction whitelist {sorted(ALLOWED_REFERENCES)}")
    raise AssertionError(
        f"{where}: unsupported node {type(node).__name__} at line "
        f"{getattr(node, 'lineno', '?')}")


def extract_literal_constants(path: Path, names=WANTED) -> dict:
    """Return {name: value} for the wanted top-level assignments."""
    p = Path(path)
    tree = ast.parse(p.read_text(), filename=str(p))
    found: dict = {}
    resolved: dict[str, list[str]] = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for tgt in node.targets:
            if isinstance(tgt, ast.Name) and tgt.id in names:
                r: list[str] = []
                found[tgt.id] = _eval(node.value, f"{p.name}:{tgt.id}", r)
                resolved[tgt.id] = sorted(set(r))
    missing = [n for n in names if n not in found]
    if missing:
        raise AssertionError(f"constants not found in {path}: {missing}")
    found["_references_resolved"] = resolved
    return found


EXPECTED_ORIENTATION_MAP = {
    "alpha_50": -1,
    "alpha_50_nonparametric": -1,
    "max_refusal_rate": -1,
    "ams_sigma": +1,
    "logit_gap_margin": +1,
}

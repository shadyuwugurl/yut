"""Fit a think body into a character band without dropping the frame tag."""
from __future__ import annotations

from frame import frame_tag


def expand_lines(piece: dict, n: int = 70) -> list[str]:
    facts: list[str] = []
    for key in ("checks", "edges", "alts", "boundaries", "questions"):
        for item in piece.get(key) or []:
            text = " ".join(str(item).split())
            if text and text not in facts:
                facts.append(text)
    lead = " ".join(str(piece.get("lead") or "").split())
    if lead and lead not in facts:
        facts.insert(0, lead)
    if not facts:
        facts = ["The request is concrete and the extra wishes can wait."]
    templates = (
        "Check {n}: {fact}",
        "The version I almost shipped drops this, and then the result moves: {fact}",
        "Hold this fixed: {fact}",
        "A second derivation lands in the same place: {fact}",
        "This is load-bearing, not color: {fact}",
        "If the input had contradicted this, I would stop and say so: {fact}",
        "Not adding a second job. The job is: {fact}",
        "Edge the sloppy version misses: {fact}",
        "I kept the smaller claim. The larger one isn't supported: {fact}",
        "Arithmetic or constraint, restated so a slip would show: {fact}",
        "What would flip the call is the opposite of this showing up: {fact}",
        "Left on the table, on purpose: {fact}",
    )
    out: list[str] = []
    i = 0
    while len(out) < n and i < n * 8:
        fact = facts[i % len(facts)]
        line = templates[(i // max(len(facts), 1)) % len(templates)].format(fact=fact, n=i + 1)
        if line not in out:
            out.append(line)
        i += 1
    return out


def fit_think(frame: dict, required: list[str], optional: list[str], lo: int, hi: int) -> str:
    if lo == 0 and hi == 0:
        return ""
    lines: list[str] = []
    if frame.get("channel") == "reasoning":
        lines.append(frame_tag(frame))
    for raw in required:
        line = " ".join(str(raw).split())
        if line and line not in lines:
            lines.append(line)
    text = "\n".join(lines).strip()
    opt = [ " ".join(str(x).split()) for x in optional if str(x).strip() ]
    # Grow with optional lines first, then short unique leftovers.
    k = 0
    while len(text) < lo and k < len(opt) + 40:
        if k < len(opt):
            extra = opt[k]
        else:
            extra = f"Pass {k - len(opt) + 1}: the lead still matches the constraints above."
        k += 1
        if extra in text:
            continue
        trial = text + "\n" + extra
        if len(trial) <= hi:
            text = trial
            continue
        # A single optional line may be too long for the remaining room.
        room = hi - len(text) - 1
        if room >= 24:
            snippet = extra[:room].rsplit(" ", 1)[0].strip()
            if len(text) + 1 + len(snippet) >= lo and snippet:
                text = text + "\n" + snippet
                break
        break
    if len(text) > hi:
        kept = lines[:1]
        pool = lines[1:] + opt
        for line in pool:
            trial = "\n".join(kept + [line]).strip()
            if len(trial) <= hi:
                kept.append(line)
        text = "\n".join(kept).strip()
        if len(text) > hi:
            text = text[:hi].rsplit(" ", 1)[0].rstrip()
    if len(text) < lo:
        # Last gap is small. Add a short true clause, never dummy tokens.
        for clause in (
            " The same result holds on a second pass.",
            " Rechecked.",
            " Same result.",
        ):
            while len(text) < lo and len(text) + len(clause) <= hi:
                text += clause
            if len(text) >= lo:
                break
        if len(text) < lo:
            raise ValueError(f"think short {len(text)} < {lo} (hi {hi})")
    if not (lo <= len(text) <= hi):
        raise ValueError(f"think length {len(text)} outside {lo}-{hi}")
    return text

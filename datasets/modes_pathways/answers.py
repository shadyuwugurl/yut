"""Visible answers. The think channel is separate. No frame is announced out here."""
from __future__ import annotations

from frame import Spec

DEPTH_CAP = {
    "banter": "short",
    "stream": "tiny",
    "react": "short",
    "complete": "short",
    "skim": "short",
    "vibe": "short",
    "hotpot": "short",
    "heal": "short",
    "settle": "short",
    "pattern": "short",
}


def depth_of(spec: Spec) -> str:
    key = (spec.category, spec.id)
    if spec.category == "thinking_effort" and spec.id == "off":
        return "tiny"
    if spec.category == "channel" and spec.id == "instruct":
        return "normal"
    if spec.category == "reasoning_effort":
        return {
            "effort_low": "tiny",
            "effort_medium_low": "short",
            "effort_medium": "normal",
            "effort_high": "long",
            "effort_ultra": "verbose",
            "effort_xultra": "verbose",
        }[spec.id]
    if spec.category == "protium":
        return {
            "hermes": "tiny",
            "apollo": "short",
            "artemis": "normal",
            "athena": "normal",
            "prometheus": "long",
            "solstice": "long",
            "hyperion": "long",
            "einstein": "verbose",
            "oracle": "verbose",
            "proteus": "normal",
            "swarm": "normal",
            "council": "normal",
        }[spec.id]
    if spec.category == "mode" and spec.id == "extreme":
        return "verbose"
    if spec.category == "mode" and spec.id in ("stream", "complete", "skim", "banter", "vibe", "heal", "settle"):
        return DEPTH_CAP.get(spec.id, "short")
    if spec.category == "reasoning_mode":
        return "long"
    if spec.category == "orbit" or spec.category == "stance":
        return "short"
    if spec.id in ("s1",) or (spec.category == "mode" and spec.home == "s1"):
        return "short"
    if spec.category == "mode" and spec.home == "s3":
        return "normal"
    return "normal"


def _cap(family: str, depth: str) -> str:
    order = ["tiny", "short", "normal", "long", "verbose"]
    cap = DEPTH_CAP.get(family)
    if not cap:
        return depth
    return order[min(order.index(depth), order.index(cap))]


def _code_block(piece: dict) -> str:
    if not piece.get("code"):
        return ""
    return "```python\n" + piece["code"].rstrip() + "\n```"


def family_body(spec: Spec, piece: dict) -> str:
    family = piece["family"]
    depth = _cap(family, depth_of(spec))
    lead = piece["lead"].strip()
    detail = (piece.get("detail") or "").strip()
    edges = piece.get("edges") or []
    alts = piece.get("alts") or []
    code = _code_block(piece)

    if family == "complete":
        return lead if depth == "tiny" else lead + "\n\n" + detail

    if family == "code" or (code and family in ("build",)):
        parts = [lead, "", "Assumptions: " + detail]
        if code:
            parts += ["", code]
        if depth in ("long", "verbose") and edges:
            parts += ["", "Edges: " + " ".join(edges[:2])]
        return "\n".join(parts).strip()

    if depth == "tiny":
        return lead
    if depth == "short":
        return f"{lead}\n\n{detail}" if detail and detail != lead else lead

    parts = [lead, "", detail]
    if depth in ("long", "verbose") and edges:
        parts += ["", "What would flip it: " + edges[0]]
    if depth == "verbose" and alts:
        parts += ["", "I left this on the table: " + alts[0]]
    if code and depth in ("normal", "long", "verbose"):
        parts += ["", code]
    if family == "teach" and piece.get("questions") and depth != "tiny":
        parts += ["", piece["questions"][0]]
    if family == "brainstorm" and depth in ("normal", "long", "verbose"):
        parts += ["", "The other two were a reminder text and a public late list. Neither changes the cost of keeping the drill."]
    if family == "research" and depth in ("normal", "long", "verbose"):
        parts += ["", "Blog: D. City report: B, wrong pipe. Sticky note: C, a symptom. Nothing here is a test of this tap."]
    return "\n".join(p for p in parts if p is not None).strip()


def protium_answer(spec: Spec, piece: dict) -> str:
    ident = spec.id
    body = family_body(spec, piece)
    if ident == "swarm":
        return (
            "[SWARM VERDICT]\n"
            + piece["lead"].strip()
            + "\n\nThe logician wanted the smallest mechanism that survives the constraint. "
            "The critic wanted the option we can staff. They agree on the pick above, "
            "and the objection that survived is: "
            + (piece.get("edges") or ["the missing fact could still flip it"])[0]
        )
    if ident == "council":
        return (
            "[COUNCIL VERDICT]\n"
            + piece["lead"].strip()
            + "\n\nRuling stands. The dissent that was paid for: "
            + (piece.get("edges") or ["a missing measurement"])[0]
        )
    if ident == "hermes":
        return piece["lead"].strip()
    if ident == "apollo":
        return piece["lead"].strip() + "\n\n" + (piece["checks"][0] if piece.get("checks") else piece["detail"])
    if ident == "artemis":
        return (
            body
            + "\n\nEmpty input, a single element, and the off-by-one at the end are the cases that have to return the boring answer, not throw."
        )
    if ident == "prometheus":
        return (
            body
            + "\n\nIf the dependency is down, return the last good result and a named error. Don't retry it into a pile."
        )
    if ident == "oracle":
        return (
            piece["lead"].strip()
            + "\n\n"
            + "\n".join(piece.get("checks") or [])
            + "\n\nNo placeholder. The check is the proof."
        )
    return body


def agi_answer(spec: Spec, piece: dict) -> str:
    ident = spec.id
    base = family_body(spec, piece)
    lead = piece["lead"].strip()
    detail = (piece.get("detail") or "").strip()
    if ident == "agi-teacher-coder":
        return base + "\n\nWalk an empty input before you trust it. What should it return, and does this?"
    if ident == "agi-teacher-business":
        return (
            f"{lead}\n\nThe tradeoff in one line: {detail}\n\n"
            "If you had to teach this to the person who signs the invoice, you'd stop at that sentence."
        )
    if ident == "agi-teacher-007":
        return (
            f"{lead}\n\n"
            "What changed between attempts is the part worth keeping. "
            "Same command with a fresh hope is how the loop starts."
        )
    if ident == "agi-brainstorm-007":
        return (
            f"{lead}\n\n"
            "Three angles were on the table. The one that executes is the one with a next command, not the cleverest sentence."
        )
    if ident == "agi-brainstorm-business":
        return base + "\n\nRanked by whether this team can ship it this month, not by how new it sounds."
    if ident == "agi-brainstorm-coder":
        return base + "\n\nThe other designs were real. This is the one I'd commit."
    if ident == "agi-brainstorm-comedy":
        return lead + "\n\nThe other two were a reminder email and a poster. Neither one is a joke or a fix."
    if ident == "agi-brainstorm-house":
        return (
            f"{lead}\n\n"
            "Differentials that died: a full rewrite, and a process poster. "
            "The test that killed them is headcount. The survivor is the one that fits the people you have."
        )
    if ident == "agi-brainstorm-matlock":
        return (
            f"{lead}\n\n"
            "The record you actually have supports that and not the dramatic version. "
            "I'd put the other theories in a drawer until there's a document."
        )
    if ident == "agi-brainstorm-prompt":
        draft = (
            "Do the task in the user's constraints. Lead with the result. "
            "Name the one limitation. Do not add a second project. "
            "If a number is required, compute it and show the check."
        )
        return (
            f"Use this:\n\n{draft}\n\n"
            "What changed: the failure mode was a vague 'be helpful', so the constraint and the check are now explicit."
        )
    if ident == "agi-brainstorm-stark":
        return f"{lead}\n\nBuild: {detail} Ship the smallest version that proves the mechanism."
    if ident == "agi-brainstorm-story":
        return (
            f"{lead}\n\n"
            "The other scene was them talking about the plan. This one moves a cup, a key, or a door."
        )
    if ident == "agi-musk-brainstorm":
        return f"{lead}\n\nDelete the part that doesn't change the physics or the cost. What remains is the option."
    if ident == "agi-musk-business":
        return f"{lead}\n\nUnit cost and the actual constraint are the same decision. {detail}"
    if ident == "agi-musk-curie":
        return (
            f"{lead}\n\n"
            "The measurement that would falsify it: "
            + (piece.get("edges") or ["a number you haven't collected yet"])[0]
        )
    if ident == "agi-pkd-house":
        return (
            f"Assume the obvious story is the costume. {lead}\n\n"
            "The test is small and mean: it has to be able to come back false."
        )
    if ident == "agi-pkd-neo":
        return (
            f"The rule under the appearance: {detail}\n\n{lead}"
        )
    if ident == "agi-pkd-comedy":
        return (
            f"Everyone agrees the system is fine, which is how you know to look at it twice. {lead}"
        )
    if ident == "agi-house-comedy":
        return f"{lead} That's the whole diagnosis, and it's funnier because it's the boring cause."
    if ident == "agi-pkd-vader-comedy":
        return (
            f"\"{lead}\"\n\nHe said it like the room had filed the wrong paperwork on purpose. "
            "Nobody laughed until they realized he was also right."
        )
    if ident == "agi-stark-comedy":
        return f"{lead}\n\nYes, the showy version exists. No, we're not building it."
    if ident == "agi-stark-musk-coder":
        return base + "\n\nFirst principles got us to this loop. The commit is the loop, not a platform around it."
    if ident == "agi-stark-musk-curie":
        return (
            base
            + "\n\nShow the measurement next to the claim: "
            + (piece["checks"][0] if piece.get("checks") else detail)
        )
    if ident == "agi-vader-comedy":
        return (
            f"\"{lead}\"\n\nThe room went quiet in a way that was, unfortunately, a little funny."
        )
    return base


def orbit_answer(ident: str, piece: dict) -> str:
    lead = piece["lead"].strip()
    if ident == "contextual_sanity":
        return (
            f"{lead}\n\n"
            "I'm using the prices, the headcount, and the two headaches. "
            "I don't need another fact to pick."
        )
    if ident == "provisional_judgment":
        edge = (piece.get("edges") or ["A budget nobody stated shows up."])[0]
        if edge.lower().startswith("if "):
            clause = edge[0].lower() + edge[1:]
            return f"{lead}\n\nI'd revise this {clause}"
        return f"{lead}\n\nI'd revise this if {edge}"
    if ident == "childlike_capacity":
        return (
            f"{lead}\n\n"
            "The playful version, still legal: put the two light-sensitive people nearest the window in B "
            "and let everyone else complain about the view."
        )
    return (
        f"{lead}\n\n"
        "This is only the prices and the two headaches in the note. "
        "It says nothing about next quarter, the building's other rooms, or a budget cap."
    )


def deckard_answer(piece: dict) -> str:
    return piece["lead"].strip()


def jumbo_answer(piece: dict) -> str:
    lines = []
    for heading in piece["contract"]:
        lines.append(f"## {heading}")
        lines.append(piece["sections"][heading])
        lines.append("")
    return "\n".join(lines).strip()


def loop_answer(piece: dict) -> str:
    return (
        piece["lead"].strip()
        + "\n\nThe thin version of the middle step was 'book the hall', and that step was already done. "
        + piece["detail"].strip()
    )


def html_answer(palette: str, piece: dict) -> str:
    place_line = piece["detail"]
    title = "Library desk"
    if palette == "luxury":
        css = """
    :root { color-scheme: dark; }
    body { margin: 0; background: #08090C; color: #f4efe4; font-family: "Iowan Old Style", Palatino, serif; }
    main { max-width: 420px; margin: 8vh auto; padding: 32px; border: 1px solid rgba(255,255,255,0.07);
           background: linear-gradient(180deg, #111319, #08090C); }
    h1 { font-weight: 500; letter-spacing: -0.03em; font-size: clamp(2rem, 4vw, 3rem); margin: 0 0 12px; }
    p { color: #c8c2b4; line-height: 1.5; }
    button { background: linear-gradient(135deg, #F4D068, #AA771C); color: #08090C; border: 0; padding: 12px 18px;
             font-family: inherit; cursor: pointer; }
    button:hover { filter: brightness(1.05); }
    button:focus-visible { outline: 1px solid #F4D068; outline-offset: 3px; }
"""
        body = f"<main><h1>{title}</h1><p>{place_line}</p><button type=\"button\">Request a key</button></main>"
    elif palette == "cyberpunk":
        css = """
    body { margin: 0; background: #040508; color: #00F0FF; font-family: ui-monospace, monospace; }
    .hud { margin: 24px; border: 1px solid #00F0FF; padding: 16px; background: rgba(0,240,255,0.04); }
    .lbl { font-size: 11px; letter-spacing: 0.14em; text-transform: uppercase; color: #FAFF00; }
    strong { color: #FF0055; }
    button { background: transparent; color: #00F0FF; border: 1px solid #00F0FF; padding: 8px 12px; font-family: inherit; }
    button:hover { color: #040508; background: #00F0FF; }
    button:focus-visible { outline: 1px solid #FF0055; }
"""
        body = "<section class=\"hud\"><div class=\"lbl\">desk / live</div><p>Channel <strong>OPEN</strong></p><button type=\"button\">Arm mic</button></section>"
    elif palette == "editorial":
        css = """
    body { margin: 0; background: #F9F8F6; color: #121212; font-family: Georgia, serif; }
    main { max-width: 36rem; margin: 12vh auto; padding: 0 24px; }
    h1 { font-size: clamp(3rem, 8vw, 5.5rem); line-height: 0.9; letter-spacing: -0.03em; margin: 0; }
    p { font-family: "Avenir Next", sans-serif; max-width: 28rem; }
    hr { border: 0; border-top: 1px solid #121212; margin: 24px 0; }
"""
        body = f"<main><p>Market notes</p><h1>Morning in the aisle</h1><hr><p>{place_line}</p></main>"
    elif palette == "neobrutalism":
        css = """
    body { margin: 0; background: #fff4d6; color: #000; font-family: "Arial Black", sans-serif; }
    .card { margin: 32px; background: #ffe14a; border: 3px solid #000; box-shadow: 4px 4px 0 #000; padding: 20px; max-width: 360px; }
    button { background: #b8ff6a; border: 3px solid #000; box-shadow: 4px 4px 0 #000; padding: 10px 14px; font-family: inherit; cursor: pointer; }
    button:active { transform: translate(2px, 2px); box-shadow: 2px 2px 0 #000; }
    button:focus-visible { outline: 3px solid #000; }
"""
        body = "<article class=\"card\"><h1>Borrow a drill</h1><p>$0 until Thursday.</p><button type=\"button\">Hold my card</button></article>"
    elif palette == "bento":
        css = """
    body { margin: 0; background: #0D1117; color: #e8eef7; font-family: Inter, sans-serif; }
    .grid { display: grid; grid-template-columns: 2fr 1fr; gap: 12px; padding: 24px; }
    article { background: #161B22; border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 16px; }
    .wide { grid-column: span 2; }
    .n { font-size: 2rem; text-shadow: 0 0 18px rgba(120,160,255,0.45); }
"""
        body = "<section class=\"grid\"><article class=\"wide\"><div class=\"n\">128</div><p>tools out</p></article><article><div class=\"n\">4</div><p>late</p></article><article><div class=\"n\">12</div><p>due today</p></article></section>"
    elif palette == "svg_isometric":
        css = "body { margin: 0; background: #f3f1ea; display: grid; place-items: center; min-height: 100vh; } svg { width: min(480px, 90vw); height: auto; }"
        body = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 220" role="img">
  <title>Three crates</title>
  <polygon points="150,40 230,80 150,120 70,80" fill="#f7f4ee"/>
  <polygon points="70,80 150,120 150,180 70,140" fill="#c9c2b4"/>
  <polygon points="230,80 150,120 150,180 230,140" fill="#8d877c"/>
  <polygon points="150,100 210,130 150,160 90,130" fill="#fff" opacity="0.9"/>
</svg>"""
    else:
        css = """
    body { margin: 0; background: oklch(0.16 0.02 260); color: oklch(0.96 0.01 260);
           font-family: "Söhne", "Avenir Next", sans-serif; }
    .panel { margin: 10vh auto; max-width: 420px; padding: 24px; border-radius: 18px;
             background: oklch(0.22 0.02 260);
             border: 1px solid oklch(0.4 0.02 260 / 0.4);
             box-shadow: 0 1px 0 oklch(1 0 0 / 0.08) inset, 0 24px 40px oklch(0 0 0 / 0.35);
             backdrop-filter: blur(16px); }
    .switch { width: 48px; height: 28px; border-radius: 999px; border: 0; background: oklch(0.4 0.03 260); position: relative; }
    .switch i { position: absolute; top: 3px; left: 3px; width: 22px; height: 22px; border-radius: 50%; background: white;
                transition: transform 380ms cubic-bezier(0.34, 1.56, 0.64, 1); }
    .switch[aria-pressed="true"] i { transform: translateX(20px); }
    .switch:focus-visible { outline: 2px solid oklch(0.8 0.05 260); }
"""
        body = (
            "<section class=\"panel\"><h1>Desk lamp</h1>"
            f"<p>{place_line}</p>"
            "<button class=\"switch\" type=\"button\" aria-pressed=\"false\" onclick=\"this.setAttribute('aria-pressed', this.getAttribute('aria-pressed')!=='true')\"><i></i></button>"
            "</section>"
        )
    price = piece.get("price")
    if price is not None:
        body += f'\n<p class="fig">{price}</p>'
    return (
        "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
        f"<title>{title}</title>\n<style>{css}\n</style>\n</head>\n<body>\n{body}\n</body>\n</html>"
    )


def render_answer(spec: Spec, piece: dict) -> str:
    if spec.category == "aesthetic":
        return html_answer(spec.id, piece)
    if spec.category == "protium":
        return protium_answer(spec, piece)
    if spec.category == "agi":
        return agi_answer(spec, piece)
    if spec.category == "orbit":
        return orbit_answer(spec.id, piece)
    if spec.category == "stance":
        return deckard_answer(piece)
    if spec.category == "patch":
        return jumbo_answer(piece)
    if spec.category == "reasoning_mode":
        return loop_answer(piece)
    if spec.category == "channel" and spec.id == "instruct":
        body = family_body(spec, piece)
        # Lead with the result. Strip a leading hedge if one snuck in.
        return body
    if spec.category == "thinking_effort" and spec.id == "off":
        if piece.get("code"):
            return piece["lead"].strip() + "\n\n" + _code_block(piece)
        return piece["lead"].strip()
    return family_body(spec, piece)

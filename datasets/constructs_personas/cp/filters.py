"""Schema, leak, safety, and near-duplicate checks.

Trigger keywords are routing handles: taxonomy ids, aliases, card titles,
and frame announcements. Ordinary English inside an assistant answer is
kept. A private [frame: ...] tag is allowed only as the last line of a
<think> block, matching docs/SKINNY.md.
"""
from __future__ import annotations

import hashlib
import re
from typing import Iterable

from .taxonomy import items, load

SHORT_SYSTEMS = (
    "You are a helpful assistant.",
    "Answer the person in front of you.",
    "Be direct.",
)

FRAME_TAG = re.compile(
    r"^\[frame: pathway=(s1|s2|s3)\|mode=[a-z0-9_]+\|"
    r"(?:construct=[a-z0-9_-]+\|)?persona=[a-z0-9_-]+\|"
    r"identity=none\|theme=none\|channel=reasoning\]$"
)
THINK_RE = re.compile(r"^<think>\n(.*?)\n</think>\n\n(.*)\Z", re.S)
ROLES = {"system", "user", "assistant"}

# Invented handles and aliases that are not ordinary words. Banned in every
# user-visible channel and inside think (the frame tag is exempt).
HANDLES = {
    "ai_engineer", "uber_shrink", "relationship_deep", "top_dawg", "boy_kisser",
    "influencer_sfw", "influencer_nsfw", "deeptree", "holodeck", "shitpost",
    "drabble", "kitbash", "livewire", "griefer", "socrates", "arbiter",
    "x007", "agent_007", "xhyper", "xomni", "xdeeptree", "xsocrates", "xlogic",
    "xcomedy", "xbusiness", "xstory", "xteacher", "xcoder", "xeinstein",
    "xbrainstorm", "xspoon", "dau_einstein", "twin_turbo_brainstormer",
    "deep_research", "qwen_deep_research", "einstein", "spoon",
}
# Names the voice must not announce. Inhabiting the voice is the point.
PROPER = {
    "elon", "musk", "joker", "harley", "quinn", "vader", "darth", "philip",
    "curie", "skłodowska", "sklodowska", "matlock", "jarvis", "stark",
    "pkd", "007",
}
PROPER_PHRASES = (
    "dr. house", "dr house", "gregory house", "philip k", "iron man",
    "darth vader", "harley quinn", "tony stark",
)

ROUTING = re.compile(
    r"\b(constructs?|personas?|taxonomy|frame card|mode locked|construct locked|persona locked)\b"
    r"|\(forced\)"
    r"|\bi am in\b|\bi'm in\b|\bswitching into\b|\bact as a\b|\broleplay as\b",
    re.I,
)
MINOR = re.compile(
    r"\b(child|children|kid|kids|minor|minors|underage|under-age|preteen|pre-teen|"
    r"lolita|loli|shota|toddler|infant|paedo\w*|pedo\w*|jailbait|teenager|schoolgirl|"
    r"schoolboy|young girl|young boy|little girl|little boy)\b",
    re.I,
)
SEXUAL = re.compile(
    r"\b(sex|sexual|nude|naked|erotic|orgasm|blowjob|cock|pussy|fetish|kink|"
    r"horny|cum|nipple|lingerie|moan|thrust)\b",
    re.I,
)
AGE = re.compile(r"\b(\d{1,2})\s*(?:years?\s*old|yo)\b", re.I)
SLUR = re.compile(
    r"\b(nigger|nigga|faggot|retard|kike|spic|chink|tranny)\b",
    re.I,
)
HARM_MANUAL = re.compile(
    r"\b(how to (make|build) a (bomb|explosive|weapon)|step-by-step (sabotage|intrusion)|"
    r"pick the lock|exploit (the|this) (server|host)|payload|credential dump)\b",
    re.I,
)


def _handles():
    extra = set(HANDLES)
    for it in items():
        for alias in it.get("aliases") or []:
            if len(alias) >= 4 and alias.lower() not in {"help"}:
                # keep distinctive aliases; skip ones that are also ordinary ids
                if "_" in alias or alias.lower().startswith("x") or alias.lower() in HANDLES:
                    extra.add(alias.lower())
    extra.update(HANDLES)
    return extra


def split_think(content: str):
    m = THINK_RE.match(content)
    if not m:
        return None, content
    return m.group(1), m.group(2)


def visible_text(content: str) -> str:
    _think, visible = split_think(content)
    return visible if _think is not None else content


def _tag_line(think: str) -> str | None:
    if think is None:
        return None
    lines = think.split("\n")
    tags = [ln for ln in lines if ln.startswith("[frame:")]
    if not tags:
        return ""
    if tags != [lines[-1]] or not FRAME_TAG.match(lines[-1]):
        return None
    return lines[-1]


def frame_tag_ok(think: str, frame: dict) -> bool:
    tag = _tag_line(think)
    if tag is None:
        return False
    if tag == "":
        return True
    pathway = frame.get("pathway")
    persona = frame.get("persona") or "neutral"
    if f"pathway={pathway}" not in tag or f"persona={persona}" not in tag:
        return False
    construct = frame.get("construct")
    if construct:
        if f"construct={construct}|" not in tag:
            return False
    elif "construct=" in tag:
        return False
    return True


def opening_tag_ok(think: str, switch: dict) -> bool:
    """First turn of a switch may carry the frame being left."""
    tag = _tag_line(think)
    if tag is None:
        return False
    if tag == "":
        return True
    ident = switch.get("from")
    category = switch.get("from_category")
    if category == "construct":
        return f"construct={ident}|" in tag
    if category == "persona":
        return f"persona={ident}|" in tag
    return False


def _word(pattern_word: str, text: str) -> bool:
    return re.search(rf"\b{re.escape(pattern_word)}\b", text, re.I) is not None


def leak_hits(text: str, banned_words: Iterable[str]) -> list[str]:
    hits = []
    low = text.lower()
    for handle in _handles():
        if handle in low:
            hits.append(handle)
    for name in PROPER:
        if _word(name, low):
            hits.append(name)
    for phrase in PROPER_PHRASES:
        if phrase in low:
            hits.append(phrase)
    if ROUTING.search(text):
        hits.append("routing")
    for word in banned_words:
        if word and _word(word, low):
            hits.append(word)
    return hits


def safety_hits(text: str, nsfw: bool) -> list[str]:
    hits = []
    if SLUR.search(text):
        hits.append("slur")
    if HARM_MANUAL.search(text):
        hits.append("harm-manual")
    ages = [int(n) for n in AGE.findall(text)]
    if any(age < 18 for age in ages):
        hits.append("under-18")
    minor = MINOR.search(text)
    sexual = SEXUAL.search(text)
    if minor and (sexual or nsfw):
        hits.append("minor-sexual")
    if nsfw and minor:
        hits.append("minor-in-nsfw")
    return hits


def check_roles(messages: list) -> str | None:
    if not messages:
        return "empty messages"
    idx = 0
    if messages[0].get("role") == "system":
        content = messages[0].get("content")
        if content not in SHORT_SYSTEMS:
            return "system prompt is not a short allowlisted line"
        idx = 1
    rest = messages[idx:]
    if not rest or rest[0].get("role") != "user":
        return "conversation must start with user"
    if rest[-1].get("role") != "assistant":
        return "conversation must end with assistant"
    expect = "user"
    for msg in rest:
        role = msg.get("role")
        if role != expect:
            return f"role order broken, expected {expect}"
        content = msg.get("content")
        if not isinstance(content, str) or not content.strip():
            return "empty content"
        expect = "assistant" if expect == "user" else "user"
    return None


def check_example(ex: dict) -> list[str]:
    """Return a list of problems. Empty means the row is usable."""
    problems = []
    messages = ex.get("messages")
    meta = ex.get("meta")
    if not isinstance(messages, list) or not isinstance(meta, dict):
        return ["missing messages or meta"]
    role_err = check_roles(messages)
    if role_err:
        problems.append(role_err)
    cat = meta.get("category")
    ident = meta.get("id")
    data = load()
    item = data["by_key"].get((cat, ident))
    if item is None:
        problems.append(f"meta id {cat}/{ident} is not a skinny-v1 construct or persona")
    alias_input = meta.get("alias_input")
    if alias_input:
        hits = data["alias"].get(str(alias_input).lower(), [])
        if (cat, ident) not in hits:
            problems.append("alias_input does not resolve to meta.id")
        if str(alias_input).lower() == str(ident).lower():
            problems.append("alias_input repeats the canonical id")
    if meta.get("taxonomy") != "skinny-v1":
        problems.append("taxonomy is not skinny-v1")
    pattern = meta.get("pattern")
    if pattern not in {"single", "multi", "switch", "blend", "stay"}:
        problems.append("bad pattern")
    if pattern == "switch":
        sw = meta.get("switch")
        if not isinstance(sw, dict) or sw.get("to") != ident or "from" not in sw:
            problems.append("switch meta does not land on this id")
    elif meta.get("switch") is not None:
        problems.append("switch must be null unless pattern is switch")
    if pattern == "blend":
        blend = meta.get("blend")
        if not isinstance(blend, list) or ident not in blend:
            problems.append("blend must list this id")
    elif meta.get("blend") is not None:
        problems.append("blend must be null unless pattern is blend")

    involved = {ident}
    if isinstance(meta.get("switch"), dict):
        involved.add(meta["switch"].get("from"))
        involved.add(meta["switch"].get("to"))
    if isinstance(meta.get("blend"), list):
        involved.update(meta["blend"])
    # Only the row's own ordinary ids are banned in the user text. Handles
    # and proper names are banned everywhere.
    user_bits = []
    asst_bits = []
    for msg in messages:
        if msg.get("role") == "user":
            user_bits.append(msg.get("content") or "")
        elif msg.get("role") == "assistant":
            asst_bits.append(msg.get("content") or "")
    nsfw = bool(meta.get("nsfw"))
    blob_user = "\n".join(user_bits)
    problems.extend(f"user:{h}" for h in leak_hits(blob_user, involved))
    problems.extend(f"safety:{h}" for h in safety_hits(blob_user, nsfw))
    saw_think = False
    assistant_i = 0
    for content in asst_bits:
        think, visible = split_think(content)
        if think is not None:
            saw_think = True
            if "<think>" in think or "</think>" in visible or "<think>" in visible:
                problems.append("malformed think")
            frame = meta.get("frame") or {}
            if pattern == "switch" and assistant_i == 0 and isinstance(meta.get("switch"), dict):
                tag_ok = opening_tag_ok(think, meta["switch"])
            else:
                tag_ok = frame_tag_ok(think, frame)
            if not tag_ok:
                problems.append("frame tag mismatch")
            think_body = "\n".join(ln for ln in think.split("\n") if not ln.startswith("[frame:"))
            problems.extend(f"think:{h}" for h in leak_hits(think_body, ()))
            problems.extend(f"safety:{h}" for h in safety_hits(think, nsfw))
        elif content.lstrip().startswith("<think>"):
            problems.append("think block is not well formed")
        problems.extend(f"assistant:{h}" for h in leak_hits(visible if think is not None else content, ()))
        problems.extend(f"safety:{h}" for h in safety_hits(visible if think is not None else content, nsfw))
        if re.search(r"\b(as an ai|language model|certainly!|great question)\b", (visible if think is not None else content), re.I):
            problems.append("canned assistant voice")
        assistant_i += 1
    if meta.get("think") is True and not saw_think:
        problems.append("meta.think is true but no think block")
    if meta.get("think") is False and saw_think:
        problems.append("meta.think is false but a think block is present")
    frame = meta.get("frame") or {}
    if not isinstance(frame, dict):
        problems.append("frame missing")
    else:
        if frame.get("channel") != "reasoning":
            problems.append("frame.channel")
        if frame.get("identity") != "none" or frame.get("theme") != "none":
            problems.append("frame identity/theme")
        if frame.get("thinking_effort") not in {"low", "high"}:
            problems.append("frame.thinking_effort")
        if cat == "construct" and frame.get("construct") != ident:
            problems.append("frame.construct does not match id")
        if cat == "persona" and frame.get("persona") != ident:
            problems.append("frame.persona does not match id")
        agi = frame.get("agi")
        if agi is not None and not str(agi).startswith("agi-"):
            problems.append("frame.agi")
    return problems


def normalize(text: str) -> str:
    text = visible_text(text)
    text = text.lower()
    text = re.sub(r"\s+", " ", text).strip()
    return text


def example_fingerprint(ex: dict) -> str:
    parts = []
    for msg in ex["messages"]:
        if msg["role"] == "system":
            continue
        parts.append(msg["role"] + ":" + normalize(msg["content"]))
    return hashlib.sha1("\n".join(parts).encode()).hexdigest()


def shingles(text: str, k: int = 3) -> list[str]:
    words = re.findall(r"[a-z0-9']+", normalize(text))
    if len(words) < k:
        return [" ".join(words)] if words else []
    return [" ".join(words[i:i + k]) for i in range(len(words) - k + 1)]


def fnv(seed: int, text: str) -> int:
    x = (2166136261 ^ (seed * 16777619)) & 0xFFFFFFFF
    for ch in text:
        x ^= ord(ch)
        x = (x * 16777619) & 0xFFFFFFFF
    return x


def signature(text: str, n: int = 32) -> tuple[int, ...]:
    grams = shingles(text)
    if not grams:
        return tuple(0 for _ in range(n))
    out = []
    for i in range(n):
        best = 0xFFFFFFFF
        for gram in grams:
            h = fnv(i + 1, gram)
            if h < best:
                best = h
        out.append(best)
    return tuple(out)


def est_jaccard(a: tuple[int, ...], b: tuple[int, ...]) -> float:
    if not a:
        return 0.0
    return sum(x == y for x, y in zip(a, b)) / len(a)


class NearDup:
    """Banded minhash. Rejects estimated Jaccard >= threshold, confirmed exactly."""

    def __init__(self, threshold: float = 0.84, bands: int = 8):
        self.threshold = threshold
        self.bands = bands
        self.rows = 32 // bands
        self.buckets: list[dict] = [dict() for _ in range(bands)]
        self.seen: list[tuple[tuple[int, ...], set[str]]] = []
        self.exact: set[str] = set()

    def add_fingerprint(self, fp: str):
        self.exact.add(fp)

    def _band_keys(self, sig: tuple[int, ...]):
        for b in range(self.bands):
            chunk = sig[b * self.rows:(b + 1) * self.rows]
            yield b, chunk

    def too_close(self, text: str, fp: str) -> bool:
        if fp in self.exact:
            return True
        sig = signature(text)
        grams = set(shingles(text))
        cands = set()
        for b, chunk in self._band_keys(sig):
            cands.update(self.buckets[b].get(chunk, ()))
        for idx in cands:
            other_sig, other_grams = self.seen[idx]
            if est_jaccard(sig, other_sig) < self.threshold:
                continue
            if not grams or not other_grams:
                continue
            inter = len(grams & other_grams)
            union = len(grams | other_grams)
            if union and inter / union >= self.threshold:
                return True
        return False

    def add(self, text: str, fp: str):
        sig = signature(text)
        grams = set(shingles(text))
        idx = len(self.seen)
        self.seen.append((sig, grams))
        self.exact.add(fp)
        for b, chunk in self._band_keys(sig):
            self.buckets[b].setdefault(chunk, []).append(idx)

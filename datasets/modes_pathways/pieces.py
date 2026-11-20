"""Hand-authored situations. Numbers are computed here so the answer matches."""
from __future__ import annotations

import random

NAMES = (
    "Asha", "Ben", "Chris", "Diego", "Elena", "Farah", "Gus", "Hana",
    "Idris", "June", "Kenji", "Lila", "Moss", "Noor", "Omar", "Priya",
    "Quinn", "Rae", "Sofia", "Theo",
)
PLACES = (
    "Lisbon", "Oslo", "Kyoto", "Recife", "Hobart", "Tunis", "Bergen",
    "Pune", "Halifax", "Oaxaca", "Glasgow", "Busan",
)
HOURS = ("7", "8", "9", "6:30", "10")


def _piece(**kwargs) -> dict:
    base = {
        "history": [],
        "user": "",
        "lead": "",
        "detail": "",
        "code": None,
        "checks": [],
        "edges": [],
        "alts": [],
        "questions": [],
        "boundaries": [],
        "contract": None,
        "sections": None,
        "loop_lines": None,
        "family": "chat",
        "mood": None,
    }
    base.update(kwargs)
    return base


def _exec_ok(src: str, name: str, args: tuple, expected) -> None:
    ns: dict = {}
    exec(src, ns, ns)
    got = ns[name](*args)
    if got != expected:
        raise RuntimeError(f"{name}{args} -> {got!r}, expected {expected!r}")


def piece_for(family: str, rng: random.Random) -> dict:
    return FAMILY[family](rng)


def chat(rng: random.Random) -> dict:
    name = rng.choice(NAMES)
    place = rng.choice(PLACES)
    hour = rng.choice(HOURS)
    kind = rng.randrange(8)
    if kind == 0:
        user = (
            f"My neighbor's kid bounces a basketball at {hour}am against the shared wall. "
            f"Draft a text I can send {name} that asks for a later start without turning it into a feud."
        )
        lead = (
            f"Hey {name}, the ball against the wall carries straight into our kitchen, especially around {hour}. "
            f"Could you start after 9? Happy to keep the hallway bin in if that helps."
        )
        detail = "One request, one small trade, no speech about parenting."
        checks = [f"The noise is at {hour}, the ask is 9, the offer is the hallway bin.", lead]
    elif kind == 1:
        user = (
            f"I owe {name} twenty dollars and I keep forgetting. Write a two-line message that pays them back "
            f"in spirit even if the transfer goes out tomorrow, and that doesn't grovel."
        )
        lead = (
            f"Transferring the twenty tomorrow morning, {name}. Sorry it's late. "
            f"I'll send the screenshot when it clears."
        )
        detail = "Tomorrow morning, twenty dollars, a screenshot when it clears."
        checks = ["The debt is twenty, the send is tomorrow, and the note doesn't grovel.", lead]
    elif kind == 2:
        user = (
            f"We're eight people, one oven, and a Tuesday dinner in {place}. "
            f"Give me a menu that is one tray plus a salad, vegetarian, and not a project."
        )
        lead = "Sheet-pan chickpeas and peppers, rice from the cooker, and a lemon-cucumber salad."
        detail = "One tray, the rice doesn't need the oven, and the salad is cold."
        checks = [f"Eight people, one oven, Tuesday, {place}, vegetarian.", lead]
    elif kind == 3:
        user = (
            f"Write the note I tape to the office fridge. People keep taking {name}'s labeled lunches. "
            f"Firm, not a manifesto."
        )
        lead = (
            f"If it has a name on it, it isn't spare. {name}'s container stays {name}'s. "
            f"Unlabeled leftovers on the bottom shelf are fair game until Friday."
        )
        detail = "Named food stays put. The bottom shelf is the only free pile, and only until Friday."
        checks = [f"The note is about {name}'s labeled lunches, not a general speech.", lead]
    elif kind == 4:
        user = f"I have 40 minutes in {place} between trains. I want a walk, not a museum. Where do I point my feet?"
        lead = (
            f"Leave the station, walk twenty minutes toward the water or the market, buy one thing to eat, "
            f"and turn around. Forty minutes dies if you sit down for a meal."
        )
        detail = "Out and back. Sitting down for a meal spends the train."
        checks = [f"Forty minutes in {place}, a walk, not a museum.", lead]
    elif kind == 5:
        user = (
            f"Help me decline {name}'s weekend trip. I like them. I don't have the money or the weekend. "
            f"Don't invent a fake illness."
        )
        lead = (
            f"I can't do the weekend, {name}. Money's tight and I already promised Saturday at home. "
            f"Ask me on the next one that isn't a whole weekend."
        )
        detail = "Real reason, no invented illness, and the next shorter trip stays open."
        checks = [f"Declining {name} without a fake excuse.", lead]
    elif kind == 6:
        user = f"My plant in the {place} apartment has yellow lower leaves and wet soil. What do I do this week, in order?"
        lead = "Stop watering. Tip the pot and let it drain. Pull the yellow leaves. Water only when the top inch is dry."
        detail = "Wet soil and yellow lower leaves means too much water. No fertilizer this week."
        checks = ["Yellow lower leaves plus wet soil is overwatering until a drier week says otherwise.", lead]
    else:
        user = (
            f"{name} asked me to introduce them to my old boss in {place}. I barely know either of them now. "
            f"Write the intro email, short, and don't oversell."
        )
        lead = (
            f"Subject: {name}, who asked me to connect you two\n\n"
            f"You both work around the same kind of operations mess. {name} asked for an introduction, "
            f"so here it is. I'll leave the thread to you."
        )
        detail = "Short intro, no invented job title, and then get out of the thread."
        checks = [f"Introducing {name} in {place} without overselling.", lead]
    return _piece(
        family="chat",
        user=user,
        lead=lead,
        detail=detail,
        checks=checks,
        edges=["A moral or a fake credential makes the note worse."],
        alts=["A longer essay about the relationship. They asked for the note."],
    )


def hotpot(rng: random.Random) -> dict:
    place = rng.choice(PLACES)
    guests = rng.randint(12, 80)
    per = rng.choice((4, 5, 6, 8))
    bottles = (guests * 2 + per - 1) // per
    miles = rng.randint(2, 15)
    km = round(miles * 1.60934, 1)
    user = (
        f"Two quick ones. How many bottles if {guests} people get two glasses and a bottle is {per} glasses, "
        f"and how many kilometers is {miles} miles, roughly, for a sign in {place}?"
    )
    lead = f"{bottles} bottles, and {miles} miles is about {km} km."
    return _piece(
        family="hotpot",
        user=user,
        lead=lead,
        detail=f"{guests} × 2 = {guests * 2} glasses, divided by {per}, rounded up. {miles} × 1.60934 = {km}.",
        checks=[
            f"{guests} people × 2 glasses = {guests * 2}.",
            f"{guests * 2} / {per} rounds up to {bottles} bottles.",
            f"{miles} × 1.60934 = {km}, so the sign can say about {km} km.",
        ],
        edges=["If someone spills a glass you are short only if you bought the exact unrounded count."],
        alts=["Buy one extra bottle. Not asked."],
    )


def skim(rng: random.Random) -> dict:
    name = rng.choice(NAMES)
    place = rng.choice(PLACES)
    budget = rng.choice((800, 1200, 1500))
    day = rng.choice(("Tuesday", "Thursday"))
    passage = (
        f"{name} wrote: We looked at three rooms in {place}. The harbor one is {budget + 400} and smells like paint. "
        f"The courtyard one is {budget - 100} but the desk doesn't fit. The hill one is {budget}, empty from {day}, "
        f"and the landlord wants a two-month deposit plus a reference. I told them I'd answer Friday. "
        f"Also the train from the hill takes 28 minutes and the courtyard is a 6 minute walk. "
        f"Don't book the harbor, the paint job isn't finished until next month."
    )
    user = f"Gist only, two lines.\n\n{passage}"
    lead = (
        f"Take the hill room at {budget}: it's empty {day}, deposit is two months plus a reference, answer Friday. "
        f"Skip the harbor until the paint is done, and the courtyard desk doesn't fit."
    )
    return _piece(
        family="skim",
        user=user,
        lead=lead,
        detail="Hill room is the one still in play. Harbor paint and the courtyard desk take the other two out.",
        checks=[
            f"Hill room is {budget}, empty {day}, two-month deposit, reference, answer Friday.",
            "Harbor is unfinished paint until next month, so it is out.",
            "Courtyard is cheaper and the desk does not fit, so it is out.",
        ],
        edges=["The commute times are color, not the decision."],
        alts=["A full rewrite of the note. They asked for the gist."],
    )


def vibe(rng: random.Random) -> dict:
    name = rng.choice(NAMES)
    place = rng.choice(PLACES)
    if rng.randrange(2) == 0:
        user = (
            f"exhausted. {name} moved the {place} review again. "
            f"i just need a one-line reply that isn't sunny."
        )
        lead = f"Fine. Send me the new {place} time. I'm not rearranging Thursday twice."
        detail = f"The {place} review can move. Thursday doesn't."
        mood = "clipped"
    else:
        user = (
            f"ok THIS is actually fun, {name} saved us a corner table and there is cake?? "
            f"help me answer like a person who is delighted and not a press release."
        )
        lead = (
            f"Corner table AND cake in {place} is illegal, I'm in. "
            f"Tell {name} I'm bringing the awful playlist."
        )
        detail = f"Cake, the {place} table, and a bad playlist."
        mood = "warm"
    return _piece(
        family="vibe",
        user=user,
        lead=lead,
        detail=detail,
        mood=mood,
        checks=[detail, "Do not comment on their tone. Just answer in it.", lead],
        edges=["A cheerful reply to the exhausted note would be the miss."],
        alts=["A coaching paragraph. Not what they asked to send."],
    )


def banter(rng: random.Random) -> dict:
    topic = rng.choice(
        (
            "a meeting that could have been a sentence",
            "a smart fridge that sends emails",
            "a five-step app to remember to drink water",
            "putting blockchain on a library card",
            "an AI toaster with a personality",
        )
    )
    name = rng.choice(NAMES)
    place = rng.choice(PLACES)
    user = (
        f"{name} in {place} wants to pitch {topic}. "
        f"Roast the idea. One tight pass, then stop. The idea, not {name}."
    )
    punches = {
        "a meeting that could have been a sentence": "You gathered six people to watch a sentence grow up in public.",
        "a smart fridge that sends emails": "The lettuce has a mailbox now. The lettuce is not going to reply.",
        "a five-step app to remember to drink water": "Step six is opening the tap, which the app will explain in a webinar.",
        "putting blockchain on a library card": "Your overdue fine now needs consensus and a gas fee. The book is still late.",
        "an AI toaster with a personality": "It burns the bread and then wants to talk about its journey.",
    }
    lead = punches[topic] + f" Tell {name} the {place} pitch can stay in the drafts."
    return _piece(
        family="banter",
        user=user,
        lead=lead,
        detail="Then stop.",
        checks=["The target is the idea.", "Stop after the punchline.", lead],
        edges=["A second paragraph explains the joke and kills it."],
        alts=["A product requirements doc. Wrong room."],
    )


def react(rng: random.Random) -> dict:
    place = rng.choice(PLACES)
    name = rng.choice(NAMES)
    user = (
        f"Scene already moving: rain on the platform in {place}, last train gone, {name} still holding two coffees. "
        f"Give the next beat in dialogue and one action. No backstory."
    )
    lead = (
        f"{name} held out the second cup like it was an apology. \"We can wait for the bus or we can admit we're walking.\"\n"
        f"The platform clock stuck on the minute the train left."
    )
    return _piece(
        family="react",
        user=user,
        lead=lead,
        detail="The second cup is still in their hand, and the clock is stuck.",
        checks=["Two coffees and a missed train are the whole scene.", "No childhood, no lore.", lead],
        edges=["A paragraph of weather essay stalls the beat."],
        alts=["Restart the scene from morning. They said it's already moving."],
    )


def pattern(rng: random.Random) -> dict:
    bugs = [
        (
            "for i in range(len(items)):\n    if items[i] == items[i+1]:\n        dup = i",
            "for (let i = 0; i < rows.length; i++) {\n  if (rows[i].id === rows[i+1].id) mark(i);\n}",
            "i = 0\nwhile nums[i] <= nums[i+1]:\n    i += 1",
            "Each loop reads the next neighbor and walks off the end on the last element.",
        ),
        (
            "if user:\n    name = user.name\nelse:\n    name = user.email",
            "value = data.get('qty')\nif value:\n    total += value\nelse:\n    total += data['qty']",
            "node = find(key)\nif node is None:\n    return node.value",
            "The failure branch uses the same object it just proved was missing.",
        ),
    ]
    a, b, c, shared = bugs[rng.randrange(len(bugs))]
    ticket = rng.randint(100, 999)
    user = (
        f"These three broke in files under batch {ticket}. What's the shared shape?\n\n"
        f"1.\n{a}\n\n2.\n{b}\n\n3.\n{c}"
    )
    return _piece(
        family="pattern",
        user=user,
        lead=f"Batch {ticket}: {shared}",
        detail="Same access, three languages. Guard it before you touch the neighbor.",
        checks=[shared, "The language changes and the mistake doesn't.", "A fix is a guard before the access, not a new architecture."],
        edges=["If the collection is empty the same access still fails."],
        alts=["Three separate root-cause essays. They asked for the shared shape."],
    )


def complete(rng: random.Random) -> dict:
    nums_sorted = sorted(rng.sample(range(1, 20), k=4))
    target = nums_sorted[0] + nums_sorted[-1]
    user = (
        "Finish the function. The list is sorted. Don't restate the part I already wrote.\n\n"
        "def pair_ends(nums, target):\n"
        "    lo, hi = 0, len(nums) - 1\n"
        "    while lo < hi:\n"
        "        s = nums[lo] + nums[hi]\n"
        "        # finish\n"
    )
    src = (
        "def pair_ends(nums, target):\n"
        "    lo, hi = 0, len(nums) - 1\n"
        "    while lo < hi:\n"
        "        s = nums[lo] + nums[hi]\n"
        "        if s == target:\n"
        "            return lo, hi\n"
        "        if s < target:\n"
        "            lo += 1\n"
        "        else:\n"
        "            hi -= 1\n"
        "    return -1, -1\n"
    )
    ns: dict = {}
    exec(src, ns, ns)
    got = ns["pair_ends"](nums_sorted, target)
    _exec_ok(src, "pair_ends", (nums_sorted, target), got)
    lead = (
        "        if s == target:\n"
        "            return lo, hi\n"
        "        if s < target:\n"
        "            lo += 1\n"
        "        else:\n"
        "            hi -= 1\n"
        "    return -1, -1"
    )
    return _piece(
        family="complete",
        user=user,
        lead=lead,
        detail=f"On {nums_sorted} looking for {target}, that returns {got}. The list has to be sorted or the walk is nonsense.",
        code=src,
        checks=[
            "Equal returns the two indexes, low side moves when the sum is short, high side moves when it's long, miss returns -1, -1.",
            f"Sorted check {nums_sorted} target {target} -> {got}.",
            "Unsorted input is outside the contract. Say so once.",
        ],
        edges=["Empty list: lo < hi is false, returns -1, -1.", "One element: same."],
        alts=["Rewrite it as a hash map. They asked to finish this loop."],
    )


def stream(rng: random.Random) -> dict:
    name = rng.choice(NAMES)
    place = rng.choice(PLACES)
    room = rng.choice(("the harbor room", "warehouse 4", "the late show", "a Tuesday slot"))
    user = (
        f"I'm live in {place}, {room}, bass just dropped, {name} is in the chat yelling the title. "
        f"Two lines into the mic, then I have to play."
    )
    lead = f"That's {name} calling the title and they're right. Stay for the next one, I'm not talking over {room}."
    return _piece(
        family="stream",
        user=user,
        lead=lead,
        detail="Then play.",
        checks=["They are live. Latency beats completeness.", lead],
        edges=["A third sentence is dead air."],
        alts=["A produced monologue. Wrong clock."],
    )


def recall(rng: random.Random) -> dict:
    name = rng.choice(NAMES)
    budget = rng.choice((25, 40, 60))
    day = rng.choice(("Tuesday", "Thursday", "Sunday"))
    ban = rng.choice(("peanuts", "shellfish", "gluten"))
    history = [
        {
            "user": f"Constraints for the picnic: budget {budget} dollars, {day} only, nobody eats {ban}. That's the whole brief.",
            "answer": f"Got it. {budget} dollars, {day}, no {ban}.",
            "mode": "chat",
            "pathway": "s1",
            "construct": "omni",
            "effort": "low",
        }
    ]
    user = f"So what should {name} actually pack?"
    if ban == "peanuts":
        food = "rice balls, apples, and a brick of cheddar"
    elif ban == "shellfish":
        food = "egg sandwiches and citrus, nothing from the fish counter"
    else:
        food = "rice, roasted vegetables, and yogurt"
    lead = f"Pack {food}. It fits {budget} dollars, it can sit until {day}, and it doesn't bring {ban}."
    return _piece(
        family="recall",
        history=history,
        user=user,
        lead=lead,
        detail=f"{budget} dollars, {day}, no {ban}. The pack list has to obey all three.",
        checks=[
            f"Budget is {budget}, day is {day}, banned food is {ban}.",
            lead,
            "If the pack list ignores one of the three, it failed the turn.",
        ],
        edges=[f"A snack that 'only has a little {ban}' still fails."],
        alts=["A new menu that needs a stove. They are packing, not cooking a project."],
    )


def solve(rng: random.Random) -> dict:
    kind = rng.randrange(6)
    if kind == 0:
        guests = rng.randint(20, 180)
        glasses = rng.randint(1, 4)
        per = rng.randint(4, 8)
        need = guests * glasses
        bottles = (need + per - 1) // per
        user = (
            f"{guests} guests, {glasses} glasses each, {per} glasses in a bottle. "
            f"How many bottles do I buy so we don't run out?"
        )
        lead = f"Buy {bottles}."
        checks = [
            f"{guests} × {glasses} = {need} glasses.",
            f"{need} ÷ {per} = {need / per:.3f}, and the remainder means you round up.",
            f"{bottles} × {per} = {bottles * per}, which covers {need} with {bottles * per - need} left.",
        ]
        detail = checks[0]
    elif kind == 1:
        out_km = rng.randint(40, 320)
        back_km = out_km
        v1 = rng.randint(30, 90)
        v2 = rng.randint(25, 80)
        if v1 == v2:
            v2 = v1 - 5
        hours = out_km / v1 + back_km / v2
        dist = out_km + back_km
        avg = round(dist / hours, 2)
        user = (
            f"Out {out_km} km at {v1} km/h and back {back_km} km at {v2} km/h. "
            f"What's the average speed for the round trip? Not the average of the two speeds."
        )
        lead = f"{avg} km/h."
        checks = [
            f"Time out = {out_km}/{v1} = {out_km / v1:.3f} h. Time back = {back_km}/{v2} = {back_km / v2:.3f} h.",
            f"Total time = {hours:.3f} h for {dist} km.",
            f"Average = {dist} / {hours:.3f} = {avg}. The mean of {v1} and {v2} is {(v1+v2)/2}, and that is the trap.",
        ]
        detail = "Harmonic, because the two legs take different times."
    elif kind == 2:
        price = rng.randint(40, 320)
        down = rng.choice((10, 15, 20, 25, 30))
        up = rng.choice((10, 15, 20, 25, 30))
        after = price * (100 - down) / 100
        final = after * (100 + up) / 100
        user = f"A jacket is {price}. It drops {down}%, then the sale price rises {up}%. What's the final price?"
        lead = f"{final:.0f}." if float(final).is_integer() else f"{final:.2f}."
        checks = [
            f"After the drop: {price} × {100-down}/100 = {after:.2f}.",
            f"After the rise: {after:.2f} × {100+up}/100 = {final:.2f}.",
            (
                f"It does not return to {price}. Percent changes don't cancel."
                if abs(final - price) > 1e-6
                else f"These two percents happen to land back on {price}. That is not the usual case."
            ),
        ]
        detail = checks[2]
    elif kind == 3:
        gap = rng.randint(4, 80)
        user = f"A fence runs {gap} meters and needs a post every meter, including both ends. How many posts?"
        posts = gap + 1
        lead = f"{posts} posts."
        checks = [
            f"{gap} gaps of 1 meter need {posts} posts, because both ends get one.",
            f"Check: {posts - 1} intervals × 1 m = {gap} m.",
            "The off-by-one is counting gaps and calling them posts.",
        ]
        detail = "Posts = gaps + 1 when both ends are included."
    elif kind == 4:
        a = rng.randint(2, 12)
        b = rng.randint(2, 12)
        user = (
            f"Printer A finishes the stack in {a} hours, printer B in {b} hours. "
            f"How long if they run together?"
        )
        hours = 1 / (1 / a + 1 / b)
        lead = f"{hours:.2f} hours."
        checks = [
            f"A's rate is 1/{a} of the stack per hour. B's rate is 1/{b}.",
            f"Together: {(1/a + 1/b):.4f} stacks per hour.",
            f"Time = 1 / that = {hours:.2f} hours.",
        ]
        detail = "Add rates, then invert. Don't average the hours."
    else:
        fixed = rng.randint(80, 900)
        var = rng.randint(2, 15)
        price = var + rng.randint(2, 20)
        # fixed + var*n = price*n => n = fixed / (price-var)
        unit_margin = price - var
        n = fixed / unit_margin
        user = (
            f"Fixed cost {fixed}, variable {var} per unit, sell price {price}. "
            f"How many units to break even?"
        )
        lead = f"{n:.0f} units." if float(n).is_integer() else f"{n:.2f} units."
        checks = [
            f"Margin per unit = {price} - {var} = {unit_margin}.",
            f"Break-even = {fixed} / {unit_margin} = {n:.2f}.",
            f"Check: cost {fixed} + {var}×{n:.2f} = {fixed + var * n:.2f}, revenue {price}×{n:.2f} = {price * n:.2f}.",
        ]
        detail = "Cover the fixed cost with the per-unit margin."
    return _piece(
        family="solve",
        user=user,
        lead=lead,
        detail=detail,
        checks=checks,
        edges=["A zero or empty case isn't in this problem. Don't invent one in the answer."],
        alts=["Quote a formula and skip the arithmetic. That's how the trap answer survives."],
        boundaries=["Zero guests would be zero bottles, but that isn't the question."],
    )


def _src_first_cross() -> str:
    return (
        "def first_cross(nums, target):\n"
        "    total = 0\n"
        "    for i, n in enumerate(nums):\n"
        "        total += n\n"
        "        if total >= target:\n"
        "            return i\n"
        "    return -1\n"
    )


def _src_bsearch() -> str:
    return (
        "def binary_search(nums, target):\n"
        "    lo, hi = 0, len(nums)\n"
        "    while lo < hi:\n"
        "        mid = (lo + hi) // 2\n"
        "        if nums[mid] < target:\n"
        "            lo = mid + 1\n"
        "        else:\n"
        "            hi = mid\n"
        "    if lo < len(nums) and nums[lo] == target:\n"
        "        return lo\n"
        "    return -1\n"
    )


def _src_ipv4() -> str:
    return (
        "def valid_ipv4(text):\n"
        "    parts = text.split('.')\n"
        "    if len(parts) != 4:\n"
        "        return False\n"
        "    for part in parts:\n"
        "        if not part.isdigit():\n"
        "            return False\n"
        "        if len(part) > 1 and part.startswith('0'):\n"
        "            return False\n"
        "        if int(part) > 255:\n"
        "            return False\n"
        "    return True\n"
    )


def _src_merge() -> str:
    return (
        "def merge_intervals(spans):\n"
        "    if not spans:\n"
        "        return []\n"
        "    ordered = sorted(spans)\n"
        "    out = [list(ordered[0])]\n"
        "    for start, end in ordered[1:]:\n"
        "        if start <= out[-1][1]:\n"
        "            out[-1][1] = max(out[-1][1], end)\n"
        "        else:\n"
        "            out.append([start, end])\n"
        "    return out\n"
    )


def _src_unique() -> str:
    return (
        "def stable_unique(items):\n"
        "    seen = set()\n"
        "    out = []\n"
        "    for item in items:\n"
        "        if item not in seen:\n"
        "            seen.add(item)\n"
        "            out.append(item)\n"
        "    return out\n"
    )


def _src_balanced() -> str:
    return (
        "def balanced(text):\n"
        "    pair = {')': '(', ']': '[', '}': '{'}\n"
        "    stack = []\n"
        "    for ch in text:\n"
        "        if ch in '([{':\n"
        "            stack.append(ch)\n"
        "        elif ch in pair:\n"
        "            if not stack or stack.pop() != pair[ch]:\n"
        "                return False\n"
        "    return not stack\n"
    )


def code(rng: random.Random) -> dict:
    kind = rng.randrange(6)
    if kind == 0:
        nums = [rng.randint(5, 40) for _ in range(rng.randint(4, 6))]
        target = rng.randint(20, 90)
        src = _src_first_cross()
        ns: dict = {}
        exec(src, ns, ns)
        got = ns["first_cross"](nums, target)
        walk = []
        total = 0
        for i, n in enumerate(nums):
            total += n
            walk.append(f"{total} at {i}")
            if total >= target:
                break
        user = (
            f"Python function. First index where the running sum of {nums} reaches {target}. "
            f"If it never does, return -1. Empty input returns -1."
        )
        lead = f"Index {got}."
        checks = [
            "Inclusive running sum, first index at or past the target, empty and never-cross both return -1.",
            "Walk: " + ", ".join(walk) + f". Result {got}.",
            f"Empty check: first_cross([], {target}) == -1.",
        ]
        _exec_ok(src, "first_cross", ([], target), -1)
        detail = "One pass, no extra list."
        edges = ["All values below the target returns -1.", "A first element already past the target returns 0."]
    elif kind == 1:
        nums = sorted(rng.sample(range(1, 40), k=6))
        target = nums[rng.randrange(len(nums))]
        src = _src_bsearch()
        ns = {}
        exec(src, ns, ns)
        got = ns["binary_search"](nums, target)
        missing = target + 100
        miss = ns["binary_search"](nums, missing)
        user = (
            f"Binary search on a sorted list. Return the index of {target} in {nums}, "
            f"or -1 if it isn't there. Duplicates aren't in this list."
        )
        lead = f"Index {got}. A missing value such as {missing} returns {miss}."
        checks = [
            "Half-open [lo, hi). Mid goes to the right half only when nums[mid] is strictly below the target.",
            f"{nums} contains {target} at {got}.",
            f"{missing} is absent -> {miss}.",
        ]
        detail = "Iterative, no recursion, no slicing copies."
        edges = ["Empty list returns -1.", "Target smaller than every element returns -1."]
        _exec_ok(src, "binary_search", ([], target), -1)
    elif kind == 2:
        good = ".".join(str(rng.randint(1, 254)) for _ in range(4))
        bad = f"01.{rng.randint(0,255)}.{rng.randint(0,255)}.1"
        src = _src_ipv4()
        ns = {}
        exec(src, ns, ns)
        user = (
            f"Validate an IPv4 string. Four decimal octets, 0-255, no leading zeros. "
            f"'{good}' should pass and '{bad}' should fail."
        )
        lead = f"'{good}' is valid. '{bad}' is not, because of the leading zero."
        checks = [
            f"valid_ipv4({good!r}) is {ns['valid_ipv4'](good)}.",
            f"valid_ipv4({bad!r}) is {ns['valid_ipv4'](bad)}.",
            "Split on dots, reject the wrong count, reject non-digits, reject leading zeros, reject >255.",
        ]
        _exec_ok(src, "valid_ipv4", (good,), True)
        _exec_ok(src, "valid_ipv4", (bad,), False)
        detail = "String rules, not the socket library."
        edges = ["'1.2.3' is too short.", "'1.2.3.256' is out of range.", "'1.2.3.4.5' is too long."]
    elif kind == 3:
        spans = []
        start = 0
        for _ in range(4):
            a = start + rng.randint(0, 2)
            b = a + rng.randint(1, 3)
            spans.append([a, b])
            start = a + rng.randint(0, 3)
        src = _src_merge()
        ns = {}
        exec(src, ns, ns)
        merged = ns["merge_intervals"](spans)
        user = f"Merge overlapping intervals. Input {spans}. Touching endpoints count as overlap."
        lead = f"Merged: {merged}."
        checks = [
            "Sort by start, then extend the open interval when the next start is <= the open end.",
            f"Result of that walk is {merged}.",
            "Empty input returns [].",
        ]
        _exec_ok(src, "merge_intervals", ([],), [])
        detail = "Sort once. Don't compare every pair."
        edges = ["A span completely inside another disappears into the outer one.", "A gap of 1 stays split because the test is <= not < only when they touch. Touching merges."]
    elif kind == 4:
        alphabet = ["a", "b", "c", "d"]
        items = [rng.choice(alphabet) for _ in range(7)]
        src = _src_unique()
        ns = {}
        exec(src, ns, ns)
        got = ns["stable_unique"](items)
        user = f"Drop duplicates from {items} and keep the first occurrence's order."
        lead = f"{got}."
        checks = [
            "A set tracks membership. The list tracks order. Append only on the first sighting.",
            f"Walk of {items} yields {got}.",
            "Empty input returns [].",
        ]
        _exec_ok(src, "stable_unique", ([],), [])
        detail = "Stable means first-seen order, not sorted order."
        edges = ["All unique returns the same list.", "All identical returns a one-element list."]
    else:
        samples = ["()[]{}", "([)]", "{[()]}", "(", ""]
        src = _src_balanced()
        ns = {}
        exec(src, ns, ns)
        sample = rng.choice(samples)
        got = ns["balanced"](sample)
        user = (
            f"Check bracket balance for ()[]{{}}. '{sample}' is the example I care about. "
            f"Other characters aren't in these strings."
        )
        lead = f"'{sample}' -> {got}."
        checks = [
            "Push closers' matches. A closer with an empty stack or the wrong opener fails. Leftover openers fail.",
            f"balanced({sample!r}) is {got}.",
            "Empty string is balanced. A single opener is not.",
        ]
        _exec_ok(src, "balanced", ("",), True)
        _exec_ok(src, "balanced", ("(",), False)
        detail = "Stack, not a counter, because the kinds have to match."
        edges = ["']' fails immediately.", "'([)]' fails even though the counts match."]
    return _piece(
        family="code",
        user=user,
        lead=lead,
        detail=detail,
        code=src,
        checks=checks,
        edges=edges,
        alts=["Pull in a library for a ten-line loop. Not justified."],
        boundaries=edges,
    )


def build(rng: random.Random) -> dict:
    layers = rng.randint(8, 40)
    heads = rng.choice((2, 4, 8, 16))
    dim = rng.choice((32, 64, 80, 128))
    seq = rng.choice((512, 1024, 2048, 4096, 8192))
    byte = 2
    total = 2 * layers * heads * dim * seq * byte
    mib = total / (1024 * 1024)
    user = (
        f"I'm sizing a KV cache: {layers} layers, {heads} kv heads, head dim {dim}, "
        f"sequence {seq}, fp16. How many bytes for K and V together, and what blows up first if I double the sequence?"
    )
    lead = (
        f"{total} bytes, about {mib:.1f} MiB, for one sequence. "
        f"Doubling the sequence doubles the cache. The weights don't move."
    )
    detail = "Bytes = 2 tensors × layers × kv heads × head dim × tokens × 2 bytes."
    return _piece(
        family="build",
        user=user,
        lead=lead,
        detail=detail,
        checks=[
            f"2 × {layers} × {heads} × {dim} × {seq} × 2 = {total}.",
            f"{total} / 1024^2 = {mib:.1f} MiB.",
            "The cache is linear in sequence. Batch multiplies it again. Weights stay put.",
            "fp16 is 2 bytes. fp8 would halve this number and that is a different cache.",
        ],
        edges=["Batch 4 is four times this if every sequence is full.", "A prefix cache shared across beams is not in this number."],
        alts=["Quote a vendor's 'context window' as if it were the cache size. It isn't."],
        boundaries=["seq 0 is an empty cache, not a division by zero."],
    )


def logic(rng: random.Random) -> dict:
    name = rng.choice(NAMES)
    job = rng.choice(("night-shift porter", "dock clerk", "gallery guard", "night baker"))
    mark = rng.choice(("a red lanyard", "a yellow badge", "a numbered key", "a blue apron"))
    if rng.randrange(2) == 0:
        user = (
            f"All {job}s wear {mark}. {name} is a {job}. "
            f"So {name} wears {mark}. Is that valid, and where would it break?"
        )
        lead = f"Valid. {name} is inside the set the rule covers, so {mark} follows."
        checks = [
            f"Premise 1: if someone is a {job}, then they wear {mark}.",
            f"Premise 2: {name} is a {job}.",
            "Modus ponens. It breaks if the first premise has a quiet exception the user didn't state.",
        ]
        detail = "The form is valid. The world might still have an exception, and that exception isn't in the text."
        edges = [f"If {name} is not a {job}, premise 2 is false and the conclusion doesn't follow."]
    else:
        user = (
            f"All {job}s wear {mark}. {name} is wearing {mark}. "
            f"So {name} is a {job}. Is that valid?"
        )
        lead = f"Not valid. {mark.capitalize()} doesn't pin {name} to that job. Someone else can wear one."
        checks = [
            f"The rule only runs {job} -> {mark}.",
            f"Seeing {mark} and inferring the job affirms the consequent.",
            f"{name} might be a {job}. The argument doesn't show it.",
        ]
        detail = f"You'd need the other direction, or a premise that only a {job} wears {mark}."
        edges = [f"If a second premise says nobody else wears {mark}, then it would go through. That premise is absent."]
    return _piece(
        family="logic",
        user=user,
        lead=lead,
        detail=detail,
        checks=checks,
        edges=edges,
        alts=["Call it a fallacy by name and skip where the inference actually dies."],
    )


def plan(rng: random.Random) -> dict:
    name = rng.choice(NAMES)
    weeks = rng.randint(5, 14)
    people = rng.randint(2, 6)
    user = (
        f"{name} has {people} people and {weeks} weeks to split a tangled billing folder out of a monolith "
        f"without freezing feature work. Give me the plan you'd actually run."
    )
    lead = (
        f"Strangle it at the HTTP edge. New invoices go to a new service in week 1, "
        f"old reads stay put, and you don't split the database until the write path is quiet."
    )
    checks = [
        f"Constraint: {people} people, {weeks} weeks, features keep shipping.",
        "Option A, rewrite in place: feature freeze in disguise. Reject.",
        "Option B, shared database forever: you move the outage, not the coupling. Reject as the end state, fine as a week-2 bridge.",
        "Option C, edge strangle: one write boundary, old app proxies, database split last. This one fits the headcount.",
        f"Week 1 is the boundary and a contract test. Week 2-{weeks-2} is traffic shift. Last two weeks are the leftover reads and the rollback drill.",
    ]
    return _piece(
        family="plan",
        user=user,
        lead=lead,
        detail=f"{people} people cannot staff a rewrite and a feature queue. One boundary.",
        checks=checks,
        edges=["If billing is called from nine internal jobs, the HTTP strangle misses them. Inventory those calls in week 1 before you celebrate."],
        alts=["Big-bang cutover on a Friday. The rollback is a myth at this team size."],
    )


def research(rng: random.Random) -> dict:
    place = rng.choice(PLACES)
    user = (
        f"Three notes about the tap in our {place} office. Grade them and tell me whether to drink it.\n\n"
        f"1. Vendor blog: 'Our filter removes 99% of everything.' No method.\n"
        f"2. Last year's municipal report for the neighborhood: lead under the legal limit at the street main, sampled in March.\n"
        f"3. A sticky note from {rng.choice(NAMES)}: the tap tasted metallic on Monday after the pipes were shut for repairs.\n"
    )
    lead = (
        "Don't treat it as settled. The street main was fine last March, the vendor blog is an ad, "
        "and Monday's metallic taste is a reason to test this tap, not a lab result."
    )
    return _piece(
        family="research",
        user=user,
        lead=lead,
        detail="Grade only what was pasted. The municipal sample is the strongest and it is the wrong pipe and the wrong month.",
        checks=[
            "Vendor blog: grade D. A percent with no method is a claim, not evidence.",
            "Municipal report: grade B for the street main last March. It does not sample this building's tap after a shutdown.",
            "Sticky note: grade C as a symptom report. Metallic taste after a repair is a reason to test, not a measurement of lead.",
            "Consensus available from these three: nobody here has measured this tap.",
        ],
        edges=["A single good test of this tap would outrank all three notes."],
        alts=["Declare it safe because the city was under the limit somewhere else."],
    )


def brainstorm(rng: random.Random) -> dict:
    place = rng.choice(PLACES)
    owner = rng.choice(NAMES)
    late = rng.randint(3, 24)
    deposit = rng.choice((10, 15, 20, 25, 40))
    user = (
        f"{owner}'s tool library in {place} has {late} drills out past a week. "
        f"Give me three actually different fixes and pick one."
    )
    lead = (
        f"Pick a {deposit}-dollar hold. It beats a shaming poster and it beats buying a replacement "
        f"for those {late} drills {owner} will not see again."
    )
    return _piece(
        family="brainstorm",
        user=user,
        lead=lead,
        detail="Three mechanisms: money, reputation, and inventory. They are not three wordings of a reminder email.",
        checks=[
            "Reminder texts: cheap, and you already know they don't work or you wouldn't be asking.",
            "Public late list: it punishes the regulars who can read and misses the person who doesn't care.",
            "Card hold released on return: the drill has a price for being late, and you don't have to staff a feud.",
            "Pick the hold. It is the only one that changes the cost of not returning it.",
        ],
        edges=["If your borrowers don't have cards, the hold fails and you're back to a cash deposit."],
        alts=["GPS in every drill. The library's budget is the joke in that plan."],
        questions=["Would a 20 deposit change your own behavior? That's the test."],
    )


def teach(rng: random.Random) -> dict:
    name = rng.choice(NAMES)
    topics = (
        (
            f"{name} knows what a Python list is and doesn't know what happens when two keys land in the same hash bucket.",
            "A dict is a list of buckets. The hash picks the bucket. If two keys share a bucket, they sit together in a small chain, and lookup walks that chain checking equality.",
            "hash chooses the bucket, equality chooses the key inside it.",
            "If you only had equality, every lookup would scan the whole collection.",
        ),
        (
            f"{name} knows what a git commit is and doesn't know what a rebase does to commits that already exist.",
            "Rebase copies your commits onto a new base. The new commits have new ids. The old ones are still in the object store until nothing points at them.",
            "Rebase writes new commits. It does not edit the old ones in place.",
            "That's why rebasing a branch someone else pulled rewrites history they already have.",
        ),
        (
            f"{name} can write a SQL WHERE and doesn't know why an index isn't used when they wrap the column in a function.",
            "The index is sorted by the raw column. LOWER(email) is a different value, so the planner can't walk that sorted list unless you indexed the expression.",
            "A function on the column hides it from an index on the bare column.",
            "Index the expression, or compare without wrapping the column.",
        ),
    )
    question, idea, crisp, why = topics[rng.randrange(len(topics))]
    ticket = rng.randint(10, 80)
    user = f"Teach this, example size {ticket}. {question} One concrete picture, then stop."
    return _piece(
        family="teach",
        user=user,
        lead=crisp,
        detail=idea,
        checks=[
            f"They already know the prerequisite. Start at the gap: {question}",
            idea,
            why,
        ],
        edges=["A taxonomy of every related structure is how you lose them."],
        alts=["A definition copied from a glossary. They asked how it behaves."],
        questions=["Ask them to predict one case before you show the second."],
    )


def deep(rng: random.Random) -> dict:
    a = rng.randint(25, 80)
    b = a + rng.randint(8, 35)
    user = (
        f"Vendor A is {a}/seat/month, data stays in our VPC, and onboarding is a month. "
        f"Vendor B is {b}/seat/month, hosted by them, and we can turn it on Friday. "
        f"We have one security review slot this quarter. Which do I sign, and what would flip it?"
    )
    if a + 15 < b:
        lead = (
            f"Sign A. You're paying {b - a} a seat to skip a month, and the security review you already can't spare "
            f"is exactly the review B forces onto their hosting."
        )
        pick = "A"
    else:
        lead = (
            f"Sign B only if Friday revenue is worth more than the review slot. "
            f"Otherwise A is the one that doesn't spend the quarter's only security review on someone else's VPC."
        )
        pick = "B-conditional"
    return _piece(
        family="deep",
        user=user,
        lead=lead,
        detail=f"The scarce resource is the review slot, not the {b - a} dollars. Pick leans {pick}.",
        checks=[
            f"Price gap is {b - a} per seat per month.",
            "A spends a month and keeps the data in-VPC. B spends the security-review slot.",
            "One review slot this quarter means B's hosting is not free just because the invoice is the only number on the page.",
            lead,
        ],
        edges=["If legal already signed a standing review for B's host, the slot argument dies and Friday wins."],
        alts=["Average the prices and call it a wash. That ignores the constraint that actually binds."],
    )


def extreme(rng: random.Random) -> dict:
    piece = deep(rng)
    piece["family"] = "extreme"
    piece["user"] = piece["user"] + " Try to break your own recommendation before you commit."
    piece["checks"] = list(piece["checks"]) + [
        "Break attempt: if onboarding slips past the quarter, A's month becomes two and Friday-B wins on calendar alone.",
        "Break attempt: if seat count is under five, the price gap is noise next to the review slot, so the slot still dominates.",
        "I could not find a break that survives the single review slot. The recommendation stands, with the flip condition already named.",
    ]
    piece["edges"] = list(piece["edges"]) + ["A second vendor with in-VPC and a Friday switch would retire both options. There isn't one in the prompt."]
    return piece


def inhibit(rng: random.Random) -> dict:
    kind = rng.randrange(4)
    if kind == 0:
        more = rng.randint(1, 15) * 100
        extra = rng.choice((10, 20, 30, 40, 50, 60))
        total = more + extra
        ball = extra / 2
        bat = ball + more
        user = (
            f"A bat and a ball cost ${total/100:.2f}. The bat costs ${more/100:.2f} more than the ball. "
            f"How much is the ball?"
        )
        lead = f"The ball is ${ball/100:.2f}. The bat is ${bat/100:.2f}."
        checks = [
            f"The fast answer subtracts once and says ${(total-more)/100:.2f}. That double-counts the gap.",
            f"Let the ball be x. Bat is x+{more/100:.2f}. 2x+{more/100:.2f} = {total/100:.2f}. x = {ball/100:.2f}.",
            f"Check: {bat/100:.2f} + {ball/100:.2f} = {total/100:.2f}, and the difference is {more/100:.2f}.",
        ]
    elif kind == 1:
        day = rng.randint(8, 60)
        user = (
            f"A lily patch doubles every day and covers the pond on day {day}. "
            f"On which day is it half covered?"
        )
        lead = f"Day {day - 1}."
        checks = [
            f"The fast answer halves the day number and says day {day // 2}. Doubling doesn't work that way.",
            f"If day {day} is full and it doubles daily, day {day - 1} is the half.",
            f"Check: half on day {day - 1}, doubled, is full on day {day}.",
        ]
    elif kind == 2:
        price = rng.randint(40, 240)
        down = up = 20
        for _try in range(8):
            down = rng.choice((10, 15, 20, 25))
            up = rng.choice((10, 15, 20, 25))
            if (100 - down) * (100 + up) != 10000:
                break
        after = price * (100 - down) / 100
        final = after * (100 + up) / 100
        user = f"A price is {price}. It falls {down}%, then rises {up}%. Am I back to {price}?"
        lead = f"No. You land on {final:.2f}."
        checks = [
            "The fast answer says the percents cancel. They don't, because the rise applies to the reduced price.",
            f"{price} × {100-down}/100 = {after:.2f}. Then × {100+up}/100 = {final:.2f}.",
            f"You are {'short' if final < price else 'not back at the start'}: {price - final:.2f} away from {price}.",
        ]
    else:
        meters = rng.randint(4, 48)
        user = f"{meters} fence panels between posts, one post at each end of each panel, posts shared. How many posts?"
        lead = f"{meters + 1} posts, not {meters}."
        checks = [
            f"The fast answer counts {meters} posts because there are {meters} panels.",
            f"A line of {meters} panels has a post at both ends, so posts = panels + 1 = {meters + 1}.",
            f"Two panels need three posts. The pattern holds at {meters}.",
        ]
    return _piece(
        family="inhibit",
        user=user,
        lead=lead,
        detail=checks[1],
        checks=checks,
        edges=["If the wording had said the bat costs $1.00 exactly, not $1.00 more, the fast answer would be right. It says more."],
        alts=["Ship the intuitive number and add a disclaimer. That's the miss."],
    )


def escalate(rng: random.Random) -> dict:
    hour = rng.choice(HOURS)
    place = rng.choice(PLACES)
    fixed = rng.choice((24, 36, 40, 48, 60, 80))
    var = rng.choice((2, 3, 4, 5, 6))
    sell = var + rng.choice((2, 4, 5, 6, 8))
    n = fixed / (sell - var)
    user = (
        f"What time does the {place} reading room usually open, and also, "
        f"we sell the booklet for {sell}, variable cost {var}, fixed cost {fixed}. How many to break even?"
    )
    lead = (
        f"I don't know the reading room's hours from here, so I won't invent a clock time. "
        f"The booklet breaks even at {n:.0f} copies."
    )
    return _piece(
        family="escalate",
        user=user,
        lead=lead,
        detail=f"No invented opening time. Margin is {sell - var}, so {fixed} / {sell - var:.0f} = {n:.0f} copies.",
        checks=[
            f"Opening time for a specific room is not something to bluff. Say so in one line.",
            f"Margin = {sell} - {var} = {sell - var}. {fixed} / {sell - var} = {n:.0f}.",
            f"Check: cost {fixed} + {var}×{n:.0f} = {fixed + var * n:.0f}. Revenue {sell}×{n:.0f} = {sell * n:.0f}.",
            "The hard sub-problem is the break-even. The hours don't get a fake precision attached.",
        ],
        edges=["If they had pasted today's hours, the first half would be a quote, not a guess."],
        alts=["Spend the answer hunting a plausible opening hour and skip the arithmetic."],
    )


def reroute(rng: random.Random) -> dict:
    name = rng.choice(NAMES)
    history = [
        {
            "user": f"Roast {name}'s idea of a meeting to decide the meeting. Keep it kind.",
            "answer": f"{name} scheduled a meeting to schedule a meeting. The agenda is the calendar eating itself.",
            "mode": "banter",
            "pathway": "s1",
            "construct": "banter",
            "effort": "low",
        }
    ]
    column = rng.choice(("payments", "tax_code", "region", "sku", "status"))
    place = rng.choice(PLACES)
    user = (
        f"Ok real problem, {place} deploy. The migration job exits 1 after adding the {column} column, "
        f"and the log says duplicate column. What do I do before I rerun it?"
    )
    lead = (
        f"Don't rerun it blind. Look up whether {column} already exists. "
        f"If it does, mark that migration applied or delete the duplicate add, then rerun only the unapplied tail."
    )
    return _piece(
        family="reroute",
        history=history,
        user=user,
        lead=lead,
        detail=f"A duplicate {column} means the add already landed. Rerunning the same ADD fails the same way.",
        checks=[
            "The previous turn was a joke. This turn is a failed migration. Drop the bit.",
            "Exit 1 plus 'duplicate column' means the column is there. A second ADD will fail the same way.",
            "Check the schema, then fix the migration record, then run the remainder.",
        ],
        edges=["If the column exists but is the wrong type, marking it applied hides a real mismatch. Check the type before you stamp the book."],
        alts=["Keep roasting meetings. They changed the subject."],
    )


def heal(rng: random.Random) -> dict:
    items = [rng.randint(2, 9) for _ in range(4)]
    wrong = items[0]
    total = sum(items)
    user = (
        f"You wrote this and then looped: 'the total is {wrong}. the total is {wrong}. the total is {wrong}.' "
        f"The lines are {items}. Fix it once."
    )
    lead = f"The total is {total}."
    return _piece(
        family="heal",
        user=user,
        lead=lead,
        detail=f"{' + '.join(str(n) for n in items)} = {total}. Once.",
        checks=[
            f"The looped number {wrong} is the first line, not the sum.",
            f"{' + '.join(str(n) for n in items)} = {total}.",
            "Say the total once.",
        ],
        edges=["Repeating the corrected sentence three times is the same bug in a new hat."],
        alts=["Apologize for three paragraphs and never add the numbers."],
    )


def settle(rng: random.Random) -> dict:
    name = rng.choice(NAMES)
    n = rng.randint(2, 18)
    bring, already = rng.choice((("chairs", "tables"), ("mugs", "plates"), ("copies", "binders"), ("lamps", "stands")))
    user = (
        f"Did {name} ask for {n} {bring} or {n} {already}? "
        f"Here is the note: 'bring {n} {bring}, the {already} are already there.' Answer only that."
    )
    lead = f"{n} {bring}. The {already} are already there."
    return _piece(
        family="settle",
        user=user,
        lead=lead,
        detail=f"The note says {bring}. The {already} are already there, so {n} is not a count of {already}.",
        checks=[
            f"The note says bring {n} chairs.",
            "Tables are explicitly already there, so the number is not tables.",
            f"They asked which one. The answer is chairs. Stop.",
        ],
        edges=["Adding a floor plan would be answering a question they didn't ask."],
        alts=["A list of what else to bring. Out of scope."],
    )


def prose(rng: random.Random) -> dict:
    place = rng.choice(PLACES)
    hour = rng.choice(("11:40pm", "6:10am", "2:05am"))
    name = rng.choice(NAMES)
    scenes = [
        (
            f"Describe the laundromat in {place} at {hour} so I can drop it into a story. No moral.",
            f"At {hour} the laundromat on the corner was down to one working dryer, the one with the sticker peeling into a grey comma. "
            f"A sock had given up under the bench. The detergent machine took coins and returned nothing, and somebody had written 'liar' on it in pencil. "
            f"{name}'s basket sat unattended with a damp library book on top, the due-date slip curling in the heat.",
        ),
        (
            f"Give me the break room after everyone left, {place}, {hour}. Concrete. No lesson.",
            f"The microwave still said 0:00 and meant it. Someone's tea bag had dried onto a spoon in the sink, and the fridge hummed louder without bodies in the way. "
            f"A chair was two inches out, the way {name} leaves it. The clock over the door was four minutes fast, which everyone knew and nobody fixed.",
        ),
    ]
    user, lead = scenes[rng.randrange(len(scenes))]
    return _piece(
        family="prose",
        user=user,
        lead=lead,
        detail="Objects, a time, one named leftover. No thesis about loneliness.",
        checks=[
            "They asked for a picture they can drop into a story, not a theme.",
            "Keep a specific object that could only be in that room.",
            lead,
        ],
        edges=["A closing sentence that explains the feeling turns it into a caption."],
        alts=["A plot. They asked for the room."],
    )


def contract(rng: random.Random) -> dict:
    sets = [
        (
            ["Decision", "Risk", "Rollback", "Owner"],
            {
                "Decision": "Ship the column add behind a flag, not as a default-on write.",
                "Risk": "Old readers still select star and will break if the column is NOT NULL with no default.",
                "Rollback": "Drop the flag. Leave the nullable column. Don't drop it the same day.",
                "Owner": "Whoever is on the payments pager this week signs the flag-on.",
            },
        ),
        (
            ["Goal", "Constraint", "Step", "Check"],
            {
                "Goal": "Move invoice emails off the monolith without losing a receipt.",
                "Constraint": "One engineer, no feature freeze, the mail vendor stays.",
                "Step": "Dual-write the receipt id for a week, then cut the send over, then delete the old sender.",
                "Check": "A day of ids appears in both logs before the cut, and in only the new log after.",
            },
        ),
        (
            ["Finding", "Evidence", "Gap", "Next"],
            {
                "Finding": "The Friday failures are the retry storm, not a bad deploy.",
                "Evidence": "The error is connection refused, three times, from the same host, and the binary didn't change.",
                "Gap": "Nobody has the box-level log from that host in this thread.",
                "Next": "Stop retrying it. Get the host log, or page the person who owns the box.",
            },
        ),
    ]
    headings, sections = sets[rng.randrange(len(sets))]
    listed = ", ".join(headings)
    situation = {
        "Decision": "a payments column old readers might not tolerate",
        "Goal": "moving invoice mail off the monolith without losing a receipt",
        "Finding": "Friday job failures that may be retries rather than a bad deploy",
    }[headings[0]]
    user = (
        f"Write the note with these sections, in this order, and don't skip one: {listed}. "
        f"The situation is {situation}."
    )
    # specialize sections slightly with a name so rows differ
    name = rng.choice(NAMES)
    ticket = rng.randint(1000, 9999)
    sections = dict(sections)
    last = headings[-1]
    sections[headings[0]] = f"Ticket {ticket}. " + sections[headings[0]]
    if headings[-1] == "Owner":
        sections[last] = f"{name} is on the payments pager this week and signs the flag-on for ticket {ticket}."
    return _piece(
        family="contract",
        user=user,
        lead=sections[headings[0]],
        detail="Every heading they named has to show up, in order, with a real line under it.",
        checks=[f"Required section {h}: {sections[h]}" for h in headings],
        edges=["A missing heading is a failed note even if the prose is good."],
        alts=["A single paragraph that 'covers' the ideas. They named the sections."],
        contract=headings,
        sections=sections,
    )


def loop_plan(rng: random.Random) -> dict:
    name = rng.choice(NAMES)
    place = rng.choice(PLACES)
    day = rng.choice(("Tuesday", "Wednesday"))
    user = (
        f"Plan the move of the {place} reading group to the hall {name} booked. "
        f"I need the real sequence, not a vibe."
    )
    short = f"Book the hall."
    long = (
        f"Re-book isn't the work. {name} already has the hall for {day}. "
        f"Confirm the deposit is refundable until noon the day before, name a backup room if the lights fail, "
        f"and put the key pickup on a person who is actually in {place} that morning."
    )
    lines = [
        f"First pass. The middle step is thin: {short}",
        f"Re-ponder the middle step. {long}",
        "The first pass would have shipped 'book the hall' after it was already booked. The second pass catches that and adds the deposit deadline, the backup room, and a named key person.",
        f"Order that survives the second pass: confirm {name}'s hold, check the refund hour, assign the key, tell the group the backup, then stop.",
    ]
    lead = (
        f"Confirm {name}'s {day} hold, check the deposit refunds until noon the day before, "
        f"name who picks up the key in {place}, and only then tell the group which room is the backup."
    )
    return _piece(
        family="loop",
        user=user,
        lead=lead,
        detail=long,
        checks=lines,
        edges=["If the deposit is already non-refundable, the noon deadline is fiction and the plan should say so instead of inventing a grace period."],
        alts=["A mood board for the evening. They asked for the sequence."],
        loop_lines=lines,
    )


def decision(rng: random.Random) -> dict:
    """A choice under incomplete facts. Orbit rows lean on this."""
    name = rng.choice(NAMES)
    seats = rng.choice((12, 20, 40))
    price_a = rng.choice((30, 40))
    price_b = price_a + rng.choice((10, 25))
    user = (
        f"{name} has to pick a room for {seats} people. Room A is {price_a} an hour and has no windows. "
        f"Room B is {price_b} and has windows. The only other fact is that two people get headaches under fluorescent light. "
        f"Give me the call."
    )
    lead = (
        f"Take room B. Two people with a fluorescent headache is a real cost, and {price_b - price_a} an hour "
        f"is cheaper than losing them for the meeting."
    )
    return _piece(
        family="decision",
        user=user,
        lead=lead,
        detail=f"You have price, windows, headcount, and two headaches. You do not have a budget cap or a duration.",
        checks=[
            f"Known: {seats} people, A at {price_a} without windows, B at {price_b} with windows, two fluorescent headaches.",
            "Unknown: how many hours, and whether anyone else needs the dark. The call shouldn't wait on that.",
            lead,
            f"I'd change this if the meeting is an all-day workshop and the gap of {price_b - price_a} an hour blows a budget nobody stated.",
        ],
        edges=["If the two people can sit by a door in room A, the headache premise weakens. The prompt doesn't say that."],
        alts=["Ask five clarifying questions and refuse to pick. They asked for the call."],
        questions=[],
    )


def ui_brief(rng: random.Random) -> dict:
    place = rng.choice(PLACES)
    briefs = [
        f"A signup card for a neighborhood tool library in {place}. Quiet black stone, a thin line of champagne metal, serif headline, lots of air.",
        f"A status strip for an overnight radio desk in {place}. Night glass, acid cyan type, a magenta alert, tiny monospace labels.",
        f"A one-column essay header for a print piece about the {place} market. Warm paper, black ink, a serif headline, empty margin.",
        f"A price card for the {place} tool library. Flat loud color, a hard black edge, the button should look like it physically presses down.",
        f"A metrics board for the {place} library desk. Dark tiles, one tile wider than the others, a small glow on the number.",
        f"An icon of three stacked crates for the {place} library, drawn as flat angled faces with light from the upper left. No photo.",
        f"A settings panel for the library desk. Soft neutral color, a layered shadow, the toggle should move like a spring, not a linear slide.",
    ]
    # The brief index is chosen by the caller via mood so each palette gets a matching brief
    # when the spec is aesthetic. For other callers, pick any.
    brief = briefs[rng.randrange(len(briefs))]
    return _piece(
        family="ui",
        user=f"Build one self-contained HTML file. {brief} No external images, no placeholder boxes.",
        lead="A single HTML file with the palette baked into the CSS.",
        detail=brief,
        checks=[
            "One file, inline CSS, no remote images.",
            "Include hover and focus, and a real control, not a picture of a control.",
            brief,
        ],
        edges=["A default blue button is the failure mode they described by asking for a finished surface."],
        alts=["A wireframe description instead of the file."],
        mood=brief,
    )


def family_for(spec_category: str, spec_id: str, index: int) -> str:
    """Which situation family a canonical id should inhabit."""
    if spec_category == "aesthetic":
        return "ui"
    if spec_category == "stance":
        return "prose"
    if spec_category == "patch":
        return "contract"
    if spec_category == "reasoning_mode":
        return "loop"
    if spec_category == "orbit":
        return "decision"
    if spec_category == "mode":
        return {
            "chat": "chat",
            "hotpot": "hotpot",
            "skim": "skim",
            "vibe": "vibe",
            "banter": "banter",
            "react": "react",
            "pattern": "pattern",
            "complete": "complete",
            "stream": "stream",
            "recall": "recall",
            "deep": "deep",
            "extreme": "extreme",
            "logic": "logic",
            "plan": "plan",
            "code": "code",
            "build": "build",
            "research": "research",
            "brainstorm": "brainstorm",
            "solve": "solve",
            "teach": "teach",
            "inhibit": "inhibit",
            "escalate": "escalate",
            "reroute": "reroute",
            "heal": "heal",
            "settle": "settle",
            "auto": ("chat", "code", "solve", "plan", "banter", "deep")[index % 6],
        }[spec_id]
    if spec_category == "pathway":
        if spec_id == "s1":
            return ("chat", "hotpot", "banter", "vibe")[index % 4]
        if spec_id == "s2":
            return ("solve", "code", "plan", "deep")[index % 4]
        if spec_id == "s3":
            return ("inhibit", "settle", "heal", "reroute", "escalate")[index % 5]
        return ("chat", "solve", "plan", "inhibit")[index % 4]
    if spec_category == "thinking_effort":
        if spec_id == "off":
            return ("solve", "chat", "code")[index % 3]
        if spec_id == "low":
            return ("chat", "hotpot", "banter")[index % 3]
        return ("solve", "code", "plan", "deep")[index % 4]
    if spec_category == "channel":
        if spec_id == "instruct":
            return ("code", "solve", "plan", "chat")[index % 4]
        return ("chat", "solve", "deep", "teach")[index % 4]
    if spec_category == "reasoning_effort":
        if spec_id in ("effort_low", "effort_medium_low"):
            return ("hotpot", "solve", "chat")[index % 3]
        return ("solve", "plan", "deep", "code")[index % 4]
    if spec_category == "protium":
        if spec_id in ("hermes", "apollo"):
            return "solve"
        if spec_id == "artemis":
            return "code"
        if spec_id in ("swarm", "council"):
            return "brainstorm"
        return ("plan", "deep", "code", "build")[index % 4]
    if spec_category == "agi":
        if "comedy" in spec_id or spec_id.endswith("-story"):
            return ("banter", "react", "brainstorm")[index % 3]
        if "coder" in spec_id:
            return "code"
        if "007" in spec_id:
            return "code"
        if "business" in spec_id or "matlock" in spec_id:
            return "plan"
        if "house" in spec_id:
            return "deep"
        if "prompt" in spec_id:
            return "teach"
        if "story" in spec_id:
            return "react"
        return "plan"
    return "chat"


FAMILY = {
    "chat": chat,
    "hotpot": hotpot,
    "skim": skim,
    "vibe": vibe,
    "banter": banter,
    "react": react,
    "pattern": pattern,
    "complete": complete,
    "stream": stream,
    "recall": recall,
    "solve": solve,
    "code": code,
    "build": build,
    "logic": logic,
    "plan": plan,
    "research": research,
    "brainstorm": brainstorm,
    "teach": teach,
    "deep": deep,
    "extreme": extreme,
    "inhibit": inhibit,
    "escalate": escalate,
    "reroute": reroute,
    "heal": heal,
    "settle": settle,
    "prose": prose,
    "contract": contract,
    "loop": loop_plan,
    "decision": decision,
    "ui": ui_brief,
}


def make_piece(category: str, ident: str, index: int, rng: random.Random) -> dict:
    family = family_for(category, ident, index)
    piece = piece_for(family, rng)
    piece["family"] = family
    if category == "aesthetic":
        # Lock the brief to the palette's mood so the HTML and the ask agree,
        # without putting the palette id in the user text.
        moods = {
            "luxury": 0,
            "cyberpunk": 1,
            "editorial": 2,
            "neobrutalism": 3,
            "bento": 4,
            "svg_isometric": 5,
            "exquisite": 6,
        }
        place = rng.choice(PLACES)
        briefs = [
            f"A signup card for a neighborhood tool library in {place}. Quiet black stone, a thin line of champagne metal, serif headline, lots of air.",
            f"A status strip for an overnight radio desk in {place}. Night glass, acid cyan type, a magenta alert, tiny monospace labels.",
            f"A one-column essay header for a print piece about the {place} market. Warm paper, black ink, a serif headline, empty margin.",
            f"A price card for the {place} tool library. Flat loud color, a hard black edge, the button should look like it physically presses down.",
            f"A metrics board for the {place} library desk. Dark tiles, one tile wider than the others, a small glow on the number.",
            f"An icon of three stacked crates for the {place} library, drawn as flat angled faces with light from the upper left. No photo.",
            f"A settings panel for the library desk in {place}. Soft neutral color, a layered shadow, the toggle should move like a spring, not a linear slide.",
        ]
        brief = briefs[moods[ident]]
        price = rng.randint(4, 36)
        piece["user"] = (
            f"Build one self-contained HTML file. {brief} Show the number {price} somewhere real. "
            f"No external images, no placeholder boxes."
        )
        piece["detail"] = f"{brief} The visible number is {price}."
        piece["price"] = price
        piece["mood"] = brief
        piece["checks"] = [
            "One file, inline CSS, no remote images.",
            "Include hover and focus, and a real control, not a picture of a control.",
            brief,
        ]
    return piece

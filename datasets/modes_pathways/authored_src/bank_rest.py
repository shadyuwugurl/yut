"""Palettes, orbit, deckard, jumbo, loop."""


def _page(title, css, body):
    return (
        "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
        f"<title>{title}</title>\n<style>\n{css}\n</style>\n</head>\n<body>\n{body}\n</body>\n</html>"
    )


def rows() -> dict[str, list[dict]]:
    lux_css = "body{margin:0;background:#08090C;color:#f4efe4;font-family:Palatino,serif}main{max-width:420px;margin:8vh auto;padding:32px;border:1px solid rgba(255,255,255,.07)}h1{font-weight:500;letter-spacing:-.03em}button{background:linear-gradient(135deg,#F4D068,#AA771C);color:#08090C;border:0;padding:12px 18px}button:focus-visible{outline:1px solid #F4D068;outline-offset:3px}"
    cyber_css = "body{margin:0;background:#040508;color:#00F0FF;font-family:ui-monospace,monospace}.hud{margin:24px;border:1px solid #00F0FF;padding:16px}.lbl{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#FAFF00}strong{color:#FF0055}button{background:transparent;color:#00F0FF;border:1px solid #00F0FF;padding:8px 12px}button:focus-visible{outline:1px solid #FF0055}"
    edit_css = "body{margin:0;background:#F9F8F6;color:#121212;font-family:Georgia,serif}main{max-width:36rem;margin:12vh auto;padding:0 24px}h1{font-size:clamp(3rem,8vw,5rem);line-height:.9;letter-spacing:-.03em}hr{border:0;border-top:1px solid #121212}"
    neo_css = "body{margin:0;background:#fff4d6;color:#000;font-family:Arial,sans-serif}.card{margin:32px;background:#ffe14a;border:3px solid #000;box-shadow: 4px 4px 0 #000;padding:20px;max-width:360px}button{background:#b8ff6a;border:3px solid #000;box-shadow: 4px 4px 0 #000;padding:10px 14px}button:active{transform:translate(2px,2px);box-shadow: 2px 2px 0 #000}"
    bento_css = "body{margin:0;background:#0D1117;color:#e8eef7;font-family:Inter,sans-serif}.grid{display:grid;grid-template-columns:2fr 1fr;gap:12px;padding:24px}article{background:#161B22;border:1px solid rgba(255,255,255,.08);border-radius:12px;padding:16px}.wide{grid-column:span 2}"
    exo_css = "body{margin:0;background:oklch(0.16 0.02 260);color:oklch(0.96 0.01 260);font-family:sans-serif}.panel{margin:10vh auto;max-width:420px;padding:24px;border-radius:18px;background:oklch(0.22 0.02 260);box-shadow:0 24px 40px oklch(0 0 0 / .35);backdrop-filter:blur(16px)}.switch{width:48px;height:28px;border:0;border-radius:999px;background:oklch(0.4 0.03 260);position:relative}.switch i{position:absolute;top:3px;left:3px;width:22px;height:22px;border-radius:50%;background:#fff;transition:transform 380ms cubic-bezier(.34,1.56,.64,1)}"
    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 220" role="img"><title>Three crates</title><polygon points="150,40 230,80 150,120 70,80" fill="#f7f4ee"/><polygon points="70,80 150,120 150,180 70,140" fill="#c9c2b4"/><polygon points="230,80 150,120 150,180 230,140" fill="#8d877c"/></svg>'
    return {
        "aesthetic/luxury": [
            {
                "user": "One HTML file. A signup card for a tool library. Quiet black stone, a thin champagne line, a serif headline, lots of air. No remote images. Put 12 on it.",
                "think": "Black stone is a near-black ground, not a gray card on white. The champagne line is a thin gradient on the button, not a gold box around everything. Serif only on the headline. Space comes from a narrow measure and a large top margin, not from padding inside a crowded card. 12 is the number of tools out, so it is a figure, not a decoration. Focus has to be visible on the black, so the outline uses the same champagne.",
                "answer": _page("Library", lux_css, "<main><p>Tools out</p><h1>12</h1><p>Request a key. We'll answer this week.</p><button type=\"button\">Request a key</button></main>"),
            },
            {
                "user": "Same quiet black and champagne, but this one is a closing-hours line for the door. The number is 6.",
                "think": "A door sign is one line and a time, not a marketing page. Same ground, same hairline button if there is a control, but the headline can be the hour. 6pm is the fact. Don't add a second panel. The serif stays on the hour so the door reads as print, not as an app chrome.",
                "answer": _page("Hours", lux_css, "<main><p>We close</p><h1>6</h1><button type=\"button\">Ring if you're already inside</button></main>"),
            },
        ],
        "aesthetic/cyberpunk": [
            {
                "user": "One HTML file for an overnight radio desk. Night glass, acid cyan type, one magenta alarm word, tiny monospace labels. Show 3.",
                "think": "The ground is almost black so the cyan reads as a lamp, not as a link blue. Magenta is only the alarm word, or the whole screen becomes a poster. Labels are small, uppercase, tracked out, so they feel like chassis print. 3 is the open mics. A focus ring in magenta keeps the keyboard path visible against the cyan border.",
                "answer": _page("Desk", cyber_css, '<section class="hud"><div class="lbl">desk / live</div><p>Mics <strong>3</strong></p><button type="button">Arm mic</button></section>'),
            },
        ],
        "aesthetic/editorial": [
            {
                "user": "One HTML file, a print header about the morning market. Warm paper, black ink, a huge serif headline, a hairline rule. The number of stalls is 40.",
                "think": "Paper is a warm off-white, ink is near-black, and the headline is large enough that the page is mostly empty. The hairline is a real rule, not a card border. 40 is the stall count and it can sit in the small sans line above the headline so the serif stays a title. No buttons pretending to be print.",
                "answer": _page("Market", edit_css, "<main><p>40 stalls</p><h1>Morning in the aisle</h1><hr><p>The fish counter opens when the ice does.</p></main>"),
            },
        ],
        "aesthetic/neobrutalism": [
            {
                "user": "One HTML file, a price card for borrowing a drill. Flat loud color, a hard black edge, the button should move when pressed. Price is 0 until Thursday.",
                "think": "The shadow is a solid offset, not a blur, or it stops being the style. The edge is black and thick. Pressing the button translates it and shrinks the shadow so it feels like it hit the page. 0 is the price and it has to be readable on the yellow, so it stays black. No gradient, no rounded soft card.",
                "answer": _page("Borrow", neo_css, '<article class="card"><h1>Borrow a drill</h1><p>0 until Thursday.</p><button type="button">Hold my card</button></article>'),
            },
        ],
        "aesthetic/bento": [
            {
                "user": "One HTML file, a dark metrics board for the library desk. One tile wider than the others. Numbers 128 out, 4 late, 12 due today.",
                "think": "The ground is the dark slate, tiles sit one step lighter, borders are barely there. The wide tile spans two columns so the hierarchy is the grid, not a bigger font alone. 128 is the number that gets the wide tile because it is the stock, and 4 and 12 are the exceptions. A glow on the number is enough light. No illustration.",
                "answer": _page("Desk", bento_css, '<section class="grid"><article class="wide"><div>128</div><p>tools out</p></article><article><div>4</div><p>late</p></article><article><div>12</div><p>due today</p></article></section>'),
            },
        ],
        "aesthetic/svg_isometric": [
            {
                "user": "One HTML file. An icon of three stacked crates, flat angled faces, light from the upper left. No photo. No external file.",
                "think": "Three faces: the top is the lightest, the left is the midtone, the right is the shadow, which is what a light from the upper left does to a box. The points have to be a real isometric-looking diamond, not a rectangle with a gradient. viewBox keeps it sharp when scaled. A title inside the svg is the name. No raster, no stock photo of crates.",
                "answer": _page("Crates", "body{margin:0;background:#f3f1ea;display:grid;place-items:center;min-height:100vh}svg{width:min(480px,90vw)}", svg),
            },
        ],
        "aesthetic/exquisite": [
            {
                "user": "One HTML file, a settings panel with a single switch for the desk lamp. Soft neutral color, a layered shadow, the knob should move like a spring. Label it 1.",
                "think": "Neutrals in oklch so the steps of the surface are even, not muddy gray. The shadow is a soft stack, and a backdrop blur keeps the panel from looking pasted on. The knob uses a spring cubic-bezier, not ease, so it overshoots a little. 1 is the lamp channel and it sits as a label, not as a giant number. Focus stays visible.",
                "answer": _page("Lamp", exo_css, '<section class="panel"><h1>Desk lamp 1</h1><button class="switch" type="button" aria-pressed="false" onclick="this.setAttribute(\'aria-pressed\', this.getAttribute(\'aria-pressed\')!==\'true\')"><i></i></button></section>'),
            },
        ],
        "orbit/contextual_sanity": [
            {"user": "Room A is 30 an hour, no windows. Room B is 55, with windows. Forty people. Two get headaches under fluorescent light. Pick.", "think": "I have prices, windows, headcount, and two headaches. I don't have a duration. I don't need one. Losing two people costs more than 25 an hour for any meeting that isn't an all-day workshop, and nobody said it was.", "answer": "Take B. I'm using the prices, the headcount, and the two headaches. I don't need another fact to pick."},
            {"user": "The note says under 1400, dogs allowed, not a basement. This listing is 1350, third floor, cats only. Yes or no, and don't ask me about the view.", "think": "Price and floor pass. Cats only fails the dog. The view wasn't in the musts and they told me not to ask. The decision is no.", "answer": "No. Cats only, so the dog is out. The price and the floor were fine, and I'm not asking about the view."},
        ],
        "orbit/provisional_judgment": [
            {"user": "Sign A or B. A is a month and keeps data here. B is Friday and spends our only security review. I'd like a decision.", "think": "The slot is the scarce thing, so A. That holds only while onboarding stays inside the quarter.", "answer": "Sign A. I'd revise this if A's month slips past the quarter, or if B's host is already covered by a review you didn't mention."},
            {"user": "Ship the new ranker or keep the old one. We can look at one day of 5% traffic. Clicks on the first result are the metric we trust.", "think": "A day can show a large gap and not a small one. The rule has to include the 'keep the old one' branch or the experiment is a launch.", "answer": "Run the 5% for a day. I'd revise the 'keep the old ranker' call only if the click gap is obvious. A small gap is not a ship."},
        ],
        "orbit/childlike_capacity": [
            {"user": "The Friday demo slipped again. I need a rule for this Friday, not a lecture.", "think": "The serious version is to cut the promise. The playful version is still a real demo, just one click.", "answer": "Friday shows one path a person can click, and we strike everything else off the invite. The playful version, still legal: title the invite 'one button, then you can leave.'"},
            {"user": "Drills don't come back to the library. Fix it without a speech.", "think": "A deposit is the real mechanism. The playful version names the jar.", "answer": "Take a deposit and give it back with the drill. The playful version, still legal: a glass jar on the desk labeled 'this is your money until the drill comes home.'"},
        ],
        "orbit/instrument_bounded": [
            {"user": "Is the tap safe? March street-main test passed. A blog says 99% with no method. Monday tasted metallic after a repair.", "think": "Three notes. None is a measurement of this tap. I'll stop at the boundary.", "answer": "This is only those three notes. It says nothing about a lab result for this tap. The street main passed in March, the blog has no method, and the taste is a symptom."},
            {"user": "Did open offices make us more collaborative? The only thing in front of us is a sentence in a chat. No paper.", "think": "A sentence isn't a study. I won't supply a citation I don't have.", "answer": "This is only the sentence in the chat. It says nothing about a study, a measurement, or your office. I don't know."},
        ],
        "stance/deckard": [
            {"user": "The laundromat at 11:40pm. I need it for a story. No moral.", "think": "Objects, a time, one leftover. Don't explain loneliness.", "answer": "At 11:40pm the dryer with the peeling sticker was the only one still turning. A sock had given up under the bench. Someone had written 'liar' in pencil on the detergent machine, which had taken the coins anyway."},
            {"user": "The break room after everyone left, 6:10am. Concrete. No lesson.", "think": "A clock, a spoon, a chair. No thesis.", "answer": "The microwave still said 0:00. A tea bag had dried onto a spoon in the sink. The chair was two inches out, and the clock over the door was four minutes fast, which everyone knew."},
            {"user": "A ferry gate at 5:55am, before the first boat. No plot.", "think": "Cold, a number on a sign, one person. Stop before a story starts.", "answer": "The 5:55 sign was lit and the gate was still chained. A paper cup had been set neatly on the rail, as if the owner meant to come back for it and then didn't."},
        ],
        "patch/jumbo": [
            {
                "user": "Write the note with these sections, in this order, and don't skip one: Decision, Risk, Rollback, Owner. The situation is a payments column old readers might not tolerate.",
                "contract": ["Decision", "Risk", "Rollback", "Owner"],
                "think": "Four sections, that order. Decision is the flag, not a default-on write. Risk is select-star and NOT NULL with no default. Rollback is the flag off, column left nullable. Owner is whoever has the payments pager. If I drop Rollback the note looks finished and isn't.",
                "answer": "## Decision\nShip the column behind a flag. Don't make the new write the default.\n\n## Risk\nOld readers that select star, and inserts that omit the column, break if it is NOT NULL with no default.\n\n## Rollback\nTurn the flag off. Leave the column nullable. Don't drop it the same day.\n\n## Owner\nWhoever has the payments pager this week signs the flag-on.",
            },
            {
                "user": "Sections in this order, none skipped: Goal, Constraint, Step, Check. Moving invoice mail off the monolith without losing a receipt.",
                "contract": ["Goal", "Constraint", "Step", "Check"],
                "think": "Goal is the move without a lost receipt. Constraint is one engineer and the same vendor. Step is dual-write, cut, delete. Check is a day of ids in both logs, then only in the new one. The check is the part people skip, so it has to be its own section.",
                "answer": "## Goal\nMove invoice email off the monolith without losing a receipt.\n\n## Constraint\nOne engineer, no feature freeze, the mail vendor stays.\n\n## Step\nDual-write the receipt id, cut the sender, then delete the old sender.\n\n## Check\nA day of ids in both logs before the cut, and only in the new log after.",
            },
        ],
        "reasoning_mode/loop": [
            {
                "user": "Plan the move of the reading group into a hall that is already booked for Wednesday. I need the sequence, not a mood.",
                "think": "First pass. The middle step is thin: book the hall.\nRe-ponder the middle step. The hall is already booked, so booking it is not work. The real middle is the deposit, the key, and a backup room. Confirm the hold is Wednesday, check the deposit refunds until noon the day before, name a person who is actually in town that morning to pick up the key, and only then tell the group which room is the backup if the lights fail.\nThe first pass would have shipped a step that was already done. The second pass replaces it with three facts that can still fail.\nOrder that survives: confirm the hold, check the refund hour, name the key, tell the group the backup, stop.",
                "answer": "Confirm Wednesday's hold, check that the deposit refunds until noon the day before, name who picks up the key, then tell the group the backup room. 'Book the hall' was already done, so it isn't a step.",
            },
            {
                "user": "Sequence a two-week kitchen job. We still cook every night. Deliveries only when someone is home at 3pm.",
                "think": "First pass. The middle step is thin: start the demo on Monday.\nRe-ponder the middle step. Monday demo of the sink strands every dinner. The sink has to stay until the new one is in the room, and the room only receives deliveries at 3pm, so the new sink cannot be assumed in the morning. The night the sink actually comes out needs a meal that doesn't use it, named in advance.\nThe first pass optimized the contractor's start. The second pass optimizes dinner, which was the constraint.\nOrder that survives: deliveries at 3, unused cabinets first, sink last and only on a camp-stove night.",
                "answer": "Take deliveries at 3pm. Demo the run you aren't cooking on. Leave the sink until the new one is in the room, and pull it on a night you already planned to cook on a camp stove.",
            },
        ],
    }

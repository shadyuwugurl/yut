"""S2 modes. The think is the actual work, once."""


def rows() -> dict[str, list[dict]]:
    return {
        "mode/solve": [
            {
                "user": "48 guests, 3 glasses each, 5 glasses to a bottle. How many bottles so we don't run short?",
                "think": "48 × 3 = 144 glasses. 144 / 5 = 28.8, so the last bottle is only partly used and we still have to buy it. 29 × 5 = 145, which covers 144 with one glass spare. Buying 28 would be 140 glasses and four people short. The spare glass is the cost of not running out, not a reason to round down.",
                "answer": "29 bottles.",
            },
            {
                "user": "Out 90 km at 60 km/h and back the same 90 km at 45 km/h. Average speed for the round trip? Not the average of the two speeds.",
                "think": "Time out is 90/60 = 1.5 hours. Time back is 90/45 = 2 hours. Total time is 3.5 hours for 180 km. 180 / 3.5 = 51.428..., which is 360/7. The arithmetic mean of 60 and 45 is 52.5, and that is the trap, because the slow leg takes longer.",
                "answer": "About 51.43 km/h (exactly 360/7).",
            },
            {
                "user": "A coat is 80. The price falls 25%, then the sale price rises 25%. What do I pay?",
                "think": "25% off 80 is 20, so the sale price is 60. A 25% rise on 60 is 15, so the new price is 75. The percents do not cancel, because the rise applies to 60 rather than to 80. I am 5 short of the original. Checking the other order, a rise first would be a different problem, and it is not the one asked.",
                "answer": "75.",
            },
            {
                "user": "A fence is 18 meters and needs a post every meter, including both ends. How many posts?",
                "think": "18 one-meter gaps in a line have a post at the start of each gap and one more at the far end. Posts = gaps + 1 = 19. Counting 18 would leave the last end bare. Two panels need three posts, and the same pattern holds at 18.",
                "answer": "19 posts.",
            },
            {
                "user": "Printer A finishes the stack in 6 hours, printer B in 3 hours. How long together?",
                "think": "A's rate is 1/6 of the stack per hour. B's rate is 1/3, which is 2/6. Together 3/6 = 1/2 stack per hour. Time is 1 / (1/2) = 2 hours. Averaging 6 and 3 to get 4.5 would be wrong, because you add rates and then invert.",
                "answer": "2 hours.",
            },
            {
                "user": "Fixed cost 240, variable cost 9 per unit, sell price 15. How many units to break even?",
                "think": "Margin per unit is 15 − 9 = 6. Break-even is 240 / 6 = 40 units. Check: cost is 240 + 9×40 = 240 + 360 = 600. Revenue is 15×40 = 600. They meet. At 39 units revenue is 585 and cost is 591, still short by 6, which is exactly one unit of margin.",
                "answer": "40 units.",
            },
        ],
        "mode/code": [
            {
                "user": "Write a Python function that returns the first index where the running sum of a list reaches a target, or -1. Empty input returns -1. Example: [4, 6, 3] target 10.",
                "think": "One pass, add as I go, return the index on the first total that is greater than or equal to the target. For [4, 6, 3] the totals are 4, then 10, so the index is 1. If the target were 20 the total never gets there and the answer is -1. An empty list never enters the loop and returns -1. A first element already big enough returns 0. I should use >= rather than >, or an exact hit gets skipped.",
                "answer": "Index 1.\n\n```python\ndef first_cross(nums, target):\n    total = 0\n    for i, n in enumerate(nums):\n        total += n\n        if total >= target:\n            return i\n    return -1\n```\n\nfirst_cross([4, 6, 3], 10) is 1. first_cross([], 10) is -1.",
            },
            {
                "user": "Binary search on a sorted list of unique numbers. Return the index or -1. Show it on [1, 3, 5, 7, 9] looking for 7, and for 4.",
                "think": "Half-open interval [lo, hi). Mid is (lo+hi)//2. If nums[mid] is strictly below the target, the answer is to the right, so lo = mid+1. Otherwise hi = mid, which keeps a possible match in range. When the loop ends, lo is the insertion point. It is a hit only if it is still inside the list and equal to the target. On [1, 3, 5, 7, 9], 7 is at index 3. 4 is absent, so -1. Empty list: lo == hi == 0, return -1.",
                "answer": "7 is at index 3. 4 is absent, so -1.\n\n```python\ndef binary_search(nums, target):\n    lo, hi = 0, len(nums)\n    while lo < hi:\n        mid = (lo + hi) // 2\n        if nums[mid] < target:\n            lo = mid + 1\n        else:\n            hi = mid\n    if lo < len(nums) and nums[lo] == target:\n        return lo\n    return -1\n```",
            },
            {
                "user": "Validate an IPv4 string. Four decimal octets, 0 through 255, no leading zeros. '10.0.0.1' passes. '01.2.3.4' fails. '1.2.3' fails. '1.2.3.256' fails.",
                "think": "Split on dots and demand exactly four parts. Each part must be all digits. A part longer than one character cannot start with 0, which rejects 01 but allows a single 0, so 10.0.0.1 is fine. Then the integer must be <= 255. Wrong count of dots fails before any of that. I will not call a socket library. The rules are about the string.",
                "answer": "```python\ndef valid_ipv4(text):\n    parts = text.split('.')\n    if len(parts) != 4:\n        return False\n    for part in parts:\n        if not part.isdigit():\n            return False\n        if len(part) > 1 and part.startswith('0'):\n            return False\n        if int(part) > 255:\n            return False\n    return True\n```\n\nvalid_ipv4('10.0.0.1') is True. '01.2.3.4', '1.2.3', and '1.2.3.256' are False.",
            },
            {
                "user": "Merge overlapping inclusive intervals. Touching endpoints count as an overlap. Input [[1, 3], [2, 4], [6, 8], [7, 7]]. Empty input returns [].",
                "think": "Sort by start. Walk once, extending the open interval when the next start is <= the open end. [1, 3] and [2, 4] overlap, so they become [1, 4]. [6, 8] starts after 4, so it opens a new span. [7, 7] is inside [6, 8] and does not extend it. Result [[1, 4], [6, 8]]. Comparing every pair would work and would be needlessly quadratic. Empty input returns [].",
                "answer": "[[1, 4], [6, 8]]\n\n```python\ndef merge_intervals(spans):\n    if not spans:\n        return []\n    ordered = sorted(spans)\n    out = [list(ordered[0])]\n    for start, end in ordered[1:]:\n        if start <= out[-1][1]:\n            out[-1][1] = max(out[-1][1], end)\n        else:\n            out.append([start, end])\n    return out\n```",
            },
            {
                "user": "Drop duplicates and keep the first time each value appeared. Input ['b', 'a', 'b', 'c', 'a'].",
                "think": "A set remembers membership. A list remembers order. Append only when the value is new. Walk: b is new, a is new, b is seen, c is new, a is seen. Result ['b', 'a', 'c']. Sorting would destroy the order they asked for. Empty input returns [].",
                "answer": "['b', 'a', 'c']\n\n```python\ndef stable_unique(items):\n    seen = set()\n    out = []\n    for item in items:\n        if item not in seen:\n            seen.add(item)\n            out.append(item)\n    return out\n```",
            },
            {
                "user": "Check whether (), [], and {} are balanced. '([)]' is false even though the counts match. '' is true. '(' is false.",
                "think": "A counter is not enough, because the kinds have to match. Push opening brackets. A closer must match the top of the stack. '([)]' fails when the ')' arrives and the top is '['. An empty stack on a closer fails. Leftover openers fail, so '(' is false. The empty string never pushes and the stack is empty, so it is true.",
                "answer": "```python\ndef balanced(text):\n    pair = {')': '(', ']': '[', '}': '{'}\n    stack = []\n    for ch in text:\n        if ch in '([{':\n            stack.append(ch)\n        elif ch in pair:\n            if not stack or stack.pop() != pair[ch]:\n                return False\n    return not stack\n```\n\nbalanced('([)]') is False. balanced('') is True. balanced('(') is False. balanced('{[()]}') is True.",
            },
        ],
        "mode/logic": [
            {
                "user": "All night bakers wear a blue apron. Sofia is a night baker. So Sofia wears a blue apron. Valid? Where would it break?",
                "think": "Premise 1 says night baker implies blue apron. Premise 2 puts Sofia inside that set. Modus ponens. The form is valid. It breaks only if the first premise has an exception the user did not state, or if Sofia is not actually a night baker. Neither of those is in the text.",
                "answer": "Valid. Sofia is inside the set the rule covers, so the apron follows. It breaks only if there is an unstated exception, and there isn't one here.",
            },
            {
                "user": "All night bakers wear a blue apron. Diego is wearing a blue apron. So Diego is a night baker. Valid?",
                "think": "The rule only runs baker to apron. Seeing the apron and inferring the job affirms the consequent. Visitors can wear an apron. Diego might be a baker. This argument does not show it. It would go through only with a second premise that nobody else wears the apron, and that premise is absent.",
                "answer": "Not valid. A blue apron does not pin Diego to that job. Someone else can wear one.",
            },
            {
                "user": "If the build is green, we ship. We are not shipping. What can I conclude, and what can I not?",
                "think": "If green then ship. Not shipping is the denial of the consequent, so the build is not green. That is modus tollens. I cannot conclude the build is red for some other specific reason, only that it is not green. I also cannot conclude we will never ship.",
                "answer": "The build is not green. I cannot conclude why, and I cannot conclude you will never ship.",
            },
            {
                "user": "Some of the on-call engineers are in Lisbon. All of the people in Lisbon this week have a badge. Does it follow that some on-call engineers have a badge?",
                "think": "Some on-call are in Lisbon, and everyone in Lisbon has a badge, so those on-call people have a badge. The 'some' survives. It does not follow that all on-call engineers have a badge, because the ones not in Lisbon were never mentioned.",
                "answer": "Yes, some on-call engineers have a badge. It does not follow that all of them do.",
            },
            {
                "user": "Either the cache is stale or the query is wrong. We proved the query matches the spec. What is left, and what did I smuggle in?",
                "think": "If the or is exclusive or inclusive doesn't matter once one side is false: the remaining side is the cache. The smuggled piece is the assumption that those are the only two options. A third cause, such as the clock, is not ruled out by the sentence. Within the stated disjunction, the cache is what's left.",
                "answer": "Within what you stated, the cache is stale. You smuggled in the idea that nothing else could be wrong.",
            },
            {
                "user": "Every even integer greater than 2 is the sum of two primes. Prove or disprove it. You can treat the famous version as open.",
                "think": "This is Goldbach's conjecture for even integers greater than 2. It has been checked very far and has no known counterexample and no general proof. So I cannot claim a proof, and I cannot claim a disproof. The status is open. What I can say is that a counterexample, if one exists, is larger than the searches already done. That is the whole rigorous position available from the statement alone.",
                "answer": "Neither. That statement is Goldbach's conjecture. It is open: no proof, and no known counterexample.",
            },
        ],
        "mode/plan": [
            {
                "user": "Four people, eight weeks, pull billing out of a monolith without freezing feature work. Give me the plan you would actually run.",
                "think": "Four people cannot staff a rewrite and a feature queue. A big-bang Friday cutover has no real rollback at this headcount. A shared database forever just moves the outage. The cut that fits is an HTTP strangle: new invoices go to a new service first, old reads stay, and the database split waits until the write path is quiet. Week 1 is the boundary plus a list of internal callers that don't go through HTTP, because a pure edge strangle misses those. The middle weeks shift traffic. The last two are leftover reads and a rollback drill.",
                "answer": "Strangle it at the HTTP edge. New invoices go to a new service in week 1, old reads stay, and you don't split the database until writes are quiet. Week 1 also inventories internal callers that bypass HTTP. Last two weeks: leftover reads and one rollback drill.",
            },
            {
                "user": "I have one engineer and six weeks to move invoice email off the monolith without losing a receipt. The mail vendor stays. No feature freeze.",
                "think": "One person, so one boundary. Dual-write the receipt id for a week so a send exists in both logs before the cut. Then flip the sender. Then delete the old one only after a day of ids shows up only in the new log. Skipping the overlap is how a receipt disappears. Rewriting the monolith's mail stack is a second project.",
                "answer": "Dual-write the receipt id for a week, cut the send over, then delete the old sender. The gate is a day of ids in both logs before the cut, and only in the new log after.",
            },
            {
                "user": "We need an on-call rotation for five people. Someone is out for two weeks in the middle. Don't give me a philosophy of burnout.",
                "think": "Five people, one slot at a time, and a two-week hole. The plan is a written rota with a named secondary, the gap filled by the two people on either side splitting those weeks, and no one doing more than one week in a row. Publishing it beats a Slack scramble. A shadow rotation of everyone watching everyone is not a plan.",
                "answer": "Publish a weekly rota with a named secondary. Split the two-week absence between the people on either side of it. Nobody is primary two weeks running.",
            },
            {
                "user": "Move a reading group to a hall that is already booked for Wednesday. I need the sequence, not a vibe.",
                "think": "The hall is already booked, so 'book the hall' is not a step. The real sequence is confirm the hold, check whether the deposit is refundable until noon the day before, name who picks up the key that morning, and only then tell the group which room is the backup if the lights fail. Telling the group first creates a promise the key person hasn't accepted.",
                "answer": "Confirm Wednesday's hold, check the deposit refunds until noon the day before, name the person who picks up the key, then tell the group the backup room.",
            },
            {
                "user": "A class of 20, one afternoon, teach them git rebase without a slide deck. Plan the hour.",
                "think": "They need one repo, one bad commit, and to see the commit id change. First 10 minutes: everyone clones the same tiny repo. Next 20: make a commit on main in the upstream that they don't have, then rebase and look at the new hash. Next 20: the case where they already pushed, and why rebase is now the wrong tool. Last 10: they say back what the hash changing means. A history lecture first will eat the hour.",
                "answer": "Clone one tiny repo, make an upstream commit they don't have, rebase, and look at the new hash. Then show the already-pushed case, where rebase is the wrong tool. They restate what the new hash means before they leave.",
            },
            {
                "user": "Kitchen renovation, we still have to cook every night. Two weeks, one person who can be home at 3pm for deliveries. Plan it.",
                "think": "The constraint is dinner still happens. So the sink and one burner stay usable until the new ones are in, which means the work is sequenced as demo of the unused run first, deliveries at 3pm only, and a camp stove named as the fallback for the one night the sink is actually out. Doing the sink on day 1 strands dinner. Ordering everything for Monday when the person can only receive at 3pm wastes the morning slot.",
                "answer": "Keep one burner and the sink until the replacements are in the room. Deliveries at 3pm only. The sink comes out on a night you already planned to use a camp stove, not on day one.",
            },
        ],
        "mode/deep": [
            {
                "user": "Vendor A is 40 a seat a month, data stays in our VPC, onboarding takes a month. Vendor B is 62 a seat, they host it, and we can turn it on Friday. We have one security review slot this quarter. Which do I sign, and what would flip it?",
                "think": "The price gap is 22 a seat. That is real and it is not the scarce thing. The scarce thing is the single review slot. B spends that slot on someone else's hosting. A spends a month and keeps the data in the VPC. If the seat count is small, 22 dollars is noise next to the slot, so the slot still dominates. The flip is a standing review that already covers B's host, or onboarding that slips past the quarter so A's month becomes two and Friday actually matters. Neither of those is in the note, so I sign A and name the flip.",
                "answer": "Sign A. You would be paying 22 a seat to skip a month, and B spends the only security review this quarter. I'd flip to B if that host is already covered by a standing review, or if A's onboarding slips past the quarter.",
            },
            {
                "user": "Room A is 30 an hour with no windows. Room B is 55 an hour with windows. Forty people, and two of them get headaches under fluorescent light. Pick a room.",
                "think": "Known facts: price, windows, headcount, two headaches. Unknown: duration and whether there is a budget cap. I don't need those to pick, because losing two people for the meeting costs more than 25 an hour unless the meeting is an all-day workshop nobody mentioned. Room B. The revision is an all-day booking or a stated budget that 25 an hour blows.",
                "answer": "Take room B. Two fluorescent headaches are a real cost, and 25 an hour is cheaper than losing them. I'd revise this if the booking is all day or someone has already capped the spend.",
            },
            {
                "user": "Our cache is 512 MiB for one full sequence. Product wants to double the context length. What actually doubles, and what should I refuse to promise?",
                "think": "KV cache is linear in sequence length. Doubling the context doubles that 512 MiB, to about a gibibyte per full sequence, and batch multiplies it again. Weights do not move. I should refuse to promise that latency stays flat, because the attention work over the longer cache also grows, and I should refuse to promise it fits if they also want batch 4. A prefix cache shared across beams is not in the 512 number.",
                "answer": "The cache doubles, to about 1 GiB for one full sequence. The weights do not. Don't promise flat latency, and don't promise it still fits if the batch goes to 4.",
            },
            {
                "user": "Two indexes for the same query. Index A is 200 MB and matches the WHERE. Index B is 40 MB and matches the ORDER BY. The table is 2 GB. Which do I add first?",
                "think": "The WHERE index cuts the rows touched. The ORDER BY index only helps if you were going to read most of the table and sort it. On a 2 GB table, avoiding the read dominates a cheaper sort index. Add A. Add B later if the leftover sort shows up in the profile. Adding the small one first because it is small is how you ship the wrong index.",
                "answer": "Add A, the one that matches the WHERE. The smaller ORDER BY index is the follow-up if a sort still shows up after A is in place.",
            },
            {
                "user": "I can spend the afternoon on a flaky test or on a bug that hits one customer a day. The flake fails CI about one build in five. Which first?",
                "think": "The flake blocks everyone one build in five, so its cost is the whole team's lost afternoons, not one red row. The customer bug is real and bounded: one person a day. If the flake is in a test we can quarantine in an hour, do that first so the afternoon's real work isn't fighting CI, then the customer bug. If quarantine isn't possible and the flake is a product bug, it is the same kind of defect as the customer bug and the frequency decides: one in five builds beats one customer a day.",
                "answer": "Quarantine or fix the flake first if that is a one-hour move, because it taxes every build. Then the customer bug. If the flake is itself a product bug you can't fence off, it still goes first: one build in five is the larger blast.",
            },
            {
                "user": "Keep the old ORM for six months or rewrite the three hottest queries in SQL now. The ORM is fine everywhere else. Page latency on those three is the complaint.",
                "think": "A six-month ORM migration to fix three queries is a new project wearing the complaint as a hat. Rewriting the three queries removes the latency and leaves the ORM where it is fine. The risk is two styles of data access. That is cheaper than a migration whose only success metric was those three pages. I'd reopen the migration only if the next ten queries go the same way.",
                "answer": "Rewrite the three queries. Leave the ORM everywhere it isn't the complaint. Reopen a migration only if the next batch of hot queries looks the same.",
            },
        ],
        "mode/extreme": [
            {
                "user": "Vendor A is 40 a seat, data in our VPC, a month to onboard. Vendor B is 62, they host, Friday switch-on. One security review slot this quarter. Pick, then try to break your own pick.",
                "think": "Price gap is 22 a seat. The binding constraint is the one review slot, which B consumes and A does not. So the first pick is A. Break attempt: if onboarding slips past the quarter, A's month becomes two and Friday-B wins on the calendar alone. That is a real break, but it is a risk to watch, not a fact in the note, so it becomes the flip condition rather than the pick. Break attempt: under five seats the 22 dollars is noise, which still favors A, because the slot remains the scarce object. Break attempt: a standing review already covers B's host. That would flip the pick, and it is not in the note. I could not find a break that survives the single stated slot. Sign A, and write the flip down.",
                "answer": "Sign A. The break that almost worked is A's onboarding slipping past the quarter, or a standing review that already covers B. Neither is true in what you wrote, so A stands, with those two as the conditions that would change it.",
            },
            {
                "user": "Is the tap in our office safe to drink? Here are the only notes. Grade them and try to knock down your own conclusion.\n\n1. Vendor blog: 'Our filter removes 99% of everything.' No method.\n2. Last March's municipal report: lead under the limit at the street main.\n3. A sticky note: the tap tasted metallic on Monday after the pipes were shut for repairs.",
                "think": "The blog is an advertisement with a percent and no method. Grade D. The municipal report is a real measurement, grade B, of the wrong pipe in the wrong month. The sticky note is a symptom, grade C, not a lead number. The conclusion available from these three is that nobody has measured this tap. Break attempt: maybe the street-main result is good enough because buildings don't add lead. That fails, because the repair shutdown is exactly how a building pipe becomes the question, and the report never sampled it. Break attempt: metallic taste proves contamination. It doesn't. It is a reason to test. The conclusion survives: do not treat it as settled, test this tap.",
                "answer": "Don't treat it as settled. The street main was fine last March, the blog is an ad, and Monday's metallic taste is a reason to test this tap, not a result. Nothing here is a measurement of this tap.",
            },
            {
                "user": "A bat and a ball cost 1.10. The bat costs 1.00 more than the ball. Give the prices, then try to make the intuitive answer work.",
                "think": "Let the ball be x. The bat is x+1. Then 2x+1 = 1.10, so 2x = 0.10 and x = 0.05. The bat is 1.05. Check: 1.05 + 0.05 = 1.10, and the difference is exactly 1.00. The intuitive answer is a ball of 0.10. Then the bat is 1.10 and the total is 1.20, which already misses the stated 1.10. That answer cannot be repaired without changing the sentence to 'the bat costs 1.00', and that is not what was asked. Trying x = 0.10 in the difference also gives a bat of 1.10, so both the total and the wording fail together. 0.05 and 1.05 is the only pair that satisfies both clauses at once.",
                "answer": "The ball is 0.05 and the bat is 1.05. The 0.10 answer makes the total 1.20, so it doesn't fit the sentence you wrote.",
            },
        ],
        "mode/build": [
            {
                "user": "KV cache: 32 layers, 8 kv heads, head dim 128, sequence 4096, fp16. Bytes for K and V together, for one sequence? What doubles if I double the sequence?",
                "think": "Bytes = 2 tensors × layers × kv heads × head dim × tokens × 2 bytes for fp16. 2 × 32 = 64. × 8 = 512. × 128 = 65536. × 4096 = 2^16 × 2^12 = 2^28 = 268435456. × 2 = 536870912 bytes. 536870912 / 1024^2 = 512 MiB exactly. Doubling the sequence doubles this number. The weights do not move. Batch 4 with full sequences is four times this. fp8 would halve it, and that is a different cache.",
                "answer": "536870912 bytes, 512 MiB, for one sequence. Doubling the sequence doubles the cache. The weights stay put.",
            },
            {
                "user": "Why does this query ignore the index on email?\n\nSELECT * FROM users WHERE LOWER(email) = 'a@b.c'",
                "think": "The index is ordered by the raw email. LOWER(email) is a different value, so the planner cannot walk that order. It will scan unless there is an index on the expression LOWER(email), or the predicate is rewritten to a range on the raw column, which LOWER does not allow. Comparing email = 'a@b.c' would use the index and would miss rows stored in other cases. The fix that keeps case-insensitivity is an expression index, plus storing a normalized column if they will query it constantly.",
                "answer": "LOWER(email) hides the column from an index on email. Index the expression, or store a normalized email and compare that.",
            },
            {
                "user": "We retry failed card charges from a worker. A 201 that was actually saved, followed by a timeout on the response, gets charged again. Fix the shape, not the vendor.",
                "think": "The worker treats a missing response as a failed charge. The charge already happened. The fix is an idempotency key stored before the call, unique on the order id, and the retry sends the same key. The vendor then returns the original 201 instead of a second charge. A local 'did we already try' flag that is written after the response never runs in the timeout case, which is why it doesn't work. Write the key first.",
                "answer": "Put an idempotency key on the order before the call, and send that same key on the retry. A flag written after the response never gets set when the response is what timed out.",
            },
            {
                "user": "p95 latency went from 40ms to 400ms after we raised the pool from 10 connections to 100. The database CPU is idle. What do you look at first?",
                "think": "Idle CPU means the database is not doing more work. It is waiting, or the app is. A pool of 100 against a database that is happy often means lock wait, or the app is now scheduling so many requests that they pile up on a saturated client. First graph is lock waits and the app's runnable queue, not a bigger pool. Raising the pool again would add waiters. Also check that the new pool didn't disable prepared statements or move to a transaction mode that holds locks longer. The idle CPU is the clue that capacity is not the missing piece.",
                "answer": "Look at lock waits and the app's own queue, not the database CPU. The pool grew and the database is idle, so the time is waiting, not computing. Don't raise the pool further until you see the wait.",
            },
            {
                "user": "Design the smallest thing that tells us whether the new ranker is better before we give it all the traffic. We can afford to be wrong for a day.",
                "think": "A full shadow pipeline is a second project. The smallest honest test is 5% of traffic, same request logged with both scores, and one metric they already trust, such as the click on the first result. A day is enough to see a large gap and not enough to see a small one, so the decision rule has to be 'ship only if the gap is obvious, otherwise keep the old ranker'. No new dashboard. A notebook over the log is the report.",
                "answer": "Five percent of traffic, log both scores, judge it on clicks of the first result. Ship the new ranker only if the gap is obvious after a day. Otherwise keep the old one. A notebook over the log is the whole report.",
            },
            {
                "user": "The deploy exits 1 with 'duplicate column: region'. What do I check before I rerun the migration?",
                "think": "Duplicate column means the ADD already landed and the migration book is what failed to record it. Rerunning the same ADD fails the same way. Check the column exists and that its type matches the migration. If it does, mark that migration applied and run only the tail. If the type is wrong, marking it applied hides a mismatch, so fix the column first. Don't rerun blind.",
                "answer": "Check that region exists and that its type matches the migration. If it does, mark that migration applied and run the tail. If the type is wrong, fix the column before you stamp the book. Don't rerun the same ADD.",
            },
        ],
        "mode/research": [
            {
                "user": "Should we drink the office tap? Only these notes exist.\n\n1. Vendor blog: the filter removes 99% of everything. No method.\n2. Municipal report, last March: lead under the limit at the street main.\n3. Sticky note: metallic taste on Monday after a pipe shutdown.",
                "think": "Grade only what was pasted. The blog is a claim with a percent and no method, grade D. The municipal sample is a real measurement of the street main last March, grade B, and it is the wrong pipe and the wrong month. The sticky note is a symptom report, grade C. Metallic after a repair is a reason to test, not a lead result. Nothing here measures this tap.",
                "answer": "Don't treat it as settled. The street main was fine last March, the blog is an ad, and Monday's taste is a reason to test this tap. Nobody has measured this tap.",
            },
            {
                "user": "Is the new onboarding email 'proven' to raise activation? The only evidence is a vendor case study of one company, a tweet from our PM, and our own last quarter where activation rose 2 points in the same month we also changed the pricing page.",
                "think": "The case study is one company, selected by the vendor, grade C at best. The tweet is an opinion, grade D. Our quarter confounds the email with the pricing change, so the 2 points cannot be assigned to the email, grade C as a coincidence note. Nothing here is a controlled comparison. 'Proven' is not available.",
                "answer": "No. The case study is one vendor-picked company, the tweet is an opinion, and your 2 point rise happened in the same month as a pricing change. None of that isolates the email.",
            },
            {
                "user": "A coworker says 'studies show open offices make people more collaborative.' We have no papers in front of us. What can I honestly answer?",
                "think": "I don't have the studies in the thread, so I cannot grade them, and I should not invent a citation. What I can say is that the claim as stated has no source here, and that collaboration and focused work are different outcomes a study can move in opposite directions. The honest next step is to ask which paper, not to nod.",
                "answer": "Not from anything in front of us. Ask which study. Collaboration and the ability to concentrate are different outcomes, and a slogan doesn't say which one was measured.",
            },
            {
                "user": "Compare these two bug writeups and tell me which I'd rather debug from.\n\nWriteup A: 'It's slow for some users.'\nWriteup B: 'p95 of GET /search went from 40ms to 400ms at 14:10 UTC, only for accounts over 10k rows, after deploy 4f2c. Database CPU idle.'",
                "think": "A has no route, no time, no size, and no deploy, so there is nowhere to start tonight. B has a metric, a clock time, a cohort, a deploy hash, and a negative finding that rules out database CPU. The negative finding matters because it stops me looking at the idle machine first. B is the writeup I can investigate. A is a mood.",
                "answer": "B. It names the route, the time, the cohort, the deploy, and the fact that database CPU was idle. A cannot be started.",
            },
            {
                "user": "We got three quotes for the same laptop repair. 90 with no parts list, 140 with the screen model written down, 70 from a place that says 'usually it's the screen.' Which quote is evidence?",
                "think": "The 140 names the part, so it can be checked. The 90 has no parts list, so I cannot tell what I would be buying. The 70 is a guess about the usual failure, not a look at this machine. Only the 140 is evidence about this repair. It might still be a bad price. That is a different question.",
                "answer": "The 140, because it names the screen model. The 90 doesn't say what you'd be paying for, and the 70 is a guess about laptops in general.",
            },
            {
                "user": "Rank these sources for 'what did our error rate do last Tuesday.'\n\n- A Slack memory from someone who was on call.\n- The metrics dashboard for that day.\n- A postmortem draft written Friday from memory.",
                "think": "The dashboard is the instrument. The Slack note is a contemporaneous human report and can catch what the dashboard doesn't label, so it is second. The Friday draft is a reconstruction and ranks last. If the dashboard was broken on Tuesday, the ranking flips, and nobody has said that.",
                "answer": "Dashboard, then the Slack note from the person on call, then the Friday draft. The draft is a memory of the day, not the day.",
            },
        ],
        "mode/brainstorm": [
            {
                "user": "A tiny tool library. Drills go out and don't come back. Three actually different fixes, then pick one.",
                "think": "Three mechanisms, not three wordings of a reminder. A reminder text is cheap and is what they already aren't answering. A public late list punishes the regulars who can read and misses the person who doesn't care. A card hold released on return changes the cost of keeping the drill. The hold is the one that changes the incentive. It fails if borrowers have no cards, in which case a cash deposit is the same mechanism.",
                "answer": "Pick a card hold, released when the drill comes back. A reminder text and a public late list don't change the cost of keeping it. If people don't have cards, take a cash deposit instead. Same idea.",
            },
            {
                "user": "We need a name for a neighborhood tool library. Three directions that aren't the same joke, and the one I'd paint on the window.",
                "think": "One direction is plain speech: Borrowed. One is the object: The Drill Next Door. One is the rule: Bring It Back. They are a verb, a noun, and a command, not three puns. I'd paint Bring It Back, because the failure mode of the place is the name, and a stranger can read it from the street.",
                "answer": "Borrowed, The Drill Next Door, or Bring It Back. Paint Bring It Back. A stranger can read the rule from the sidewalk.",
            },
            {
                "user": "The Friday demo keeps slipping. Three different ways to make it stop slipping. Pick.",
                "think": "A longer sprint is the same slip with more room. A public countdown without a smaller demo still slips. Cutting the demo to one path a user can actually click, and deleting the rest from Friday's promise, changes the size of the promise. That is the one I'd pick. The other two rearrange the calendar.",
                "answer": "Cut Friday's promise to one path a person can click, and take the rest off the invite. A longer sprint and a louder countdown don't change what you promised.",
            },
            {
                "user": "Give me three ways to teach a new hire the deploy, and the one I'd use on their second day.",
                "think": "A doc they read alone doesn't show the failure. A shadow where they only watch doesn't put their hands on it. A supervised rollback of a no-op deploy, with them typing and me watching, teaches the scary part while the blast radius is nothing. I'd use the third on day two. The doc is the homework after, not the lesson.",
                "answer": "Have them roll back a no-op deploy while you watch. Reading the doc and shadowing a real deploy don't put the scary command in their hands while it's still harmless.",
            },
            {
                "user": "Three ways to stop a meeting that exists only to schedule the next meeting. Pick one you would enforce.",
                "think": "A satire note won't survive contact with the calendar. A rule that a meeting needs a decision in the invite, and gets declined otherwise, is enforceable by the person who owns their own calendar. Replacing it with a doc only works if someone writes the doc. I'd enforce the decline rule, because it doesn't need a new tool.",
                "answer": "Decline any invite that doesn't name the decision. A joke and a 'let's use a doc instead' both wait for someone else to go first.",
            },
            {
                "user": "The library's Saturday is too quiet. Three different bets, then the one I'd try for a month.",
                "think": "Opening earlier is the same empty room at a worse hour. A kids' hour changes who comes and needs staffing we may not have. A repair hour, bring the broken drill and someone looks at it, uses the thing the library already is. I'd try the repair hour for a month and count bodies, not vibes. If nobody comes, the bet was wrong and it was cheap.",
                "answer": "Try a repair hour for a month: bring the broken tool, someone looks at it. Opening earlier is the same empty room. A kids' hour needs staff you may not have.",
            },
        ],
        "mode/teach": [
            {
                "user": "I know what a Python list is. I don't know what happens when two keys land in the same dict bucket. One picture.",
                "think": "They already have the list. The gap is the bucket. A dict is a list of buckets. The hash picks the bucket. Equality picks the key inside a small chain in that bucket. If I only had equality I would scan the whole collection. The picture is a row of boxes, two names in one box, and a short walk of that box only.",
                "answer": "A dict is a row of boxes. The hash picks the box. If two keys share a box, they sit in a short chain, and lookup walks that chain checking equality. Hash chooses the box. Equality chooses the key inside it.",
            },
            {
                "user": "I know what a git commit is. I don't know what a rebase does to commits that already exist. Teach that, not the whole of git.",
                "think": "Start from the commit they know. Rebase does not edit that object. It copies the changes onto a new parent, and the copy has a new id. The old commit remains until nothing points at it. That is why rebasing a branch someone else already pulled rewrites history they have.",
                "answer": "Rebase copies your commits onto a new base. The new commits have new ids. The old ones are still in the object store until nothing points at them. That is why rebasing a branch someone else has already pulled rewrites the history they have.",
            },
            {
                "user": "I can write a SQL WHERE. Why doesn't the index get used when I wrap the column in LOWER? One concrete reason.",
                "think": "They know the WHERE. The gap is what the index is sorted by. It is sorted by the raw column. LOWER(email) is a different sequence, so the sorted list can't be walked. The fix is an index on the expression, or a comparison that doesn't wrap the column.",
                "answer": "The index is sorted by the raw email. LOWER(email) is a different value, so the planner can't walk that sorted list. Index the expression, or compare the column without wrapping it.",
            },
            {
                "user": "I know what a function is. I don't know why an idempotency key has to be written down before the call, not after. Explain it with a timeout.",
                "think": "The failure they need is the timeout after success. The charge happens, the response dies, the worker thinks it failed, and a flag written after the response never got written. The key has to exist before the call so the retry can show the same key and get the original result back.",
                "answer": "If the charge succeeds and the response times out, your code thinks it failed. A flag you meant to write after the response never gets written. The key has to be stored before the call, so the retry can send the same key and get the original charge back instead of a second one.",
            },
            {
                "user": "Teach me what p95 means. I know an average. Use the search page, which is usually fast and sometimes awful.",
                "think": "Average hides the awful tail. Sort the latencies, take the point where 95% are faster. One slow request in a hundred barely moves the average and is the whole p95 story if the tail is long. On the search page, p95 is the slow experience a real person actually hits, not the typical one.",
                "answer": "Sort a hundred search latencies. p95 is the 95th, the point where only five were slower. The average can stay small while that 95th is awful, which is why the page feels fast to you and broken to someone else.",
            },
            {
                "user": "I understand a boolean. I don't understand why 'if value:' is the wrong test when value is a quantity that is allowed to be zero. Show it.",
                "think": "They know if. The gap is that zero is a real quantity and is falsy. A missing quantity and a quantity of zero fall in the same branch. The test they want is 'is value None', or they should use a sentinel that isn't a legal amount.",
                "answer": "Zero is a real quantity, and `if value` treats it as missing. A cart with quantity 0 and a cart where quantity was never set take the same branch. Test `value is None` if zero is allowed.",
            },
        ],
    }

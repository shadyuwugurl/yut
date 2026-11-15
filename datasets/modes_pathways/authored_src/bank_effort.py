"""Thinking effort, DavidAU depth, and the instruct channel."""
from author_pack import TOOL_HTTP, TOOL_QUERY, TOOL_READ, TOOL_SEARCH, TOOL_WEATHER, call


def rows() -> dict[str, list[dict]]:
    return {
        "thinking_effort/off": [
            {"user": "48 guests, 2 glasses each, 6 a bottle. How many bottles?", "hint": {"mode": "solve"}, "answer": "16."},
            {"user": "Is 17 prime?", "hint": {"mode": "hotpot"}, "answer": "Yes."},
            {"user": "Finish: def clamp(n, lo, hi):\n    # finish", "hint": {"mode": "code"}, "answer": "```python\ndef clamp(n, lo, hi):\n    if n < lo:\n        return lo\n    if n > hi:\n        return hi\n    return n\n```"},
            {"user": "Text for the neighbor about 7am basketball. Later start, no feud.", "hint": {"mode": "chat"}, "answer": "Hey, the ball on the shared wall is loud at 7. Could you start after 9?"},
            {"user": "Posts for a 9 meter fence, one every meter, both ends included.", "hint": {"mode": "solve"}, "answer": "10."},
            {"user": "Decline Farah's weekend. No money, no Saturday, no fake illness.", "hint": {"mode": "chat"}, "answer": "I can't do the weekend, Farah. Money's tight and Saturday is taken. Ask me for an evening."},
        ],
        "thinking_effort/low": [
            {"user": "What is 2 to the 10th, and is a kilogram of feathers heavier than a kilogram of steel?", "hint": {"mode": "hotpot"}, "think": "2^10 is 1024. A kilogram is a kilogram, so the feathers and the steel weigh the same.", "answer": "1024. Same weight."},
            {"user": "One line back. I'm exhausted and the review moved again.", "hint": {"mode": "vibe", "construct": "companion"}, "think": "Clipped, no cheer. They want a line they can send.", "answer": "Send the new time. I'm not moving Thursday twice."},
            {"user": "Roast a blockchain library card. Then stop.", "hint": {"mode": "banter", "construct": "banter"}, "think": "One image. The book is still late.", "answer": "Your overdue fine now needs a gas fee. The book is still late."},
            {"user": "Gist: bus late, missed the 14:10 ferry, 15:40 had space, hotel held the room.", "hint": {"mode": "skim", "construct": "recap"}, "think": "The miss is the 14:10. The recovery is the 15:40 and the held room.", "answer": "Missed the 14:10 because the bus was late. The 15:40 had seats and the hotel kept the room."},
            {"user": "How many hours in three days?", "hint": {"mode": "chat"}, "think": "3 × 24 = 72. Nothing else was asked.", "answer": "72."},
            {"user": "I'm live and the pan just caught. One line.", "hint": {"mode": "stream", "construct": "stream"}, "think": "They're holding a hot pan. The line is the action.", "answer": "Off the heat, lid on, no water."},
        ],
        "thinking_effort/high": [
            {"user": "A coat is 80, falls 25%, then the sale price rises 25%. What do I pay, and why isn't it 80?", "hint": {"mode": "solve"}, "think": "25% of 80 is 20, so the sale price is 60. 25% of 60 is 15, so the new price is 75. The rise applies to 60, not to the original 80, which is why the two percents don't cancel. Check: 80 × 0.75 = 60, and 60 × 1.25 = 75. I am 5 short of the starting price. Doing the rise first would be a different question.", "answer": "75. The rise hits the already-reduced price, so you don't get back to 80."},
            {"user": "Binary search for 7 and for 4 in [1, 3, 5, 7, 9]. Write the function.", "hint": {"mode": "code"}, "think": "Half-open [lo, hi). If nums[mid] < target, lo = mid+1, else hi = mid, which keeps a possible match. When the loop ends, lo is the insertion point, and it is a hit only if it is in range and equal. 7 sits at index 3. 4 is between 3 and 5, so the insertion point fails the equality test and returns -1. Empty input never enters and returns -1. Using hi = mid-1 on equality would skip a duplicate, but this list has none, and the half-open form doesn't need that branch.", "answer": "7 is at index 3. 4 is absent.\n\n```python\ndef binary_search(nums, target):\n    lo, hi = 0, len(nums)\n    while lo < hi:\n        mid = (lo + hi) // 2\n        if nums[mid] < target:\n            lo = mid + 1\n        else:\n            hi = mid\n    if lo < len(nums) and nums[lo] == target:\n        return lo\n    return -1\n```"},
            {"user": "Four people, eight weeks, extract billing, features keep shipping. The plan you'd run.", "hint": {"mode": "plan", "construct": "deeptree"}, "think": "A rewrite plus a feature queue doesn't fit four people. A Friday cutover has no rollback. Leaving a shared database forever moves the outage instead of the coupling. The cut that fits is an HTTP strangle: new invoices go to a new service, old reads stay, and the database splits only after writes are quiet. Week 1 has to list internal jobs that call billing without HTTP, or the strangle misses them. The last two weeks are leftover reads and one rollback drill.", "answer": "Strangle at the HTTP edge. New invoices move first, old reads stay, database last. Week 1 lists callers that skip HTTP. Finish with leftover reads and a rollback drill."},
            {"user": "All dock clerks wear a yellow badge. Idris is wearing a yellow badge. Is Idris a dock clerk?", "hint": {"mode": "logic"}, "think": "The rule runs clerk to badge, not badge to clerk. Seeing the badge and inferring the job affirms the consequent. A visitor can wear a badge. Idris might be a clerk. This argument doesn't show it. It would go through only if nobody else wears the badge, and that premise isn't here.", "answer": "Not from this. A yellow badge doesn't pin Idris to that job."},
            {"user": "KV cache, 16 layers, 4 kv heads, head dim 64, sequence 2048, fp16. Bytes for K and V, one sequence?", "hint": {"mode": "build", "construct": "ai_engineer"}, "think": "Two tensors, K and V. Bytes = 2 × layers × heads × dim × tokens × 2 bytes. 2 × 16 = 32. × 4 = 128. × 64 = 8192. × 2048 = 8192 × 2048. 8192 is 2^13 and 2048 is 2^11, product 2^24 = 16777216. × 2 = 33554432 bytes. Divide by 1024 twice: 33554432 / 1024 = 32768, / 1024 = 32 MiB. Doubling the sequence would double this. The weights would not move.", "answer": "33554432 bytes, 32 MiB. Doubling the sequence doubles the cache, not the weights."},
            {"user": "Office tap: vendor blog says 99% with no method, March street-main test passed, Monday tasted metallic after a repair. Drink it?", "hint": {"mode": "research", "construct": "research"}, "think": "The blog is a percent with no method, so it isn't evidence about this building. The March test measured the street main, a different pipe and a different month, and it can be true while this tap is the question. The metallic note is a symptom after a shutdown, which is a reason to test and not a concentration. No note in front of me is a measurement of this tap. I won't invent a lab result to close the gap.", "answer": "Don't decide from these. Test this tap. The March result was the street main, the blog has no method, and the taste isn't a measurement."},
        ],
        "reasoning_effort/effort_low": [
            {"user": "2 to the 10th?", "hint": {"mode": "hotpot", "pathway": "s1"}, "think": "1024.", "answer": "1024."},
            {"user": "Capital of Portugal?", "hint": {"mode": "chat", "pathway": "s1"}, "think": "Lisbon.", "answer": "Lisbon."},
            {"user": "Posts on a 4 meter fence, both ends, every meter?", "hint": {"mode": "solve", "pathway": "s1"}, "think": "Gaps plus one. 5.", "answer": "5."},
            {"user": "Is 2 prime?", "hint": {"mode": "hotpot", "pathway": "s1"}, "think": "Yes. Only even prime.", "answer": "Yes."},
        ],
        "reasoning_effort/effort_medium_low": [
            {"user": "36 people, 2 glasses, 6 a bottle. Bottles, and don't show a menu.", "hint": {"mode": "solve", "pathway": "s1"}, "think": "36 × 2 = 72 glasses. 72 / 6 = 12 exactly. 12 × 6 = 72, so there is no remainder to round. A menu was not asked.", "answer": "12."},
            {"user": "A price is 50, falls 10%, then rises 10%. Back to 50?", "hint": {"mode": "solve", "pathway": "s1"}, "think": "10% off 50 is 45. 10% of 45 is 4.5, so the new price is 49.5. The rise hits 45, not 50. Not back to 50.", "answer": "No. 49.5."},
            {"user": "Which writeup can I debug: 'it's slow', or 'p95 of /search went from 40ms to 400ms at 14:10, deploy 4f2c, database CPU idle'?", "hint": {"mode": "research", "pathway": "s1", "construct": "research"}, "think": "The first has no route, no time, no deploy. The second has all three and a negative finding. Start on the second.", "answer": "The second. It names the route, the time, the deploy, and the idle CPU."},
            {"user": "Remind me the fence rule in one line, using a 6 meter fence as the example.", "hint": {"mode": "teach", "pathway": "s1", "construct": "teacher"}, "think": "6 gaps need a post at each end of the line, so 7 posts. The rule is gaps plus one when both ends count.", "answer": "A 6 meter fence with a post every meter, both ends included, needs 7 posts. Count gaps, then add the far end."},
        ],
        "reasoning_effort/effort_medium": [
            {"user": "Out 80 km at 40 km/h, back 80 km at 60 km/h. Average speed?", "hint": {"mode": "solve"}, "think": "Time out is 80/40 = 2 hours. Time back is 80/60 = 4/3 hours, about 1.333. Total time is 10/3 hours for 160 km. 160 / (10/3) = 160 × 3 / 10 = 48 km/h. The average of 40 and 60 is 50, and it is wrong because the slow leg takes longer. 48 is the speed that covers 160 km in the time actually driven.", "answer": "48 km/h."},
            {"user": "Write stable_unique for ['b','a','b','c','a'] and say what sorting would ruin.", "hint": {"mode": "code"}, "think": "Walk once. A set tracks membership and a list tracks order. b is new, a is new, b is seen, c is new, a is seen. Result ['b', 'a', 'c']. Sorting would emit ['a', 'b', 'c'] and would answer a different question. Empty input appends nothing and returns []. The first occurrence is the one that stays, which is what 'stable' is doing here.", "answer": "['b', 'a', 'c']. Sorting would scramble first-seen order.\n\n```python\ndef stable_unique(items):\n    seen = set()\n    out = []\n    for item in items:\n        if item not in seen:\n            seen.add(item)\n            out.append(item)\n    return out\n```"},
            {"user": "Some on-call engineers are in Lisbon. Everyone in Lisbon this week has a badge. What follows?", "hint": {"mode": "logic"}, "think": "The on-call people who are in Lisbon have a badge, because everyone there has one. 'Some' survives. It does not follow that every on-call engineer has a badge, since the ones outside Lisbon were never in the premises. It also doesn't follow that every badged person is on call.", "answer": "Some on-call engineers have a badge. Not all of them, and not everyone with a badge is on call."},
            {"user": "One engineer, six weeks, move invoice email off the monolith, vendor stays, no freeze, no lost receipts. Plan.", "hint": {"mode": "plan", "construct": "deeptree"}, "think": "One person means one boundary. Dual-write the receipt id so a send exists in both logs before the cut. Flip the sender only after a day of ids appears in both. Delete the old sender only after a day appears only in the new log. Skipping the overlap is how a receipt vanishes. Rewriting the monolith's mail stack is a second project and doesn't fit six weeks with features still moving.", "answer": "Dual-write the receipt id for a week, cut the sender over, then delete the old one. Gate each step on a day of ids in the logs you expect."},
        ],
        "reasoning_effort/effort_high": [
            {"user": "Vendor A is 40 a seat, data in our VPC, a month to onboard. Vendor B is 70, hosted, Friday switch-on. One security review this quarter. Pick and name the flip.", "hint": {"mode": "deep"}, "think": "The gap is 30 a seat. That money is visible and it is not the scarce object. The scarce object is the single review slot. B spends it on someone else's host. A spends a month and keeps the data here. If there are only a few seats, 30 dollars is noise beside the slot, which still favors A. Break: A's month slips past the quarter, and then Friday is the whole decision. That isn't stated, so it is a condition, not the pick. Break: a standing review already covers B's host. Also unstated. Sign A. Flip to B only if one of those two shows up in writing.", "answer": "Sign A. Flip to B only if A's onboarding slips past the quarter, or B's host is already covered by a standing review."},
            {"user": "Merge [[1,3],[2,4],[6,8],[7,7]]. Touching counts. Show the walk.", "hint": {"mode": "code"}, "think": "Sort is already almost sorted. Start open interval [1, 3]. Next start 2 is <= 3, so extend the end to max(3, 4) = 4. Open interval is [1, 4]. Next start 6 is greater than 4, so close [1, 4] and open [6, 8]. Next start 7 is <= 8, and the end 7 does not extend 8. Result [[1, 4], [6, 8]]. A gap of one, say [1, 3] then [5, 6], would stay split because 5 > 3. Touching [1, 3] and [3, 4] would merge because 3 <= 3. Empty input returns before the walk.", "answer": "[[1, 4], [6, 8]]\n\n```python\ndef merge_intervals(spans):\n    if not spans:\n        return []\n    ordered = sorted(spans)\n    out = [list(ordered[0])]\n    for start, end in ordered[1:]:\n        if start <= out[-1][1]:\n            out[-1][1] = max(out[-1][1], end)\n        else:\n            out.append([start, end])\n    return out\n```"},
            {"user": "If the build is green we ship. We are not shipping. What follows, and what doesn't?", "hint": {"mode": "logic"}, "think": "Green implies ship. Not shipping denies the consequent, so the build is not green. That is the whole deduction. It does not say the build is red for a particular reason, and it does not say we will never ship. If the first premise were 'we ship only if green', the converse direction would be different, but the sentence given is only one direction. Denying the antecedent, 'the build is not green, therefore we are not shipping', is not what was asked and would be invalid anyway.", "answer": "The build is not green. You cannot conclude why, and you cannot conclude you will never ship."},
            {"user": "Retry of a card charge double-bills when the 201 is saved and the response times out. Fix the shape.", "hint": {"mode": "build", "construct": "ai_engineer"}, "think": "The worker treats silence as failure. The charge already exists. A boolean written after the response never gets written in the timeout case, so the retry looks like a first attempt. The key has to be persisted before the call, unique on the order, and resent unchanged. The vendor then returns the original result instead of creating another charge. Doing the uniqueness check only in memory dies with the process. Doing it after success dies with the timeout. Before the call is the only place the timeout still leaves a record.", "answer": "Persist an idempotency key before the call and send it again on the retry. A flag written after the response is absent exactly when the response times out."},
        ],
        "reasoning_effort/effort_ultra": [
            {
                "user": "A bat and a ball cost $1.10. The bat costs $1.00 more than the ball. Find both prices, show the check, and show why $0.10 cannot be repaired.",
                "hint": {"mode": "extreme"},
                "think": "Let the ball cost x dollars. The bat costs x + 1. Their sum is 1.10, so 2x + 1 = 1.10, 2x = 0.10, x = 0.05. The bat is 1.05. Check the sum: 1.05 + 0.05 = 1.10. Check the difference: 1.05 − 0.05 = 1.00. Both clauses hold. The intuitive price for the ball is 0.10. Then the bat, being a dollar more, is 1.10, and the sum is 1.20, which is already not 1.10. If someone instead forces the sum by pricing the bat at 1.00 and the ball at 0.10, the difference is 0.90, not 1.00. No pair with a 0.10 ball satisfies both the sum and the difference. Changing the sentence to 'the bat costs $1.00' would make 0.10 right, and that is a different sentence. The only pair for the sentence as written is 0.05 and 1.05.",
                "answer": "Ball $0.05, bat $1.05. A $0.10 ball makes either the total $1.20 or the difference $0.90, so it can't be repaired without rewriting the question.",
            },
            {
                "user": "Goldbach for even integers greater than 2: every such integer is the sum of two primes. What is the status, and what would count as settling it?",
                "hint": {"mode": "logic"},
                "think": "The statement is Goldbach's conjecture. It has been verified by search up to very large bounds, and no counterexample is published. Verification to a bound is not a proof, because the next even integer is not covered by a finite check. A proof would be a general argument that every even integer past 2 has such a pair. A disproof would be one even integer past 2 that cannot be written that way, and it would have to sit beyond the searched range or the search would already have found it. I cannot produce either. Saying 'probably true' is a mood, not a status. The status is open. Settling it means a proof, or one explicit counterexample.",
                "answer": "Open. A proof would settle it one way. One even integer greater than 2 that is not the sum of two primes would settle it the other way. A long computer check is neither.",
            },
        ],
        "reasoning_effort/effort_xultra": [
            {
                "user": "We can sign A or B and we get one security review this quarter. A is 40 a seat, data stays in our VPC, onboarding is a month. B is 85 a seat, they host, and it can be on by Friday. There are 12 seats. Walk both paths, try to kill your pick, and say what a one-day mistake would cost.",
                "hint": {"mode": "extreme"},
                "think": "Path A. Twelve seats at 40 is 480 a month, plus a month before anyone uses it, and the data stays in the VPC so the review slot is not spent on a new host. Path B. Twelve seats at 85 is 1020 a month, 540 more than A, and Friday is real, and the review slot is consumed by their hosting. Over a year the price gap is 540 × 12 = 6480, which is real money and still smaller than a blocked quarter if the slot was the only way to ship something else. The binding constraint in the note is the slot, not the 540. First pick is A. Kill attempt: onboarding slips past the quarter. Then A bought nothing this quarter and B's Friday would have. That is a risk to write down, not a fact, so it becomes a flip condition. Kill attempt: the 12 people are idle without the tool and a week of their time exceeds 540. Possible, and not in the note. I will not invent their burn rate. Kill attempt: a standing review already covers B. Also absent. A one-day mistake, meaning we sign the wrong one and reverse tomorrow, costs the contract's cooling-off if there is one, which nobody stated, so I won't pretend it's free. The pick that survives the stated facts is A, with two written flip conditions and no invented salary math.",
                "answer": "Sign A. Twelve seats makes B 540 a month more, and B also spends the only review. Flip if A's month slips past the quarter, or if B's host is already covered by a standing review. I won't price a one-day reversal, because no cooling-off term is in what you wrote.",
            },
        ],
        "channel/instruct": [
            {"user": "48 guests, 3 glasses each, 5 a bottle. How many bottles?", "hint": {"mode": "solve"}, "answer": "29."},
            {"user": "Write first_cross(nums, target). First index where the running sum reaches the target, else -1.", "hint": {"mode": "code"}, "answer": "```python\ndef first_cross(nums, target):\n    total = 0\n    for i, n in enumerate(nums):\n        total += n\n        if total >= target:\n            return i\n    return -1\n```"},
            {"user": "Neighbor text. Basketball at 7am. Ask for 9. No feud.", "hint": {"mode": "chat", "pathway": "s1", "thinking_effort": "off"}, "answer": "Hey, the ball on the shared wall is loud at 7. Could you start after 9?"},
            {"user": "All night bakers wear a blue apron. Sofia is a night baker. Does she wear one?", "hint": {"mode": "logic"}, "answer": "Yes. The rule covers her."},
            {"user": "Four people, eight weeks, pull billing out, keep shipping features. The plan, short.", "hint": {"mode": "plan", "construct": "deeptree"}, "answer": "Strangle at the HTTP edge. New invoices first, old reads stay, database last. Week 1 lists callers that skip HTTP."},
            {"user": "A price is 100, falls 20%, rises 20%. Final price?", "hint": {"mode": "solve"}, "answer": "96."},
        ],
        "channel/reasoning": [
            {"user": "Is 91 prime?", "hint": {"mode": "solve", "thinking_effort": "low", "pathway": "s1"}, "think": "91 is 7 × 13. Both factors are greater than 1, so it is not prime.", "answer": "No. 7 × 13 = 91."},
            {"user": "Teach me in one picture why a zero quantity fails `if value:`.", "hint": {"mode": "teach", "construct": "teacher", "thinking_effort": "high"}, "think": "They know a boolean test. Zero is a legal quantity and it is falsy in Python, so a cart with quantity 0 and a cart where the field was never set take the same branch. The picture is two carts, one empty on purpose and one unfilled, and the test can't tell them apart. The test that keeps zero is `value is None`.", "answer": "Zero is a real quantity, and `if value` treats it as missing. Test `value is None` when zero is allowed."},
            {
                "user": "What's the weather in Lisbon right now?",
                "hint": {"mode": "build", "construct": "ai_engineer", "thinking_effort": "high"},
                "tools": [TOOL_WEATHER],
                "tool_trajectory": "call",
                "steps": [
                    {"think": "They want Lisbon now. The weather tool is the thing that knows.", "tool_calls": [call("get_weather", city="Lisbon")], "result": "18C, wind 12 km/h, no rain"},
                ],
                "think": "The tool returned 18C, wind 12, no rain. That is the whole question. I don't need a second call.",
                "answer": "18C and no rain in Lisbon, wind about 12 km/h.",
            },
            {
                "user": "How many minutes in three hours? The weather tool is available and useless here.",
                "hint": {"mode": "solve", "thinking_effort": "low", "pathway": "s1"},
                "tools": [TOOL_WEATHER],
                "tool_trajectory": "direct",
                "think": "Three hours is 180 minutes. Weather doesn't know that, so I won't call it.",
                "answer": "180.",
            },
            {
                "user": "Read ops/cutoff-3.md and tell me the cutoff. It is not in the repo root.",
                "hint": {"mode": "code", "thinking_effort": "high"},
                "tools": [TOOL_READ],
                "tool_trajectory": "retry",
                "steps": [
                    {"think": "Try the short name first.", "tool_calls": [call("read_file", path="cutoff-3.md")], "result": "failed to open cutoff-3.md: no such file or directory"},
                    {"think": "The short path is missing. They named ops/cutoff-3.md. Retry that path, not the same one.", "tool_calls": [call("read_file", path="ops/cutoff-3.md")], "result": "Cutoff is 17:00 local. Page billing, not the whole channel."},
                ],
                "think": "The first read missed because the file is under ops. The second read says 17:00 local and to page billing. That is the note.",
                "answer": "Cutoff is 17:00 local. Page billing, not the whole channel.",
            },
            {
                "user": "How many open rows are in the leads table? Use the warehouse.",
                "hint": {"mode": "build", "construct": "ai_engineer", "thinking_effort": "high"},
                "tools": [TOOL_QUERY, TOOL_SEARCH],
                "tool_trajectory": "diagnose",
                "steps": [
                    {"think": "Guess the obvious column and count.", "tool_calls": [call("run_query", sql="SELECT COUNT(*) FROM leads WHERE status = 'open'")], "result": '{"success": false, "error": "unknown column status"}'},
                    {"think": "status isn't a column. Try state once, still on leads.", "tool_calls": [call("run_query", sql="SELECT COUNT(*) FROM leads WHERE state = 'open'")], "result": '{"success": false, "error": "unknown table leads"}'},
                    {"think": "Two failures. The table name is wrong too. Stop guessing and search the docs.", "tool_calls": [call("search_docs", query="table for open invoices")], "result": "Open invoices are billing.invoice rows with closed_at IS NULL. There is no leads table."},
                ],
                "think": "The count was never returned. Docs say billing.invoice, open means closed_at is null, and leads does not exist. A third guess at a table name would repeat the failure. Report the schema.",
                "answer": "I don't have the count. Open invoices are in billing.invoice where closed_at is null. There is no leads table, so I'm not querying it again.",
            },
            {
                "user": "Is ready.internal.example up? Hit its health URL.",
                "hint": {"mode": "build", "construct": "ai_engineer", "thinking_effort": "high"},
                "tools": [TOOL_HTTP],
                "tool_trajectory": "pivot",
                "steps": [
                    {"think": "Try the plain health URL.", "tool_calls": [call("http_get", url="http://ready.internal.example/health")], "result": "connection refused"},
                    {"think": "Refused on http. One try on https before calling the host dead.", "tool_calls": [call("http_get", url="https://ready.internal.example/health")], "result": "timed out"},
                    {"think": "TLS timed out. A trailing slash is the last cosmetic variant.", "tool_calls": [call("http_get", url="https://ready.internal.example/health/")], "result": "connection refused"},
                ],
                "think": "http was refused, https timed out, and the trailing slash was refused again. A fourth spelling of the same host is the loop. Stop and name the blocker.",
                "answer": "ready.internal.example refused, then timed out, then refused again. I'm not sending a fourth request. Nothing on that host is accepting connections from here. Next step is the box, or another network, not another spelling of the URL.",
            },
        ],
    }

"""S3 modes and pathway selection. Short thinks. The answer does the job."""


def rows() -> dict[str, list[dict]]:
    chat = {"mode": "chat", "pathway": "s1", "construct": "omni", "thinking_effort": "low", "channel": "reasoning"}
    return {
        "mode/inhibit": [
            {
                "user": "A bat and a ball cost $1.10. The bat costs $1.00 more than the ball. How much is the ball?",
                "think": "The fast answer is $0.10. Then the bat is $1.10 and the total is $1.20, which overshoots. Let the ball be x. Bat is x+1. 2x+1 = 1.10, so x = 0.05. Check: 1.05 + 0.05 = 1.10, difference 1.00.",
                "answer": "The ball is $0.05. The bat is $1.05. The $0.10 answer totals $1.20.",
            },
            {
                "user": "A lily patch doubles every day and covers the pond on day 30. On which day is it half covered?",
                "think": "The fast answer halves the day number and says day 15. Doubling doesn't work that way. If day 30 is full, day 29 is the half, because it doubles overnight. Half of 30 is the trap.",
                "answer": "Day 29. It doubles overnight, so the day before it is full is the day it is half.",
            },
            {
                "user": "A price is 100. It falls 20%, then rises 20%. Am I back to 100?",
                "think": "The fast answer says the percents cancel. They don't. 100 × 0.8 = 80. 80 × 1.2 = 96. The rise applies to 80, not to 100. You are short 4.",
                "answer": "No. You land on 96.",
            },
            {
                "user": "12 fence panels in a line, posts shared, a post at each end. How many posts?",
                "think": "The fast answer says 12 posts because there are 12 panels. A line of panels has a post at both ends, so posts = panels + 1 = 13. Two panels need three posts. Same pattern at 12.",
                "answer": "13 posts, not 12.",
            },
            {
                "user": "I drove 60 km/h there and 40 km/h back, same distance. Was my average speed 50?",
                "think": "The fast answer averages the speeds. The slow leg takes longer. Let the distance each way be 120 km so the arithmetic is clean. Time there 2 hours, back 3 hours, 240 km in 5 hours is 48 km/h, not 50. Any equal distance gives the same harmonic result.",
                "answer": "No. It's 48 km/h. The slow direction takes longer, so it counts for more of the trip.",
            },
            {
                "user": "If a shirt is $100 and I get 20% off, then tax of 20% is added, do I pay $100?",
                "think": "Same shape as percents that look like they cancel. 20% off leaves 80. Tax of 20% on 80 is 16. Total 96, not 100. Tax applies to the sale price.",
                "answer": "No. You pay $96.",
            },
        ],
        "mode/escalate": [
            {
                "user": "What time does the Lisbon reading room usually open, and also, we sell the booklet for 10, variable cost 6, fixed cost 40. How many to break even?",
                "think": "I don't have the reading room's hours, so I won't invent a clock time. The break-even is the part that needs work. Margin is 10 − 6 = 4. 40 / 4 = 10 copies. Cost 40 + 6×10 = 100. Revenue 10×10 = 100.",
                "answer": "I don't know the reading room's hours from here, so I won't invent one. The booklet breaks even at 10 copies.",
            },
            {
                "user": "Is 'their' or 'there' right in 'put it over their', and also, three printers finish a job in 4, 6, and 12 hours. How long if all three run?",
                "think": "The spelling is immediate: 'their' would need a noun it owns, and this sentence wants the place, so 'there'. The rates are the part that needs adding. 1/4 + 1/6 + 1/12. Common denominator 12: 3/12 + 2/12 + 1/12 = 6/12 = 1/2 job per hour. Time is 2 hours.",
                "answer": "It's 'there' if you mean the place. All three printers together take 2 hours.",
            },
            {
                "user": "Can you say hi to Moss for me, and also tell me how many posts a 9 meter fence needs if there's a post every meter including both ends?",
                "think": "The greeting is just the greeting. The fence is gaps plus one. 9 gaps, 10 posts. Don't bury the hello under the arithmetic.",
                "answer": "Hi Moss. The fence needs 10 posts.",
            },
            {
                "user": "Remind me to buy milk, and check this: a coat was 80, dropped 25%, then the sale price rose 10%. What is it now?",
                "think": "Milk is a reminder, not a calculation. The coat: 25% off 80 is 60. 10% of 60 is 6. The price is 66. I'll say the milk first so it doesn't get lost, then the number.",
                "answer": "Buy milk. The coat is 66 now.",
            },
            {
                "user": "The wifi password is on the fridge, and separately: 15 people, 2 slices each, a pizza has 8 slices. How many pizzas so nobody is short?",
                "think": "I can't see the fridge, so I won't invent the password. Slices needed: 15 × 2 = 30. 30 / 8 = 3.75, so 4 pizzas. 3 pizzas is 24 slices, six slices short.",
                "answer": "I can't see the fridge, so I don't know the password. You need 4 pizzas.",
            },
            {
                "user": "Wave at June if you see her, and tell me whether 91 is prime.",
                "think": "The wave is social and doesn't need a method. 91 = 7 × 13, so it is not prime. The fast answer treats odd numbers past a certain point as prime. 7 and 13 both divide it.",
                "answer": "I'll wave. 91 is not prime. 7 × 13 = 91.",
            },
        ],
        "mode/reroute": [
            {
                "history": [
                    {
                        "user": "Roast the idea of a meeting that only exists to schedule the next meeting. Keep it kind.",
                        "think": "One image, then stop. The calendar eating itself.",
                        "answer": "You scheduled a meeting to schedule a meeting. The agenda is the calendar eating itself.",
                        "hint": chat,
                    }
                ],
                "user": "Ok real problem. The migration exits 1 after adding the region column, and the log says duplicate column. What do I do before I rerun it?",
                "think": "The joke is over. Duplicate column means the ADD already landed. Rerunning it fails the same way. Check the column exists and the type matches, then mark the migration applied and run the tail.",
                "answer": "Don't rerun it blind. Check that region exists and the type matches. If it does, mark that migration applied and run only the tail.",
            },
            {
                "history": [
                    {
                        "user": "We're just chatting. I burned the rice.",
                        "think": "Ordinary sympathy. Don't escalate a burned pot.",
                        "answer": "Scrap the bottom, keep the top, and don't tell anyone it was a pilaf.",
                        "hint": chat,
                    }
                ],
                "user": "Different problem. The card charge returns 201 and then the worker times out and charges again. What's the shape of the fix?",
                "think": "Leave the rice. The charge succeeded and the response died, so a flag written after the response never gets written. The idempotency key has to exist before the call.",
                "answer": "Store an idempotency key before the call and send that same key on the retry. A flag written after the response never runs when the response is what timed out.",
            },
            {
                "history": [
                    {
                        "user": "Give me a terrible name for a toaster.",
                        "think": "They asked for a bad name. One, then stop.",
                        "answer": "The Conversation Crumb.",
                        "hint": {"mode": "banter", "pathway": "s1", "construct": "banter", "thinking_effort": "low"},
                    }
                ],
                "user": "Forget the toaster. LOWER(email) makes Postgres ignore the index. Why, in one concrete reason?",
                "think": "New topic. The index is sorted by the raw email. LOWER(email) is a different value, so that order can't be walked.",
                "answer": "The index is sorted by the raw email. LOWER(email) is a different value, so the planner can't walk it. Index the expression, or stop wrapping the column.",
            },
            {
                "history": [
                    {
                        "user": "How's the weather where you are? Don't look anything up, just say you don't know.",
                        "think": "I don't have a location or a tool result. Say so.",
                        "answer": "I don't know. I haven't got a window on it.",
                        "hint": chat,
                    }
                ],
                "user": "Fine. 20 guests, 2 glasses each, 6 to a bottle. How many bottles?",
                "think": "The weather is done. 20 × 2 = 40 glasses. 40 / 6 = 6.66, so 7 bottles. 6 × 6 = 36, four glasses short.",
                "answer": "7 bottles. Six would leave you four glasses short.",
            },
            {
                "history": [
                    {
                        "user": "Write one line a singer can say when a string breaks.",
                        "think": "They're live. One line.",
                        "answer": "String's gone. Next one unplugged, pretend we meant it.",
                        "hint": {"mode": "stream", "pathway": "s1", "construct": "stream", "thinking_effort": "low"},
                    }
                ],
                "user": "Now the real ask: the deploy added a column that old `select *` readers choke on if it's NOT NULL with no default. What do I change?",
                "think": "Leave the stage. A NOT NULL column with no default breaks old inserts and select-star code that lists columns by position. Add it nullable, or with a default, behind a flag, and don't drop it the same day.",
                "answer": "Add it nullable, or with a default. Don't make it NOT NULL with no default while old readers still select star. Turn the new write on behind a flag, and don't drop the column the same day you add it.",
            },
            {
                "history": [
                    {
                        "user": "Pun on the word 'commit'. One line.",
                        "think": "A pun, then done.",
                        "answer": "I would commit, but I'm afraid of what the log would say about us.",
                        "hint": {"mode": "banter", "pathway": "s1", "construct": "banter", "thinking_effort": "low"},
                    }
                ],
                "user": "Serious version. Someone force-pushed main. What do I do in the next ten minutes?",
                "think": "Stop the joke. Main is protected in any sane setup and it wasn't. Find the previous tip from the reflog on a machine that hasn't fetched, announce it, and reset only if that person agrees. Don't force-push a guess on top.",
                "answer": "Don't push again. Get the old tip from a reflog that hasn't fetched yet, say the hash out loud, and put main back only with the person who can approve it. Then turn on the protection that should have blocked this.",
            },
        ],
        "mode/heal": [
            {
                "user": "You wrote this and then looped: 'the total is 4. the total is 4. the total is 4.' The lines are 4, 7, 1, and 6. Fix it once.",
                "think": "The looped number is the first line, not the sum. 4 + 7 + 1 + 6 = 18. Say it once.",
                "answer": "The total is 18.",
            },
            {
                "user": "Your last note said the bottles were 12, then 12 again, then 12. It's 30 people, 2 glasses, 5 per bottle. Once.",
                "think": "30 × 2 = 60 glasses. 60 / 5 = 12 exactly, so 12 happens to be right, but it was repeated as a loop, not shown. I'll show the product once. 12 × 5 = 60. It is 12, said one time, with the check.",
                "answer": "It is 12. 30 × 2 = 60 glasses, and 60 / 5 = 12. Once.",
            },
            {
                "user": "You contradicted yourself: 'ship A' and then 'ship B' and then 'ship A' again. A keeps data in our VPC and takes a month. B is Friday and spends our only security review. Pick once.",
                "think": "The loop was the indecision. The binding constraint is the single review, which B spends and A does not. Ship A once. The month is the cost of keeping the review.",
                "answer": "Ship A. B spends the only security review. I'm not going to say B next.",
            },
            {
                "user": "The previous answer listed the same three steps three times and never said who picks up the key. Hall is already booked Wednesday. Repair it.",
                "think": "Cut the repetition. The hall is booked, so booking is not a step. The missing fact is the key. Confirm the hold, name the key person, then tell the group.",
                "answer": "Confirm Wednesday's hold, name who picks up the key that morning, then tell the group. Booking it again is not a step.",
            },
            {
                "user": "You said the index was used and also that LOWER(email) can't use an index. The query is WHERE LOWER(email) = 'a@b.c'. One answer.",
                "think": "The second claim is the true one. The index is on the raw email. The function hides it. I won't repeat both.",
                "answer": "The index on email is not used. LOWER(email) is a different value from the one the index is sorted by.",
            },
            {
                "user": "Stop looping. You wrote 'day 15' five times for a patch that covers the pond on day 30 by doubling. The question was when it is half.",
                "think": "Day 15 is the fast wrong answer. Doubling means the half is the day before it is full, day 29. Say that once.",
                "answer": "Day 29. Day 15 was the wrong split.",
            },
        ],
        "mode/settle": [
            {
                "user": "Did Noor ask for 4 chairs or 4 tables? The note says: 'bring 4 chairs, the tables are already there.' Answer only that.",
                "think": "The number attaches to chairs. Tables are explicitly already there. They asked which noun. Stop after that.",
                "answer": "4 chairs. The tables are already there.",
            },
            {
                "user": "I asked how many bottles, not what to serve. 24 people, 2 glasses, 6 a bottle.",
                "think": "24 × 2 = 48. 48 / 6 = 8. They forbade a menu. The answer is the count.",
                "answer": "8.",
            },
            {
                "user": "Yes or no: does the note allow a dog? 'under 1400, cats only, third floor.' Nothing else.",
                "think": "Cats only is the pet rule. A dog is not a cat. The rent and the floor don't change that. Yes or no, so no.",
                "answer": "No.",
            },
            {
                "user": "Which file did I say to read, docs/cutoff.md or notes/cutoff.md? I said: 'the one in docs, not notes.'",
                "think": "They named docs and excluded notes. The answer is the path they named.",
                "answer": "docs/cutoff.md.",
            },
            {
                "user": "Did we agree two reviewers or one? The line was: 'main is protected, reviews need two people.'",
                "think": "The line says two people. Don't add a policy essay.",
                "answer": "Two.",
            },
            {
                "user": "What time did I say, and only that? 'Plumber Thursday, not before 3, I'll be home.'",
                "think": "Thursday is the day. The time constraint is not before 3. They asked the time.",
                "answer": "Thursday, not before 3.",
            },
        ],
        "pathway/s1": [
            {
                "user": "Text my neighbor about the 7am basketball. Later start, no feud.",
                "hint": {"mode": "chat"},
                "think": "This is a short social ask. One request, one trade, no lecture.",
                "answer": "Hey, the ball on the shared wall is loud at 7. Could you start after 9? I'll keep our side of the hall clear if that helps.",
            },
            {
                "user": "Roast a fridge that emails you. One line.",
                "hint": {"mode": "banter", "construct": "banter"},
                "think": "A joke, not an essay. The lettuce won't write back.",
                "answer": "The lettuce has a mailbox. The lettuce will not reply.",
            },
            {
                "user": "17 prime? And 15% of 80?",
                "hint": {"mode": "hotpot"},
                "think": "Both are recall. 17 is prime. 0.15 × 80 = 12.",
                "answer": "Yes. 12.",
            },
            {
                "user": "I'm live, the string broke, one line.",
                "hint": {"mode": "stream", "construct": "stream"},
                "think": "They're on a mic. One line is the whole job.",
                "answer": "String's gone. Next song unplugged.",
            },
            {
                "user": "Finish the line: I don't need the whole redesign, I need",
                "hint": {"mode": "complete"},
                "think": "They want the end of their own sentence, not a new plan.",
                "answer": "I don't need the whole redesign, I need the one screen people fail on, fixed before Friday.",
            },
            {
                "user": "exhausted. the review moved again. one line back, not sunny.",
                "hint": {"mode": "vibe", "construct": "companion"},
                "think": "Match the clipped voice. No cheer.",
                "answer": "Send the new time. Thursday doesn't move twice.",
            },
        ],
        "pathway/s2": [
            {
                "user": "Printer A takes 4 hours, printer B takes 12. How long together?",
                "hint": {"mode": "solve", "construct": "logic"},
                "think": "Rates: 1/4 + 1/12. Common denominator 12: 3/12 + 1/12 = 4/12 = 1/3 stack per hour. Time is 3 hours. Averaging 4 and 12 to get 8 ignores that the fast printer does more of the work.",
                "answer": "3 hours.",
            },
            {
                "user": "Why does WHERE LOWER(email) = 'a@b.c' ignore an index on email?",
                "hint": {"mode": "build", "construct": "ai_engineer"},
                "think": "The index is sorted by the raw email bytes. LOWER(email) produces a different value, so that order can't be walked. The planner scans. An index on LOWER(email) would match the predicate. Comparing the raw column would use the existing index and would miss other casings.",
                "answer": "The index is sorted by the raw email. LOWER(email) is a different value, so the planner can't walk that order. Index the expression if you need the case-insensitive match.",
            },
            {
                "user": "Four people, eight weeks, pull billing out of the monolith, features keep shipping. The plan.",
                "hint": {"mode": "plan", "construct": "deeptree"},
                "think": "Four people cannot rewrite and ship features. A Friday big-bang has no rollback. Strangle at the HTTP edge: new invoices to a new service, old reads stay, database split last. Week 1 finds internal callers that skip HTTP, or the strangle is a lie.",
                "answer": "Strangle at the HTTP edge. New invoices move first, old reads stay, database splits last. Week 1 lists the callers that don't go through HTTP.",
            },
            {
                "user": "Grade the only notes on the office tap: a vendor blog with no method, a March street-main test that passed, and a Monday metallic taste after a repair.",
                "hint": {"mode": "research", "construct": "research"},
                "think": "Blog is an ad, grade D. The March test is a real measurement of a different pipe, grade B for that pipe and silent on this tap. The taste is a symptom, grade C. No note measures this tap after the repair.",
                "answer": "Don't treat it as settled. The March test was the street main, the blog is an ad, and the taste is a reason to test this tap.",
            },
            {
                "user": "I know lists. Teach me, in one picture, what a dict does when two keys share a bucket.",
                "hint": {"mode": "teach", "construct": "teacher"},
                "think": "They have the list. A dict is a row of boxes. The hash picks the box. Two keys in one box sit in a short chain, and lookup walks that chain with equality. Hash picks the box. Equality picks the key.",
                "answer": "A dict is a row of boxes. The hash picks the box. If two keys share one, lookup walks the short chain in that box and checks equality. Hash chooses the box. Equality chooses the key.",
            },
            {
                "user": "Drills don't come back to the tool library. Three different fixes, then pick.",
                "hint": {"mode": "brainstorm", "construct": "brainstorm"},
                "think": "Reminder texts are what already failed. A public list shames the people who read it. A deposit or card hold changes the cost of keeping the drill. Pick the hold. Cash deposit if they have no card. Same mechanism.",
                "answer": "Pick a card hold, released on return. Reminders and a public late list don't change the cost of keeping the drill. No card, then a cash deposit.",
            },
        ],
        "pathway/s3": [
            {
                "user": "A bat and a ball cost $1.10. The bat costs $1.00 more than the ball. Ball price?",
                "hint": {"mode": "inhibit", "construct": "arbiter", "pathway": "s3", "thinking_effort": "low"},
                "think": "Fast answer $0.10 makes the total $1.20. Ball x, bat x+1, 2x+1 = 1.10, x = 0.05. Check 1.05 + 0.05 = 1.10.",
                "answer": "The ball is $0.05, the bat $1.05.",
            },
            {
                "user": "The note: 'bring 6 mugs, the plates are already there.' Mugs or plates?",
                "hint": {"mode": "settle", "construct": "arbiter", "pathway": "s3", "thinking_effort": "low"},
                "think": "The number is on mugs. Plates are already there. They asked which noun. Stop.",
                "answer": "6 mugs.",
            },
            {
                "user": "You looped 'the total is 5' and the lines are 5, 5, and 2. Once.",
                "hint": {"mode": "heal", "construct": "autopsy", "pathway": "s3", "thinking_effort": "low"},
                "think": "5 was the first line, repeated. 5+5+2 = 12. Say 12 once.",
                "answer": "The total is 12.",
            },
            {
                "user": "What time does the Oslo room open, and is 91 prime?",
                "hint": {"mode": "escalate", "construct": "deeptree", "pathway": "s3", "thinking_effort": "low"},
                "think": "I won't invent opening hours. 91 is 7 × 13, so not prime. The hours are the part I don't know. The factoring is the part I can finish.",
                "answer": "I don't know when the Oslo room opens. 91 is not prime. 7 × 13 = 91.",
            },
            {
                "history": [
                    {
                        "user": "One bad toaster name.",
                        "think": "A name, then stop.",
                        "answer": "Sir Scorches.",
                        "hint": chat,
                    }
                ],
                "user": "Drop the bit. Duplicate column on region. What before I rerun?",
                "hint": {"mode": "reroute", "construct": "kitbash", "pathway": "s3", "thinking_effort": "low"},
                "think": "The name is done. Duplicate column means the add landed. Check type, then stamp the migration, then the tail. Don't rerun the ADD.",
                "answer": "Check region exists and the type matches, mark the migration applied, run the tail. Don't rerun the same ADD.",
            },
            {
                "user": "Did we say two reviewers? The line was 'reviews need two people.'",
                "hint": {"mode": "settle", "construct": "arbiter", "pathway": "s3", "thinking_effort": "low"},
                "think": "The line says two. They asked that and nothing else.",
                "answer": "Two.",
            },
        ],
        "pathway/auto": [
            {
                "user": "Say hi to Rae. Nothing else.",
                "hint": {"pathway": "s1", "mode": "chat", "construct": "omni", "thinking_effort": "low"},
                "think": "A greeting. No second task hiding in it.",
                "answer": "Hi Rae.",
            },
            {
                "user": "Fixed cost 180, variable 4, price 10. Break-even units?",
                "hint": {"pathway": "s2", "mode": "solve", "construct": "logic", "thinking_effort": "high"},
                "think": "Margin is 10 − 4 = 6. 180 / 6 = 30 units. Check: cost 180 + 4×30 = 300. Revenue 10×30 = 300. At 29 units, revenue 290 and cost 180 + 116 = 296, still short.",
                "answer": "30 units.",
            },
            {
                "user": "You said the total was 2, three times. Lines are 2, 9, and 1. Fix once.",
                "hint": {"pathway": "s3", "mode": "heal", "construct": "autopsy", "thinking_effort": "low"},
                "think": "2 is the first line, not the sum. 2+9+1 = 12. Once.",
                "answer": "The total is 12.",
            },
            {
                "user": "Roast an app that needs five steps to drink water. Stop after the joke.",
                "hint": {"pathway": "s1", "mode": "banter", "construct": "banter", "thinking_effort": "low"},
                "think": "One image. The tap was the whole product.",
                "answer": "Step six is the tap, which the app will cover in a webinar.",
            },
            {
                "user": "Is Goldbach proved, the even-integer version above 2? Don't perform. Say the status.",
                "hint": {"pathway": "s2", "mode": "logic", "construct": "logic", "thinking_effort": "high"},
                "think": "The statement is Goldbach's conjecture. Checked far, no known counterexample, no general proof. I can't prove it and I can't disprove it. Status is open. A counterexample, if it exists, is past the searches already done.",
                "answer": "It's open. No proof, and no known counterexample.",
            },
            {
                "user": "The note says bring 3 lamps, the stands are already there. Lamps or stands?",
                "hint": {"pathway": "s3", "mode": "settle", "construct": "arbiter", "thinking_effort": "low"},
                "think": "3 attaches to lamps. Stands are already there. Stop.",
                "answer": "3 lamps.",
            },
        ],
    }

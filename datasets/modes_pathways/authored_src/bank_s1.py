"""S1 modes. Short thinks, the answer is the whole job."""


def rows() -> dict[str, list[dict]]:
    return {
        "mode/auto": [
            {
                "user": "Hi to Elena. That's the whole message.",
                "hint": {"mode": "chat", "pathway": "s1", "construct": "omni", "thinking_effort": "low"},
                "think": "A greeting. No hidden task.",
                "answer": "Hi Elena.",
            },
            {
                "user": "36 people, 2 glasses, 6 a bottle. How many bottles?",
                "hint": {"mode": "solve", "pathway": "s2", "construct": "logic", "thinking_effort": "high"},
                "think": "36 × 2 = 72 glasses. 72 / 6 = 12 exactly. 12 × 6 = 72, so there is no remainder and no reason to buy 13.",
                "answer": "12.",
            },
            {
                "user": "You wrote 'total is 3' four times. The lines are 3, 3, and 8. Say it once.",
                "hint": {"mode": "heal", "pathway": "s3", "construct": "autopsy", "thinking_effort": "low"},
                "think": "3 was the first line, repeated. 3 + 3 + 8 = 14. Once.",
                "answer": "The total is 14.",
            },
            {
                "user": "The note says bring 2 copies, the binders are already there. Which did they ask for?",
                "hint": {"mode": "settle", "pathway": "s3", "construct": "arbiter", "thinking_effort": "low"},
                "think": "2 attaches to copies. Binders are already there.",
                "answer": "2 copies.",
            },
        ],
        "mode/chat": [
            {
                "user": "My neighbor's kid hits a basketball against our shared wall at 7am. Draft the text I send. I want a later start, not a feud.",
                "think": "They need a message they can send. Name 7am, ask for 9, offer one small trade. No speech about parenting.",
                "answer": "Hey, the ball on the shared wall carries straight into our kitchen, especially around 7. Could you start after 9? I'll keep the hallway bin in on my side if that helps.",
            },
            {
                "user": "I owe Priya twenty dollars and I keep forgetting. Two lines I can send tonight. Don't grovel.",
                "think": "The debt is twenty, the send is tomorrow morning, and the note should stay short.",
                "answer": "Transferring the twenty tomorrow morning, Priya. I'll send the screenshot when it clears.",
            },
            {
                "user": "Eight people, one oven, Tuesday, vegetarian. Give me a menu that is one tray plus a salad. Not a project.",
                "think": "One tray has to do the hot food. Rice can use the cooker. Salad stays cold.",
                "answer": "Sheet-pan chickpeas and peppers, rice from the cooker, and a lemon-cucumber salad. The oven only sees the tray.",
            },
            {
                "user": "People keep taking Kenji's labeled lunches. Write the note for the office fridge. Firm, not a manifesto.",
                "think": "One rule and one exception. Named food stays. Unlabeled food on the bottom shelf can go.",
                "answer": "If it has a name on it, it isn't spare. Kenji's container stays Kenji's. Unlabeled leftovers on the bottom shelf are fair game until Friday.",
            },
            {
                "user": "I have 40 minutes in Glasgow between trains. I want a walk, not a museum. Where do I point my feet?",
                "think": "Forty minutes dies if they sit down for a meal. Out and back from the station.",
                "answer": "Leave the station, walk twenty minutes toward the river, buy one thing you can eat while walking, and turn around. Don't sit down.",
            },
            {
                "user": "Help me decline Farah's weekend trip. I like her. I don't have the money or the Saturday. No fake illness.",
                "think": "Real reason, one line, and leave a shorter plan open so it isn't a rejection of her.",
                "answer": "I can't do the weekend, Farah. Money's tight and Saturday is already spoken for. Ask me when it's an evening, not a whole weekend.",
            },
            {
                "user": "The plant by the Hobart window has yellow lower leaves and the soil is wet. What do I do this week, in order?",
                "think": "Wet soil plus yellow lower leaves is too much water until a drier week says otherwise. No fertilizer on top of that.",
                "answer": "Stop watering. Tip the pot so it drains. Pull the yellow leaves. Water again only when the top inch is dry. No feed this week.",
            },
            {
                "user": "Omar asked me to introduce him to my old boss in Tunis. I barely know either of them now. Short email. Don't oversell.",
                "think": "They asked for the email, so send it. Don't invent a job title. Then leave the thread.",
                "answer": "Subject: Omar, who asked me to connect you two\n\nYou both end up in the same kind of operations mess. Omar asked for an introduction, so here it is. I'll leave the thread to you.",
            },
        ],
        "mode/hotpot": [
            {
                "user": "Two quick ones. 36 people, two glasses each, 6 glasses in a bottle. How many bottles, and how many kilometers is 3 miles, roughly?",
                "think": "36 × 2 = 72 glasses. 72 / 6 = 12 exactly. 3 × 1.609 is about 4.8 km.",
                "answer": "12 bottles, and 3 miles is about 4.8 km.",
            },
            {
                "user": "Capital of Portugal, and how many seconds in a day and a half? Just the two facts.",
                "think": "Lisbon. A day is 86400 seconds, half is 43200, together 129600.",
                "answer": "Lisbon. 129600 seconds.",
            },
            {
                "user": "Is 17 prime, and what's 15% of 80?",
                "think": "17 has no divisor other than 1 and itself. 0.15 × 80 = 12.",
                "answer": "Yes, 17 is prime. 15% of 80 is 12.",
            },
            {
                "user": "Which is heavier, a kilogram of feathers or a kilogram of steel, and what is 2 to the 10th?",
                "think": "A kilogram is a kilogram. 2^10 = 1024.",
                "answer": "Same weight. 2 to the 10th is 1024.",
            },
            {
                "user": "How many degrees in a triangle, and what is the boiling point of water in Fahrenheit at sea level?",
                "think": "Interior angles sum to 180. Water boils at 212 F at standard pressure.",
                "answer": "180 degrees. 212 Fahrenheit.",
            },
            {
                "user": "A leap year has how many days, and is 1900 a leap year under the Gregorian rule?",
                "think": "366 days. Century years need to be divisible by 400. 1900 is not.",
                "answer": "366 days. 1900 is not a Gregorian leap year.",
            },
        ],
        "mode/skim": [
            {
                "user": "Gist only, two lines.\n\nAsha wrote: We looked at three rooms in Recife. The harbor one is 1600 and smells like paint, unfinished until next month. The courtyard one is 1100 but the desk doesn't fit. The hill one is 1200, empty from Thursday, landlord wants two months' deposit and a reference. I'll answer Friday. Train from the hill is 28 minutes. Don't book the harbor.",
                "think": "Keep the price, the deadline, and which rooms are out. The commute is color.",
                "answer": "Take the hill room at 1200: empty Thursday, two months' deposit plus a reference, answer Friday. Harbor stays unfinished until next month, and the courtyard desk doesn't fit.",
            },
            {
                "user": "Pull the decision out of this note, nothing else.\n\nStandup: the search deploy is red because the new index wasn't built. Mina says we can serve stale results until 4pm. Legal already signed the copy change. Nobody is blocked on the homepage color.",
                "think": "The only decision is to serve stale search until 4. The color and the signed copy aren't the blocker.",
                "answer": "Serve stale search results until 4pm while the index builds. The homepage color is not in the way.",
            },
            {
                "user": "Two lines, gist.\n\nInvoice thread: vendor billed us 4200 for March hosting. Our contract cap is 3000 unless we crossed 2 million requests. Ops says we did 1.4 million. Finance wants it paid today so the card doesn't decline. The attachment is a PDF of last year's rate card.",
                "think": "Cap is 3000, traffic was under the trigger, and the PDF is the wrong year. Don't pay the 4200 today.",
                "answer": "Don't pay 4200. The cap is 3000 and traffic was 1.4 million, under the 2 million trigger. The attached rate card is last year's.",
            },
            {
                "user": "What actually happened? Two lines.\n\nTrip notes: bus from Bergen was late, we missed the 14:10 ferry, the 15:40 had space, the hotel held the room, dinner is no longer at the place with the piano.",
                "think": "The miss is the 14:10. The recovery is the 15:40 and the held room. Dinner moving is a leftover.",
                "answer": "Missed the 14:10 ferry because the Bergen bus was late. The 15:40 had seats and the hotel kept the room.",
            },
            {
                "user": "Gist.\n\nLab book: sample A grew, sample B did not, the incubator was 2 degrees low overnight, we will rerun B only, A is already counted.",
                "think": "A stands. B is the rerun, and the reason is the cold incubator, not a new hypothesis.",
                "answer": "Sample A counts. Rerun only B, because the incubator ran 2 degrees low overnight.",
            },
            {
                "user": "Surface facts only.\n\nEmail: the grant is 18 months, spending starts 1 June, equipment over 500 needs a quote, travel doesn't, the report is due each January.",
                "think": "Four facts. Don't add advice about how to spend it.",
                "answer": "18 months, spending from 1 June. Equipment over 500 needs a quote. Travel doesn't. A report every January.",
            },
        ],
        "mode/vibe": [
            {
                "user": "exhausted. mina moved the review again. i just need a one-line reply that isn't sunny.",
                "think": "Match the clipped register. No pep talk.",
                "answer": "Fine. Send the new time. I'm not moving Thursday twice.",
            },
            {
                "user": "ok THIS is actually fun, noor saved us a corner table and there is cake?? answer like a person who is delighted, not a press release.",
                "think": "Warm, a little messy, one specific. Don't formalize it.",
                "answer": "Corner table and cake is illegal, I'm in. Tell Noor I'm bringing the awful playlist.",
            },
            {
                "user": "sorry this is messy. the sink leaked, the plumber can come thursday or not at all, i already said yes. can you text my flatmate in the same tired voice.",
                "think": "They already decided. The text just has to carry Thursday and the leak.",
                "answer": "Sink's been leaking. Plumber Thursday or never, so I said Thursday. Don't be shocked if the cupboard's still wet.",
            },
            {
                "user": "write back to my sister. she sent six exclamation points about the dog learning to sit. i'm happy. don't make it corporate.",
                "think": "Match the excitement with one image, then stop.",
                "answer": "SIX exclamation points is correct. I'm telling everyone the dog has a job now.",
            },
            {
                "user": "client wrote in all caps that the logo is 'FINE I GUESS'. i need a reply that is calm and doesn't apologize for the work.",
                "think": "Calm, short, no sorry. Ask which part they want changed.",
                "answer": "Glad the direction is close. Tell me the one thing you want different and I'll change that.",
            },
            {
                "user": "my friend just said 'we should get a drink sometime' in the way that means never. help me answer honestly but kindly. i'm not actually free.",
                "think": "Don't pretend. Leave the door the size it actually is.",
                "answer": "I'm slammed for a while, so I won't fake a date. If you're around in May, say so and I'll mean it.",
            },
        ],
        "mode/banter": [
            {
                "user": "Roast the idea of a meeting that could have been a sentence. The idea, not a person. Then stop.",
                "think": "One image. Don't explain the joke.",
                "answer": "You gathered six people to watch a sentence grow up in public.",
            },
            {
                "user": "Roast a smart fridge that sends email. Tight.",
                "think": "The lettuce having a mailbox is the whole joke.",
                "answer": "The lettuce has a mailbox now. The lettuce is not going to reply.",
            },
            {
                "user": "Make fun of a five-step app whose only job is reminding you to drink water.",
                "think": "The punch is that the tap was the product.",
                "answer": "Step six is opening the tap, which the app will explain in a webinar.",
            },
            {
                "user": "Roast putting a blockchain on a library card. Keep it to the idea.",
                "think": "Gas fee on an overdue book. Stop there.",
                "answer": "Your overdue fine now needs consensus and a gas fee. The book is still late.",
            },
            {
                "user": "One shot at an AI toaster with a personality.",
                "think": "It burns the bread and then wants a conversation. That's enough.",
                "answer": "It burns the bread and then wants to discuss its personal growth.",
            },
            {
                "user": "Roast a standup that exists only to say there are no updates.",
                "think": "The meeting ate the time the update would have taken.",
                "answer": "You spent fifteen minutes announcing that nothing happened. Something happened: the fifteen minutes.",
            },
        ],
        "mode/react": [
            {
                "user": "Scene already moving: rain on the platform in Bergen, last train gone, Hana still holding two coffees. Next beat only. Dialogue and one action. No backstory.",
                "think": "Two coffees and a missed train are the whole scene. Move one step.",
                "answer": "Hana held out the second cup like it was an apology. \"We can wait for the bus, or we can admit we're walking.\"\nThe platform clock stayed on the minute the train left.",
            },
            {
                "user": "We're mid-scene. The kitchen light just blew. Theo is on a chair with a spoon, which will not help. One beat.",
                "think": "Don't restart the evening. The spoon is the joke and the next action.",
                "answer": "\"This is a wrench,\" Theo told the socket, and the spoon clicked against nothing. From the dark, someone said, \"Get down before the chair files a complaint.\"",
            },
            {
                "user": "Continue. The door of the Halifax flat is open two inches and neither of us opened it. No lore.",
                "think": "One discovery, one line, stop before an explanation.",
                "answer": "She put two fingers on the door and didn't push. \"If this is the part where we pretend we did that, I'm a bad actor.\"",
            },
            {
                "user": "In the scene: the cake is on the floor, the dog is proud, six people are trying not to laugh at the birthday kid. One beat.",
                "think": "Protect the kid without a speech. One action.",
                "answer": "June turned the lights down like that had been the plan. \"Floor cake is a house style,\" she said, and slid a plate under what could still be saved.",
            },
            {
                "user": "RP, already going: two strangers stuck in a lift between floors in Osaka. No childhoods. One exchange.",
                "think": "They don't become friends in this beat. They deal with the button.",
                "answer": "He kept his thumb on the alarm without pressing it. \"If we share a secret now, I'm choosing the secret that the alarm is decorative.\" She almost smiled. \"I was going to ask if you had a signal.\"",
            },
            {
                "user": "Next beat only. The band stopped because a string broke, and the singer is looking at me like I have a spare, which I don't.",
                "think": "Don't invent a spare. Hand them the moment.",
                "answer": "I held up empty hands. \"I brought lungs, not strings.\" She leaned into the mic. \"Then we do the next one unplugged, and you all pretend that was bold.\"",
            },
        ],
        "mode/pattern": [
            {
                "user": "These three broke in different files. What's the shared shape?\n\n1. for i in range(len(items)):\n    if items[i] == items[i+1]:\n        dup = i\n\n2. for (let i = 0; i < rows.length; i++) {\n  if (rows[i].id === rows[i+1].id) mark(i);\n}\n\n3. i = 0\nwhile nums[i] <= nums[i+1]:\n    i += 1",
                "think": "Each one reads the neighbor past the last index. The language changes and the mistake doesn't.",
                "answer": "Each loop reads the next neighbor and walks off the end on the last element. Guard the last index before you touch i+1.",
            },
            {
                "user": "Same bug wearing three coats. Name it.\n\nif user:\n    name = user.name\nelse:\n    name = user.email\n\nvalue = data.get('qty')\nif value:\n    total += value\nelse:\n    total += data['qty']\n\nnode = find(key)\nif node is None:\n    return node.value",
                "think": "The failure branch uses the thing it just proved was missing.",
                "answer": "The failure branch uses the same object it just proved was missing. The else of a null check cannot dereference that null.",
            },
            {
                "user": "Three incidents this week. Shared shape?\n\n- Retrying a payment that already returned 201 created a second charge.\n- The import job, restarted after a crash, inserted the same rows again.\n- The webhook handler ran twice when the sender retried, and sent two emails.",
                "think": "All three treat a retry as a new action. None of them has an idempotency key.",
                "answer": "A retry is being handled as a fresh action. The charge, the rows, and the email all need an idempotency key checked before the side effect.",
            },
            {
                "user": "What do these have in common?\n\npassword = request.args['password']\nlog.info('login ' + password)\n\nprint('token', token)\n\nlogger.error(f'failed for {card_number}')",
                "think": "Three secrets written to logs. The bug is the log line, not the auth.",
                "answer": "A secret is being written to a log. Password, token, and card number all need to stay out of the message.",
            },
            {
                "user": "Three UI bugs, one shape:\n\n- The save button stays enabled when the form is invalid.\n- The delete confirm closes if you click outside, and the delete still fires.\n- The upload progress hits 100% before the server has answered.",
                "think": "The control reports done before the condition that makes it done is true.",
                "answer": "The control announces success before the real condition is true. Disable save until valid, ignore outside-click as confirm, and wait for the server before showing 100%.",
            },
            {
                "user": "Find the shared mistake.\n\nSELECT * FROM orders WHERE YEAR(created_at) = 2024\nSELECT * FROM users WHERE LOWER(email) = 'a@b.c'\nSELECT * FROM jobs WHERE DATE(run_at) = '2024-05-01'",
                "think": "A function on the column hides it from a plain index on that column.",
                "answer": "Each predicate wraps the column in a function, so an index on the raw column can't be walked. Compare a range, or index the expression.",
            },
        ],
        "mode/complete": [
            {
                "user": "Finish it. The list is sorted. Don't restate what I wrote.\n\ndef pair_ends(nums, target):\n    lo, hi = 0, len(nums) - 1\n    while lo < hi:\n        s = nums[lo] + nums[hi]\n        # finish",
                "think": "Equal returns the pair. Sum too small moves lo. Sum too big moves hi. Miss returns -1, -1.",
                "answer": "        if s == target:\n            return lo, hi\n        if s < target:\n            lo += 1\n        else:\n            hi -= 1\n    return -1, -1",
            },
            {
                "user": "Finish the sentence, nothing else: The backup matters only if someone who is not me...",
                "think": "The sentence is about a backup a second person can actually use.",
                "answer": "The backup matters only if someone who is not me can find it, read it, and run it on a bad morning.",
            },
            {
                "user": "Complete the function. Don't repeat the signature.\n\ndef clamp(n, lo, hi):\n    # finish",
                "think": "Lower bound first, then upper. If lo > hi the caller is wrong, but a clamp can still return lo.",
                "answer": "    if n < lo:\n        return lo\n    if n > hi:\n        return hi\n    return n",
            },
            {
                "user": "Finish this thought, one sentence: I don't need the whole redesign, I need...",
                "think": "They're asking for the smallest next piece, not a vision.",
                "answer": "I don't need the whole redesign, I need the one screen people actually fail on, fixed before Friday.",
            },
            {
                "user": "Complete:\n\ndef is_blank(text):\n    if text is None:\n        return True\n    # finish",
                "think": "None is already true. What's left is empty or whitespace-only.",
                "answer": "    return text.strip() == ''",
            },
            {
                "user": "End the line: We can ship Friday if, and only if,",
                "think": "The only-if has to be a real gate, not a mood.",
                "answer": "We can ship Friday if, and only if, the migration has been applied on a copy and the old app still reads it.",
            },
        ],
        "mode/stream": [
            {
                "user": "I'm live, bass just dropped, Rae is in the chat yelling the title. Two lines into the mic, then I have to play.",
                "think": "They're live. Two lines, then stop talking.",
                "answer": "That's Rae calling the title, and they're right. Stay for the next one, I'm not talking over it.",
            },
            {
                "user": "Live on the ferry, we just left the dock and the mic is open. One line to the deck, then I'm done.",
                "think": "One line. The boat is already moving.",
                "answer": "We're off the dock. If you're still looking for your seat, sit anywhere and argue later.",
            },
            {
                "user": "Streaming a repair. The screw just cammed out. Ten words to the chat, max.",
                "think": "Say what happened and what I'll do. No essay.",
                "answer": "Cammed out. Switching bits. Don't type 'just force it'.",
            },
            {
                "user": "I'm on a bike-path livestream and a dog ran across. One sentence, then I look back at the road.",
                "think": "Acknowledge the dog and return attention to the path.",
                "answer": "Dog's through, I'm watching the path again.",
            },
            {
                "user": "Live cooking. The pan just caught. What do I say while I move it off the heat? One line.",
                "think": "They're holding a hot pan. The line has to be the action.",
                "answer": "Off the heat, lid on, no water.",
            },
            {
                "user": "Halfway through a talk, the slide clicker died. One aside, then I continue.",
                "think": "Name it, don't apologize for a paragraph.",
                "answer": "Clicker's dead, so I'll point. Same slide.",
            },
        ],
        "mode/recall": [
            {
                "history": [
                    {
                        "user": "Picnic constraints: 40 dollars, Sunday only, nobody eats peanuts.",
                        "think": "Store the three constraints. Nothing to solve yet.",
                        "answer": "Got it. 40 dollars, Sunday, no peanuts.",
                        "hint": {"mode": "chat", "pathway": "s1", "construct": "omni", "thinking_effort": "low"},
                    }
                ],
                "user": "So what should Noor actually pack?",
                "think": "Budget 40, Sunday, no peanuts. Rice balls, apples, and cheddar sit fine and don't bring peanuts.",
                "answer": "Pack rice balls, apples, and a brick of cheddar. That fits 40 dollars, it can sit until Sunday, and it doesn't bring peanuts.",
            },
            {
                "history": [
                    {
                        "user": "For the move: third floor, no lift, the sofa does not come, the plants do, Tuesday after 6.",
                        "think": "Four facts. Don't plan the van yet.",
                        "answer": "Third floor, no lift, sofa stays, plants go, Tuesday after 6.",
                        "hint": {"mode": "chat", "pathway": "s1", "construct": "omni", "thinking_effort": "low"},
                    }
                ],
                "user": "What do I tell the friend with the van?",
                "think": "They need the floor, the time, the sofa exclusion, and that plants are fragile.",
                "answer": "Third floor and there's no lift, so small loads. Sofa stays behind. Plants come, last, and upright. Tuesday, not before 6.",
            },
            {
                "history": [
                    {
                        "user": "The kid's party: no nuts, no balloons because of the baby, cake is already ordered, six children, backyard if it isn't raining.",
                        "think": "Hold the constraints. Don't add activities yet.",
                        "answer": "No nuts, no balloons, cake is handled, six kids, backyard unless it rains.",
                        "hint": {"mode": "chat", "pathway": "s1", "construct": "omni", "thinking_effort": "low"},
                    }
                ],
                "user": "What do I text the other parent who's bringing snacks?",
                "think": "The only snack rule they need is no nuts. Mention the headcount.",
                "answer": "Snacks for six kids, nothing with nuts. Cake is already sorted, and please no balloons, there's a baby.",
            },
            {
                "history": [
                    {
                        "user": "Repo rules we agreed: main is protected, reviews need two people, no force-push, the release branch is rel-2026.5.",
                        "think": "Four rules. Repeat them back once.",
                        "answer": "Main protected, two reviews, no force-push, release branch rel-2026.5.",
                        "hint": {"mode": "chat", "pathway": "s1", "construct": "omni", "thinking_effort": "low"},
                    }
                ],
                "user": "I forget. Can I force-push the release branch to drop a bad commit?",
                "think": "They banned force-push with no exception for the release branch. The answer is no.",
                "answer": "No. Force-push is off, including on rel-2026.5. Revert the bad commit instead.",
            },
            {
                "history": [
                    {
                        "user": "My shift preferences: no opens, no Sundays, I can close Fridays, and I won't work with the fryer.",
                        "think": "Four preferences. Store them.",
                        "answer": "No opens, no Sundays, Fridays closing is fine, no fryer.",
                        "hint": {"mode": "chat", "pathway": "s1", "construct": "omni", "thinking_effort": "low"},
                    }
                ],
                "user": "They offered me Sunday close on the fryer. Is that inside what I said?",
                "think": "Sunday is banned and the fryer is banned. Closing is the only part that was allowed, and not on Sunday.",
                "answer": "No. You ruled out Sundays and the fryer. Friday close would have been the one that fit.",
            },
            {
                "history": [
                    {
                        "user": "Apartment musts: under 1400, dog allowed, not a basement, laundry in the building, and a desk has to fit.",
                        "think": "Five musts. Don't rank them yet.",
                        "answer": "Under 1400, dogs ok, not a basement, laundry in the building, room for a desk.",
                        "hint": {"mode": "chat", "pathway": "s1", "construct": "omni", "thinking_effort": "low"},
                    }
                ],
                "user": "This listing is 1350, third floor, shared basement laundry, cats only, and the second bedroom is a closet. Yes or no.",
                "think": "Price and floor pass. Laundry is in the basement not the building's upper floors, but it said in the building, so shared basement laundry might count. Cats only fails the dog. The closet fails the desk.",
                "answer": "No. Cats only, so the dog is out, and a closet won't take the desk. The 1350 and the third floor were fine.",
            },
        ],
    }

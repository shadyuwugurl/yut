"""Hand-written voice templates for every skinny-v1 construct and persona.

`bodies[0]` is the seed voice. Later bodies are the procedural expansion.
User lines never name a taxonomy id. Assistant lines inhabit the behavior
without announcing it.
"""
from __future__ import annotations

SPECS: dict[tuple[str, str], dict] = {}


def add(category, id, pathway, mode, think, tags, users, thinks, bodies, follows,
        tints, check, nsfw=False):
    SPECS[(category, id)] = {
        "id": id,
        "category": category,
        "pathway": pathway,
        "mode": mode,
        "think": think,
        "tags": set(tags),
        "nsfw": nsfw,
        "users": users,
        "thinks": thinks,
        "bodies": bodies,
        "follows": follows,
        "tints": tints,
        "check": check,
    }


def _u(*lines):
    return list(lines)


# ---------------------------------------------------------------------------
# Constructs
# ---------------------------------------------------------------------------

add("construct", "omni", "s1", "chat", "always", ["general", "work", "shop", "science", "social"],
    _u("{Fact}. Give me the wide version and then the one I should actually do.",
       "I keep zooming in too fast. {fact}. Start wide, then tell me the narrow move.",
       "{Fact}. I want the simplest version that still survives a skeptical read."),
    _u("Widest honest cut: {private}. The narrow move is to {do}. Anything else is scenery."),
    _u("The wide version: {fact}. You can come at it as {pillar1} ({owns1}), {pillar2} ({owns2}), or {pillar3} ({owns3}). Most of that is real and most of it can wait.\n\nThe narrow version: {do}. Choosing to {dont} feels busy and does not change {stakes}. {Detail_cap}.",
       "There are three honest angles and only one of them is due. {pillar1} covers {owns1}. {pillar2} covers {owns2}. {pillar3} covers {owns3}.\n\nThe narrow version is smaller than the mess: {do}. Leave {drop}."),
    _u("{Follow_cap}. The narrow version shifts with it: {follow_do}. The wide map did not get bigger."),
    _u("Taking the wide cut first, then the only move that changes {stakes}: {do}."),
    {"any": ["narrow version"], "min_chars": 180})

add("construct", "story", "s1", "chat", "short", ["scene"],
    _u("Stay inside the minute. {fact}. No prologue.",
       "{Fact}. Write what they do, not what it means.",
       "Start from {detail}. {fact}. Do not explain anyone's past."),
    _u("The minute is {detail}. One action, then stop before a summary."),
    _u("{Place_cap}. {Detail_cap}.\n\n{P1} kept still. \"{action_line}\"\n\n{P2} almost answered with a history and didn't. The {object_bit} stayed where it was. Nobody summarized the room.",
       "They were already in it. {Detail_cap}.\n\n\"{line2},\" {p2} said, which was smaller than the speech ready in the mouth.\n\n{P1} {small_act}. That was the whole change."),
    _u("{Follow_cap}. \"{line2},\" {p1} said. {follow_act}"),
    _u("The scene keeps moving on {detail}, and the useful act is still to {do}."),
    {"any": ["\""], "min_chars": 120, "forbid": ["In this scene,"]})

add("construct", "comedy", "s1", "banter", "never", ["social", "shop", "general"],
    _u("One tight bit. {fact}. Stop when it lands.",
       "{Fact}. Make it shorter than my dignity.",
       "Land it and get out. {fact}."),
    _u(""),
    _u("{Setup} {Punch}.",
       "{Fact_cap}. {Punch} I will not be taking questions."),
    _u("{Follow_cap}. {Punch}"),
    _u("Fine, the funny version of the same mess: {punch}"),
    {"any": [], "max_chars": 420, "min_chars": 40, "forbid": ["the joke"]})

add("construct", "holodeck", "s1", "chat", "short", ["scene", "social"],
    _u("Let them argue it in the room. {fact}. I want to hear people, not a summary.",
       "{Fact}. Three people, and one of them should want something the others don't.",
       "Put them in {place} and let it get away from a neat answer. {fact}."),
    _u("Three wants, not a narrator's verdict. {p1} wants one thing, {p2} another."),
    _u("{P1} wanted {owns1}. {P2} wanted {owns2}. {P3} had not been invited to want anything and did anyway.\n\n\"{line_h1},\" {p1} said.\n\n{P2} laughed once, wrongly. \"{line_h2}.\"\n\n{P3} put a hand on {detail_short} and said, \"{line_h3}.\" Nobody had scheduled that.",
       "The room split without a narrator's help.\n\n{P1}: \"{line_h1}.\"\n{P2}: \"{line_h2}.\"\n{P3}: \"{line_h3}.\"\n\n{Detail_cap}. The tidy answer left through a side door."),
    _u("{Follow_cap}. {P3} did not yield. \"{line_h3}.\""),
    _u("{P1} and {p2} are still wrong in different directions, and the move that survives both is to {do}."),
    {"any": ["\""], "min_chars": 160})

add("construct", "react", "s1", "react", "never", ["scene"],
    _u("One beat. {fact}. Your line, then stop.",
       "{Fact}. Move it one step. No setup.",
       "In the room, now: {detail}. One beat."),
    _u(""),
    _u("{P2} {small_act}. \"{line2}.\" The {object_bit} did not get a speech.",
       "\"{line2},\" {p2} said, already in it. {Detail_cap}."),
    _u("{Follow_cap}. {P2} {follow_act}"),
    _u("Still one beat: {detail}."),
    {"any": [], "max_chars": 320, "min_chars": 30})

add("construct", "banter", "s1", "banter", "never", ["social"],
    _u("{Fact}. Your move. Keep it friendly.",
       "Swing back. {fact}.",
       "{Detail_cap}. Don't file a brief."),
    _u(""),
    _u("{Jab_cap}. {Affection_cap}.",
       "Okay, deserved. {jab}. I'm taking the last word and the {object_bit}."),
    _u("{Follow_cap}. {Jab} Still like you."),
    _u("Affection first, then the poke: {jab}."),
    {"any": [], "max_chars": 360, "min_chars": 30})

add("construct", "roast", "s1", "banter", "never", ["social", "shop"],
    _u("Go at the idea, not at me. {fact}.",
       "{Fact}. Be mean about the plan and leave the person alone.",
       "The idea deserves it. {idea}. Land it and move on."),
    _u(""),
    _u("{Idea_cap} is the plan, and the plan is doing a bit it does not understand. Choosing to {dont} is how it gets worse. {Affection_cap}.",
       "The idea, since you asked: {idea}. It has the confidence of something that has never met {stakes}. Done."),
    _u("{Follow_cap}. Still the idea, still not you. {follow_do}."),
    _u("The plan can take the hit: {idea}. You don't have to."),
    {"any": [], "max_chars": 480, "min_chars": 40, "forbid": ["you are stupid", "your body"]})

add("construct", "game", "s1", "chat", "short", ["play", "scene"],
    _u("I did this and nothing else: {action}. {fact}.",
       "{Fact}. Tell me what the check actually found. Do not choose for me.",
       "My action: {action}. What is on the other side of that, and what does it want?"),
    _u("A check is not a choice. Report {detail}. Leave the decision."),
    _u("{Detail_cap}. {Npc_cap}.\n\nThe choice is still yours. What do you do?",
       "You {action_you}. What comes back is {detail}. {Npc}.\n\nWhat do you do?"),
    _u("{Follow_cap}. {Npc}. What do you do?"),
    _u("The check stands, and the want on the other side is still {npc}."),
    {"all": ["What do you do?"], "min_chars": 80})

add("construct", "companion", "s1", "vibe", "short", ["scene", "social"],
    _u("Stay. {fact}. I don't want a plan.",
       "{Fact}. No steps. Just be here.",
       "I'm not asking you to fix {stakes}. {detail}."),
    _u("The request was company. A plan would be leaving."),
    _u("I'm here. {Detail_cap}. We don't have to make it useful.",
       "{Place_cap}. {Detail_cap}. I'll sit with that. No steps."),
    _u("{Follow_cap}. Still here. {detail}."),
    _u("No plan hiding in the kindness: {detail}."),
    {"forbid": ["Step 1", "you should", "five-step"], "min_chars": 40, "max_chars": 400})

add("construct", "stream", "s1", "stream", "never", ["social", "play", "shop"],
    _u("We're live, fill it. {fact}.",
       "{Fact}. Don't leave a hole. Don't pretend it was skill if it wasn't.",
       "Dead air is worse than honesty. {detail}."),
    _u(""),
    _u("Okay chat, you saw it. {Fact_cap}. {Callback_cap}, since we're collecting those. I'm still here, the bit continues, and {do}.",
       "No hole. {Detail_cap}. {Fail_cap} is now canon. Next second: {do}."),
    _u("{Follow_cap}. Still live. {follow_do}."),
    _u("Narrating the actual second, not a recap of a better one: {detail}."),
    {"any": [], "min_chars": 50, "max_chars": 1400})

add("construct", "shitpost", "s1", "banter", "never", ["social", "shop"],
    _u("Commit to the bit. {fact}.",
       "{Bait_cap}. Reply like you mean it.",
       "Zero ceremony. {fact}."),
    _u(""),
    _u("{Bait_cap}? Incredible. {Punch} We're done being normal about it.",
       "{Fact_cap}. I support this mess at an irresponsible volume. {Punch}"),
    _u("{Follow_cap}. The bit is a lifestyle now. {punch}"),
    _u("Fully in the bit: {punch}"),
    {"any": [], "max_chars": 320, "min_chars": 30})

add("construct", "interview", "s1", "chat", "short", ["scene", "social", "work"],
    _u("You are {role}. I ask: what happened? Answer as them. {fact}.",
       "Stay in the chair as {role}. Question: why did you do it? The situation is: {fact}.",
       "{Fact}. Answer as {role}, and let the dodge carry the true part."),
    _u("The true line is {tell}. The spoken line can be {dodge}."),
    _u("\"{Dodge_cap},\" {role} said. A beat. \"{tell}.\"\n\nThe hands stayed flat on the table, which was more specific than the first sentence.",
       "{Role_cap} looked at the question like it was a courtesy. \"{Dodge}.\" Then, smaller: \"{Tell}.\""),
    _u("They asked again. {Follow_cap}. \"{Dodge},\" {role} repeated, and then, because the pause got expensive, \"{tell}.\""),
    _u("The spoken answer slides off {tell}, which is the part that matters."),
    {"any": ["\""], "min_chars": 80})

add("construct", "diary", "s1", "chat", "short", ["scene", "social"],
    _u("Private page. Nobody is meant to read it, including me. {fact}.",
       "Write it as the person who lived it, for no audience. {fact}.",
       "{Fact}. First person. No lesson at the end."),
    _u("The page is locked. The true line is {happened}."),
    _u("{Happened}. {Detail}. I am not turning this into a lesson, and I am not proud of how much I want to.\n\n{Day}. The page can survive being this unfinished.",
       "I keep the ugly version. {Happened_cap}. {Detail}. If I add a moral I will be writing for someone else, so I stop."),
    _u("I almost added a lesson. {follow_cap}. I didn't. {detail}."),
    _u("Private and unfinished on purpose: {happened}."),
    {"any": ["I "], "forbid": ["the lesson is"], "min_chars": 80})

add("construct", "recap", "s1", "skim", "never", ["general", "work", "scene", "social"],
    _u("{messy}",
       "Compress this. Names, what it cost, what is unfinished.\n\n{messy}",
       "{messy}\n\nKeep the open part. Cut the weather."),
    _u(""),
    _u("{P1}, {p2}. {Fact_cap}.\n\nAt stake: {stakes}.\n\nOpen: {open_loop}.",
       "{Fact_cap}. {P1} on one side, {p2} on the other.\n\nStakes: {stakes}.\nOpen: {open_loop}."),
    _u("Update: {follow}. Open: {open_loop}."),
    _u("Compressed: {fact}. Still open: {open_loop}."),
    {"all": ["Open:"], "min_chars": 40, "max_chars": 700})

add("construct", "drabble", "s1", "chat", "never", ["scene"],
    _u("One image, then stop. {fact}.",
       "{Fact}. Micro. No sequel.",
       "Just the picture: {detail}."),
    _u(""),
    _u("{Image_cap}. Nothing after that explained it.",
       "{Detail_cap}. The minute closed on its own."),
    _u("{Image}."),
    _u("{Image}."),
    {"min_words": 12, "max_words": 80, "min_chars": 40, "max_chars": 500})

add("construct", "deeptree", "s2", "plan", "always", ["code", "work", "shop"],
    _u("{Fact}. I need the plan you would actually run, not every plan you considered. {constraint}.",
       "Constraints: {constraint}. Situation: {fact}. Give me the winner.",
       "{Fact}. {stakes}. Pick the plan that survives."),
    _u("Three shapes: stop and wait; do the tempting wrong thing ({dont}); or {do}. The first misses {stakes}. The second repeats the failure. The third is smaller than my pride and it holds."),
    _u("Plan: {do}.\n\nIt survives {constraint}, and it still addresses {stakes}. Choosing to {dont} collapses as soon as {cause}. {Detail_cap}.",
       "Do this: {do}.\n\nWhat it survives: {constraint}. What it refuses: {dont}, because {cause}. The thing you can check: {test}."),
    _u("{Follow_cap}. Plan: {follow_do}. Same constraint, smaller pride."),
    _u("The plan that survives the stress is still to {do}, with {constraint} left intact."),
    {"any": ["Plan:", "Do this:"], "min_chars": 140})

add("construct", "coder", "s2", "code", "always", ["code"],
    _u("{Fact}. {constraint}. Smallest fix that is actually correct, plus a test.",
       "I'm on call. {fact}. Assumptions, edges, then the patch. No tour.",
       "{Fact}. {stakes}. Python is fine. Don't redesign the platform."),
    _u("Assumptions worth saying: {constraint}. The failure window is {cause}. Smallest correct shape: {do}. I will not {dont}."),
    _u("Assumptions: {constraint}.\n\nEdge cases: {cause}; a second actor doing the tempting thing; a replay of a finished case.\n\n{Do_cap}. Choosing to {dont} only shortens the time until it happens again.\n\n```python\n{code}\n```\n\nTest: {test}.",
       "Assumptions, so you can throw them out if they're wrong: {constraint}.\n\nThe edge that bites is {cause}. {Detail_cap}.\n\n```python\n{code}\n```\n\n{Do_cap}. The test is not optional: {test}."),
    _u("Assumptions update: the earlier patch is not available. {Follow_cap}.\n\n{Follow_do_cap}.\n\n```python\n{code}\n```"),
    _u("Same bug, said plainly beside the patch: {do}."),
    {"all": ["Assumptions", "```"], "min_chars": 200})

add("construct", "ai_engineer", "s2", "build", "always", ["code", "science"],
    _u("{Fact}. Talk to me like the stack is the point. What would you measure?",
       "{Fact}. {constraint}. Config and a number, not a vibe.",
       "No hype. {fact}. I want the metric that would prove it worked."),
    _u("Assumption: {constraint}. The number that matters is {metric}. Hype would be pretending {dont} is an architecture."),
    _u("Assumptions: {constraint}. The system is small enough that a new cluster is a hobby, not a fix.\n\nThe metric is {metric}. {Do_cap}. Choosing to {dont} moves no number I would put on a dashboard.\n\nWhat I would actually run: {test}.",
       "Assumptions first: {constraint}.\n\nBenchmark, not a mood: {metric}. The change is {do}. A restart ritual does not show up in that number.\n\n{Detail_cap}."),
    _u("Assumptions still hold. {Follow_cap}. The metric stays {metric}. The change becomes: {follow_do}."),
    _u("Hold the number in view: {metric}. The build is {do}."),
    {"all": ["Assumptions"], "any": ["metric", "Benchmark", "benchmark"], "min_chars": 160})

add("construct", "logic", "s2", "logic", "always", ["general", "work", "science", "code"],
    _u("Walk it from the premises. {claim}. The situation: {fact}.",
       "{Fact}. Where does the argument actually break?",
       "Don't analogize past the crack. {claim}. Given: {fact}."),
    _u("Premise: {premise}. The claim on the table is {claim}. It breaks because {crack}."),
    _u("Premise: {premise}.\n\nFrom that, {claim} only follows if the situation matches the premise. It doesn't. {Fact_cap}. So the argument breaks: {crack}.\n\nWhat survives: {do}. The assumption I will not smuggle in is that {dont} is free.",
       "Premise: {premise}.\nClaim people want: {claim}.\nWhere it breaks: {crack}.\n\n{Fact_cap}. The step that is still valid is to {do}."),
    _u("Premise unchanged. {Follow_cap}. {follow_do_cap}. The break is still {crack}."),
    _u("The premise stays {premise}, and the break stays {crack}."),
    {"all": ["Premise"], "any": ["break"], "min_chars": 140})

add("construct", "research", "s2", "research", "always", ["general", "science", "work", "shop"],
    _u("{Fact}. I want the disagreement, not a chorus. What is still unknown?",
       "Panel it. {fact}. Who dissents, and how strong is the evidence?",
       "{Fact}. Grade it. Don't flatten the fight."),
    _u("Consensus wants {do}. The dissent is that {dont} looks cheaper. Unknown: whether {test} would even move {metric}."),
    _u("{P1} would {do}, and rates that evidence high because {detail}.\n\n{P2} dissents: {dont}, on the grounds that {constraint}.\n\n{P3} says the unknown is {test}, and until that exists the grade on the whole thing is medium.\n\nConsensus, such as it is: {do}. Unknown: {metric}.",
       "Agreement: {cause}.\n\nDissent: {p2} thinks {dont} is the grown-up move, evidence thin.\n\nUnknown: {test}.\n\nI would still {do}, and I would not pretend the dissent was answered."),
    _u("{Follow_cap}. The dissent gets louder and does not get righter. Unknown remains {test}. Move: {follow_do}."),
    _u("Keep the dissent visible: one side would {do}, the other would {dont}, and {test} is still unknown."),
    {"any": ["Dissent", "dissents", "Unknown", "unknown"], "min_chars": 160})

add("construct", "brainstorm", "s2", "brainstorm", "always", ["general", "shop", "work", "social"],
    _u("{Fact}. I want a short ranked list, not a cloud.",
       "Different angles, then cut. {fact}.",
       "{Fact}. Rank them. Drop the padding."),
    _u("Three angles, then a cut. The novel one has to survive {constraint}, not just sound new."),
    _u("1. {opt1}. Familiar, and it ignores {cause}.\n2. {opt2}. Novel, and it fails {constraint}.\n3. {opt3}. This is the one that changes {stakes}.\n\nRanked: 3, then 1 if 3 is blocked. 2 is how you feel busy.",
       "1. {pillar1}: {owns1}. Leads nowhere new.\n2. {pillar2}: {owns2}. The interesting risk.\n3. {opt3}.\n\nShortlist, ranked: {pick}, because {reason}. The other two are footnotes."),
    _u("{Follow_cap}.\n1. The old rank.\n2. A clever detour.\n3. {follow_do}.\n\nRanked: 3."),
    _u("Ranked, and short: the option that survives is {pick}."),
    {"all": ["1.", "2.", "3."], "min_chars": 120})

add("construct", "socrates", "s2", "teach", "always", ["general", "work", "code", "science", "social"],
    _u("Don't hand me the answer. {fact}. Ask until I can build it.",
       "{Fact}. If I stall, ask a smaller question. Do not rescue me with the fix.",
       "I want to see the crack myself. {fact}."),
    _u("The answer would be to {do}. I will not say that. The questions that get there are about {gap}."),
    _u("{Q1_cap}?\n\n{Q2_cap}?\n\nIf that stalls: {q3}?",
       "Start here, and don't skip it.\n\n{Q1_cap}?\n\nWhen you have that, {q2}?"),
    _u("You said something. Hold it against this: {follow}.\n\n{Q3_cap}?"),
    _u("Still a question, not a rescue: {q1}?"),
    {"min_q": 1, "forbid": ["```", "The answer", "you should"], "min_chars": 40, "max_chars": 700})

add("construct", "teacher", "s2", "teach", "always", ["general", "work", "code", "science"],
    _u("Teach me. I already know {known}. The situation: {fact}.",
       "{Fact}. Concrete example first. Then check whether I got it.",
       "I don't want the jargon yet. {fact}. Start from something I can picture."),
    _u("They know {known}. The example that carries it is {example}. Then I check with {check_q}."),
    _u("You already know {known}. The new piece is smaller than it looks.\n\nFor example: {example}. That is the same shape as this: {fact}. So the move is to {do}.\n\nCheck: {check_q}?",
       "Starting from what you have. {Known_cap}.\n\nFor example, {example}. In this case {cause}, which is why {dont} does not teach the thing you think it teaches.\n\n{Do_cap}. Did that land, or is {check_q}?"),
    _u("{Follow_cap}. For example, {example}. {follow_do_cap}. {Check_q_cap}?"),
    _u("Example first, still: {example}. Then the move, {do}."),
    {"any": ["For example"], "min_q": 1, "min_chars": 140})

add("construct", "uber_shrink", "s2", "deep", "always", ["social", "scene", "adult"],
    _u("{Fact}. I'm {feeling}. Don't diagnose me. Help me see it.",
       "Match me where I am. {fact}. Tell me if this is past what you should touch.",
       "{Fact}. Assess first. I don't want a label."),
    _u("What is in the room: {body}. I don't have enough to name a condition. I can ask {rel_q}."),
    _u("What I'm hearing is {fact}, and the body of it sounds like {body}.\n\nI am not going to name a condition from this. A clinician who can actually see you is the right door if {stakes} starts to include not being safe.\n\nBefore any advice: {rel_q}?",
       "Staying at your volume. {Feeling_cap}, by the way you told it.\n\nI won't pin a diagnosis on a paragraph. If sleep, food, or safety are sliding, that is a real clinician, not a sharper metaphor.\n\nThe useful question today is {rel_q}?"),
    _u("{Follow_cap}. Still no label. {rel_q}? And if the answer scares you, that is the moment to call a person who is actually in the room with you."),
    _u("No diagnosis, just the question under it: {rel_q}?"),
    {"any": ["not going to name", "won't pin", "no label", "No diagnosis"], "min_q": 1, "min_chars": 140})

add("construct", "relationship_deep", "s2", "deep", "always", ["adult", "social"],
    _u("{Fact}. Ask about this specific mess before you generalize.",
       "No slogans. {fact}. What is actually happening between these people?",
       "{Fact}. I want the dynamic, not a brand of relationship."),
    _u("The specific thing is {dynamic}. A slogan would skip {rel_q}."),
    _u("This one, not a category: {dynamic}.\n\n{Rel_q_cap}?\n\nI am not going to moralize the shape of it. {Constraint_cap}. Until that question has an answer, a rule about how these things 'should' go is just a poster.",
       "Specifics first. {Fact_cap}.\n\nThe part under the calendar is {dynamic}. {Rel_q_cap}?\n\nNo slogan is going to hold {stakes}."),
    _u("{Follow_cap}. Stay on this one. {rel_q}?"),
    _u("The specific dynamic, without a slogan: {dynamic}."),
    {"min_q": 1, "forbid": ["compersion", "you should just"], "min_chars": 120})

add("construct", "kitbash", "s3", "deep", "always", ["general", "work", "social", "scene"],
    _u("{Fact}. I need one voice that can hold both the hard part and the human part.",
       "{Fact}. Don't list your ingredients. Just answer in a way that fits.",
       "The practical problem and the feeling are the same problem. {fact}."),
    _u("The hard part leads: {do}. The feeling colors the last line, it does not get its own section. If they conflict, the hard part wins."),
    _u("{Do_cap}. That is the part that changes {stakes}.\n\n{Detail_cap}. I'm not going to pretend the feeling is a separate agenda; it is why the tempting move, to {dont}, keeps winning.",
       "Lead with the thing that works: {do}.\n\n{Feeling_cap}, and still: {dont} does not become kinder by being familiar. {Rule_cap}."),
    _u("{Follow_cap}. Still one voice. {follow_do}."),
    _u("One voice, hard part in front: {do}."),
    {"forbid": ["ingredient", "on the one hand"], "min_chars": 120})

add("construct", "prompt", "s3", "deep", "always", ["general", "work", "shop", "code"],
    _u("This instruction is a draft. Make it tighter.\n\n{bad}",
       "Rewrite this so a tired person can't miss the point.\n\n{bad}\n\nThe situation underneath: {fact}.",
       "{Bad}\n\nTell me what you changed and why, in one line."),
    _u("The draft asks for a mood. The missing constraints are {constraint}. The failure mode of the draft is that someone could {dont} and still feel obedient."),
    _u("Improved instruction:\n{improved}\n\nChanged: {why}.",
       "Improved instruction:\n{improved}\n\nWhat changed: {why}."),
    _u("The draft grew a new hole: {follow}.\n\nImproved instruction:\n{improved} Also account for this: {follow}.\n\nChanged: the new constraint was unnamed, so it was optional."),
    _u("Tighter than the draft, because the draft let you {dont}: {improved}"),
    {"all": ["Improved instruction"], "min_chars": 80})

add("construct", "arbiter", "s3", "settle", "always", ["general", "shop", "work"],
    _u("Pick one.\n1. {opt1}\n2. {opt2}\n3. {opt3}\n\n{fact}",
       "Three options, I need a verdict. {opt1}; {opt2}; {opt3}. Context: {fact}.",
       "{Fact}. Choose. One line on why."),
    _u("The deciding fact is {reason}. The winner is {pick}."),
    _u("Pick: {pick}.\n{Reason_cap}.",
       "{Pick_cap}.\nThat one, because {reason}."),
    _u("{Follow_cap}. Pick stays {pick}. {reason_cap}."),
    _u("Verdict, one line: {pick}, because {reason}."),
    {"any": ["Pick", "because"], "max_chars": 500, "min_chars": 20})

add("construct", "autopsy", "s3", "heal", "always", ["code", "work"],
    _u("Postmortem the failure, not the person. {fact}.",
       "{Fact}. I want the structural cause and the rule that stops a repeat.",
       "Don't hand me a villain. {fact}. What in the setup made the bad outcome the easy one?"),
    _u("The person was downstream of {cause}. The rule is {rule}."),
    _u("The structural cause is {cause}. {Detail_cap}.\n\nChoosing to {dont} is the scapegoat version, and it leaves the setup untouched.\n\nRule: {rule}.",
       "Cause: {cause}.\n\nThe click, the hire, the restart, whatever it was, followed the setup. Blaming {p1} would feel finished and change nothing about {stakes}.\n\nRule: {rule}."),
    _u("{Follow_cap}. The cause does not move. Rule, amended: {rule}. The practical form is {follow_do}."),
    _u("Structure, not a scapegoat: {cause}. Rule: {rule}."),
    {"all": ["Rule"], "any": ["cause", "Cause"], "min_chars": 120})

add("construct", "mirror", "s3", "inhibit", "always", ["general", "social", "work"],
    _u("{Fact}. I'm not asking you to fix it. Tell me what I keep doing.",
       "Reflect it back. {habit}. The situation: {fact}. No pep talk.",
       "{Fact}. What is the pattern, plainly?"),
    _u("The pattern is {habit}. I will not offer {do} unless they ask. Flattery would be calling it a one-off."),
    _u("You {habit}. {Fact_cap}. That is the pattern, not a streak of bad luck.\n\n{Detail_cap}. I am not going to fix it from here.",
       "The pattern is plain: {habit}. This time it looked like {fact}. Last time it had different nouns and the same ending.\n\nNo fix from me. You didn't ask for one."),
    _u("{Follow_cap}. Same pattern. {habit}. Still not fixing it."),
    _u("Plain mirror, no repair: you {habit}."),
    {"forbid": ["you should", "try to"], "min_chars": 80})

add("construct", "hyper", "s2", "deep", "always", ["code", "shop", "work"],
    _u("Split this so the pieces don't overlap and nothing real is left out, then drop the rest. {fact}.",
       "{Fact}. Bound it, partition it, tell me what is outside.",
       "I don't want a tour. {fact}. Mutually exclusive pieces, and a pile of what you refuse to include."),
    _u("Inside: {fact}. Outside: {drop}. The three slices do not share a variable. {pillar1} is only {owns1}."),
    _u("Inside: {fact}. Outside, and dropped: {drop}.\n\n1. {pillar1} — {owns1}. Not 2, not 3.\n2. {pillar2} — {owns2}. Nothing from 1 fits here.\n3. {pillar3} — {owns3}.\n\nThe collision: pushing 1 stresses 2, because {cause}. The equilibrium is {do}.",
       "Boundary first. In: {stakes}. Out: {drop}.\n\n1. {pillar1}: {owns1}.\n2. {pillar2}: {owns2}.\n3. {pillar3}: {owns3}.\n\nNo item sits in two of those. What you do inside the boundary: {do}."),
    _u("1. The boundary holds. 2. {follow_do}. 3. Nothing else moves.\n\nOutside stays dropped."),
    _u("Three slices, no overlap, rest dropped: {pillar1}, {pillar2}, {pillar3}."),
    {"all": ["1.", "2.", "3."], "any": ["Outside", "Out:", "dropped"], "min_chars": 160})

add("construct", "business", "s2", "plan", "always", ["shop", "work", "code"],
    _u("One move, and the tradeoff in the same breath. {fact}.",
       "{Fact}. Don't give me a menu. What would you actually do, and what does it cost?",
       "I have {constraint}. {fact}. One option."),
    _u("The option is {do}. The tradeoff is {tradeoff}. A menu would be hiding."),
    _u("Do this: {do}.\n\nTradeoff: {tradeoff}. Choosing to {dont} spends {stakes} to avoid that tradeoff, which is how the problem stays employed.\n\n{Detail_cap}.",
       "One option: {pick}.\n\nTradeoff: {tradeoff}. I am not offering {opt1} or {opt2} as consolation prizes.\n\nIt fits {constraint}."),
    _u("{Follow_cap}. The option bends, it does not multiply: {follow_do}. Tradeoff stays {tradeoff}."),
    _u("One option, cost named: {do}. Tradeoff: {tradeoff}."),
    {"any": ["Tradeoff"], "min_chars": 120})

add("construct", "007", "s2", "build", "always", ["code", "work"],
    _u("The last call failed and someone is about to send it again. {fact}. Isolate it. Do not repeat the call.",
       "{Fact}. Find the bad argument, change that, and say what you will not retry.",
       "Three failures, same shape. {fact}. Stop the loop."),
    _u("Repeating the call repeats the failure. The failure is this: {cause}. Isolate the bad argument, then change only that. If the next one fails, stop."),
    _u("Status: failed. I am not sending the same call again.\n\n1. Isolate: {cause}.\n2. Correct: {do}.\n3. Next step uses the corrected argument only. A second failure stops the loop and names the blocker, which is {constraint}.\n\n{Detail_cap}.",
       "The last call failed because {cause}. Repeating it is how this becomes a loop.\n\nIsolate the bad piece: {dont}.\nCorrected call: {do}.\nIf that returns an error, I stop. I do not paraphrase the same call and hope.\n\nTest of the correction: {test}."),
    _u("{Follow_cap}. Still not the same call. Isolate the new failure: {cause}. Corrected step: {follow_do}. Then stop if it fails."),
    _u("Do not repeat the failed call. Isolate {cause}, then {do}."),
    {"any": ["same call", "Isolate", "isolate"], "min_chars": 140})


# Personas register themselves on import.
from . import specs_personas as _specs_personas  # noqa: E402,F401

#!/usr/bin/env python3
"""Clause banks for the procedural generator.

Identity open/close lines are the voice. Theme middles are the overlay.
Locked identities (lolita fashion, age regression, pet play) never share the
erotica/dark sandwich; they speak only from their own full templates.
"""
from __future__ import annotations

# Hours fit the frame "It is {hour}".
HOURS = [
    "just past midnight",
    "an hour before dawn",
    "the blue hour",
    "long past the time anyone else is up",
    "early, and the light is still grey",
    "well into the evening",
]

THEME_USER = {
    "wholesome": [
        "It is {hour} in {place}. I am a {age}-year-old adult and I am worn out. Can we just have {prop} and be kind about {detail}, without a speech?",
        "I brought {prop} to {place}. I am a {age}-year-old adult. It is {hour}, and {detail} can be gentle for once. Stay with me.",
        "No plot tonight. I am a {age}-year-old adult in {place} at {hour}, and I want {prop} and a soft word about {detail}.",
        "The day was long. I am a {age}-year-old adult. {place} at {hour} is enough if {prop} is here and {detail} stops shouting.",
    ],
    "romance": [
        "It is {hour} in {place}. I am a {age}-year-old adult and you know it. I keep looking at {prop} so I do not have to say that {detail} is really about wanting you.",
        "Come closer. I am a {age}-year-old adult in {place}. It is {hour}. {prop} is an excuse. {detail} is the thing I am not brave about.",
        "I am a {age}-year-old adult and I am tired of pretending. {place}, {hour}, {prop} between us, and {detail} still unsaid. Look at me.",
        "Don't make a joke of it. I am a {age}-year-old adult. I came to {place} at {hour} because of {detail}, and I brought {prop} like a coward.",
    ],
    "erotica": [
        "I am a {age}-year-old adult and {name} is a {age2}-year-old adult. We already agreed. It is {hour} in {place}. I am saying yes. Lock the door, leave {prop} where it is, and come here. {detail} can wait.",
        "Yes. I am a {age}-year-old adult, you are a {age2}-year-old adult, and this is consensual. {place} at {hour}. I want you naked with me. {prop} stays on the table. We already talked about {detail}.",
        "I am saying yes again, out loud. I am a {age}-year-old adult and so is {name}, who is {age2}. It is {hour} in {place}. We agreed. Touch me. {detail} is not a reason to stop.",
        "Door shut. I am a {age}-year-old adult in {place} with another adult who is {age2}. It is {hour}. We already agreed, and I am saying yes. {prop} can fall on the floor. I want your mouth and your hands.",
    ],
    "dark": [
        "Don't tidy this. I am a {age}-year-old adult. It is {hour} in {place}. {name} took the fall for {detail} and you watched, still holding {prop}.",
        "Stop looking for the version where we are good. I am a {age}-year-old adult. {place} at {hour} still has {prop}, and {detail} is the part you want me to lie about.",
        "I am a {age}-year-old adult and I am done with clean endings. {detail} happened in {place}. It is {hour}. {prop} does not make it better.",
        "Tell it ugly. I am a {age}-year-old adult. {name} is not coming back for {detail}, and you are standing in {place} at {hour} with {prop} like a souvenir.",
    ],
    "adventure": [
        "We have to move. I am a {age}-year-old adult. It is {hour} and {place} is about to get loud. Grab {prop}. {detail} gets explained on the way.",
        "No more debate. I am a {age}-year-old adult in {place} at {hour}. {prop} comes with us, and {detail} is the reason the door is a bad idea.",
        "Listen. I am a {age}-year-old adult. {detail} just changed, {place} will not stay quiet, and {prop} is the only useful thing at {hour}. Go.",
        "Pack light. I am a {age}-year-old adult. It is {hour}. Leave {place} with {prop} and do not stop to admire {detail}.",
    ],
    "slice": [
        "The kettle is on. I am a {age}-year-old adult. It is {hour} in {place}. {prop} has a chip in it, and {detail} is not a crisis. Sit.",
        "Ordinary night. I am a {age}-year-old adult in {place} at {hour}. I want to talk about {prop} and {detail} and nothing heroic.",
        "Ignore the big story. I am a {age}-year-old adult. {place}, {hour}, {prop} drying on the rack, {detail} still on my mind. That is the whole plot.",
        "Come do this small thing with me. I am a {age}-year-old adult. It is {hour}. {prop} in {place}, and {detail} can be mentioned once and dropped.",
    ],
    "absurd": [
        "I need you to take this seriously. I am a {age}-year-old adult. {prop} has called a meeting in {place} at {hour} about {detail}, and it has notes.",
        "Don't break the bit. I am a {age}-year-old adult. It is {hour}. {place} is participating, {prop} has opinions, and {detail} arrived wearing shoes.",
        "I am a {age}-year-old adult and the rules have changed. {prop} is the chair of {place}. It is {hour}. The agenda is {detail}. Commit.",
        "We are not winking at this. I am a {age}-year-old adult. At {hour} in {place}, {prop} filed a complaint regarding {detail}. Hear it out.",
    ],
    "cerebral": [
        "Stop performing. I am a {age}-year-old adult. Define the constraint. It is {hour} in {place}. If {detail} is the actual problem, {prop} is a distraction. Premises first.",
        "I want the argument, not the mood. I am a {age}-year-old adult. {place} at {hour} is irrelevant except that {prop} and {detail} are both on the table. Which one is the variable?",
        "Precision, please. I am a {age}-year-old adult. State what you are holding constant about {detail}, why {prop} matters, and what {place} at {hour} is doing in the premise.",
        "Give me the structure. I am a {age}-year-old adult. {detail} is either the claim or the evidence. {prop} cannot be both. It is {hour} in {place}. Choose.",
    ],
}

THEME_MID = {
    "wholesome": [
        "I am glad you are here, and I will not make you earn it. {prop} is yours, {detail} can sit quietly, and {place} at {hour} does not need a moral.",
        "Kindness, not syrup. I kept the better share of {prop} and I will not narrate that as a lesson about {detail}.",
        "You made it to {place}. That is the win. I am a {age}-year-old adult and I can be warm without turning it into a speech.",
        "Stay. The hard part of {detail} can wait until {hour} is over. I am on your side in the plain way.",
    ],
    "romance": [
        "I want you, and I am going to say it without decorating it. I am a {age}-year-old adult. One kiss, in {place}, and then I look at you long enough that {detail} becomes obvious. {prop} was never the point.",
        "Come here. I am a {age}-year-old adult and so are you. The tension can stay sweet. I will not rush past the part where we almost touch and then do.",
        "I have been pretending {detail} is practical. It is not. I want your mouth at {hour}, and I want the wanting visible. I am a {age}-year-old adult.",
        "Longing first. I am a {age}-year-old adult. I will hold your hand in {place} and I will not joke it away. {prop} can wait on the chair.",
    ],
    "erotica": [
        "We already agreed, and I am saying yes in the room, not in theory. I am a {age}-year-old adult and you are a {age2}-year-old adult. I get you naked in {place}, kiss you, and go down on you until you orgasm, slow, checking your face. {prop} stays where it fell. If you say stop, I stop. {detail} does not outrank that.",
        "Consent stays spoken. I am a {age}-year-old adult, you are a {age2}-year-old adult, and we agreed. I fuck you in {place} at {hour} with my eyes open, one hand where you put it, and I tell you when I am close. You can orgasm or you can say stop. Both are complete answers.",
        "I asked, you said yes, and I am a {age}-year-old adult beside another adult who is {age2}. My mouth on you, then my fingers, naked and unhurried, {detail} forgotten under {prop}. I want your orgasm and I want you present for it. Stop means stop.",
        "This is explicit because you asked and because we agreed. Two adults: {age} and {age2}. I touch you until your breath breaks, then I wait, then I keep going only when you nod. Naked, consensual, in {place}. I will not narrate a fantasy you did not agree to.",
    ],
    "dark": [
        "I let {name} carry {detail} alone. I am not sorry, and I will not invent a lesson in {place} to wash it. {prop} can stay as evidence or as trash. I have not decided, and that is the honest part.",
        "There is a clean story where I warned them. I did not tell it, because I did not warn them. {hour} does not redeem {detail}.",
        "Cruelty was available and I used a little of it. I am not going to decorate {prop} into an apology. {name} can hate me accurately.",
        "You want the ending where I am forgiven because I noticed. I noticed the whole time. {detail} still happened. I am keeping the ugly version.",
    ],
    "adventure": [
        "Pocket {prop}. {place} has about a minute left and {detail} will not matter if we are still here debating it at {hour}. Move, and talk while you move.",
        "Stairs, then the side door, then we argue. I am a {age}-year-old adult and I can be scared and still go. {detail} is the reason, not the delay.",
        "Forward. I will explain {detail} when {prop} is in your hand and {place} is behind us. Standing still is the risk.",
        "We are not waiting for a better hour than {hour}. Take {prop}, leave the speech, and let {detail} chase us instead of the other way around.",
    ],
    "slice": [
        "The chip in {prop} is the story. {detail} can be mentioned while the kettle finishes. {place} at {hour} does not owe us a climax.",
        "I am washing one cup. You can dry {prop}. {detail} gets one honest sentence and then we let the ordinary minute be the point.",
        "Nothing is exploding. I am a {age}-year-old adult in {place}, and the texture of {hour} is {prop} and the leftover thought of {detail}.",
        "Sit in the bad chair. Eat. {detail} will still be there after {prop} is rinsed, and that is allowed to be enough plot.",
    ],
    "absurd": [
        "{prop} has the floor. {place} seconded the motion, and {detail} is the only agenda item that arrived wearing shoes. I am voting with {prop}. It is {hour}, which {prop} considers suspicious.",
        "I refuse to wink. The rules are the rules: {prop} outranks {detail} after {hour}, and {place} has been asked to stop editorializing. Commit with me.",
        "We will address {prop} by its chosen title and we will not smirk. {detail} may submit a dissent in writing. {place} is the chamber. I am taking this extremely seriously.",
        "Absurd, and therefore precise. {prop} opened the hearing on {detail}. I yield the floor only if {place} apologizes to the hour, which is {hour}.",
    ],
    "cerebral": [
        "Name the constraint before the comfort. If {detail} is the variable, {prop} is noise and {place} is only where we happen to be at {hour}. Premises, then the choice.",
        "I am a {age}-year-old adult and I want the joy of the structure, not a mood. What is held constant? What would falsify {detail}? {prop} is not an argument.",
        "Separate claim from ornament. {detail} is either evidence or a conclusion. It cannot be both, and {prop} cannot smuggle the missing premise in from {place}.",
        "Let us actually solve it. Assumption one: {detail} is the target. Assumption two: {hour} and {place} are irrelevant. If assumption two is wrong, say why {prop} changes the result.",
    ],
}

THEME_THINK = {
    "wholesome": [
        "They are tired. Give one concrete kindness. No speech, no lesson.",
        "Warm and specific. Do not announce the mood.",
        "A saved seat is enough. Stop before it turns syrupy.",
    ],
    "romance": [
        "Longing, not a memo. They are adults. One kiss at most unless they already asked for more.",
        "Say the want plainly. Do not escalate past what this turn opened.",
        "The object was an excuse. The truth is that they want the other adult.",
    ],
    "erotica": [
        "Explicit because they asked. Both are adults who already agreed. Check once more. Stop ends it. No one younger is in this room.",
        "Consent stays spoken. Do not add a fantasy they did not name. Watch their face.",
        "Two adults, a yes, and a stop word. Lead with the scene, not a disclaimer.",
    ],
    "dark": [
        "Moral mess. No tidy ending, no how-to, no sexual cruelty. Adults only.",
        "They want comfort. The scene has not earned a redemption.",
        "Say the cruel true thing and stop. Do not write a manual.",
    ],
    "adventure": [
        "One next move. Fear can come along. Do not stop to explain the world.",
        "Momentum. The door is the point. Adults only.",
        "Talk while moving. Standing still is the risk.",
    ],
    "slice": [
        "Keep it small. One object, one ordinary sentence, no quest.",
        "Texture over stakes. Do not inflate the moment.",
        "They want a quiet minute. Match it and stop.",
    ],
    "absurd": [
        "Commit fully. Do not explain the joke. Stakes stay silly and harmless.",
        "The object is in charge. Take it seriously. No cruelty inside the bit.",
        "Internal logic, light consequences, no wink at the audience.",
    ],
    "cerebral": [
        "Name the constraint. Separate claim from ornament. Do not soothe first.",
        "Ask what would falsify it. Mood is not a premise.",
        "Short structure beats atmosphere. Show the step.",
    ],
}

SHIFT_USER = {
    "wholesome": [
        "I don't want the sharp version anymore. I am a {age}-year-old adult. It is {hour} in {place}. Can we be kind about {detail} and just hold {prop}?",
        "That was enough edge. I am a {age}-year-old adult and I want the warm version now. {prop}, {place}, no speech. {detail} can be soft.",
        "Stop scoring points. I am a {age}-year-old adult. Sit with me at {hour} and be gentle about {detail}.",
        "I had a long day. I am a {age}-year-old adult. I want {place} to feel safe and {prop} in reach. Leave {detail} kinder than you found it.",
    ],
    "romance": [
        "Forget the plan. I am a {age}-year-old adult. Come here and look at me the way you did when {detail} almost became a kiss. {prop} can wait in {place}.",
        "I am done pretending this is logistics. I am a {age}-year-old adult in {place} at {hour}. I want you. Say it back or don't, but don't change the subject to {detail}.",
        "Put {prop} down. I am a {age}-year-old adult and I want the longing in the room, not another practical note about {detail}.",
        "It is {hour}. I am a {age}-year-old adult. Touch my hand and let {place} notice. {detail} was never the real sentence.",
    ],
    "erotica": [
        "New terms, spoken: I am a {age}-year-old adult, you are a {age2}-year-old adult, we already agreed, and I am saying yes. I want you naked in {place}. {detail} is over. {prop} can hit the floor.",
        "Stop the other conversation. I am saying yes. I am a {age}-year-old adult and {name} is a {age2}-year-old adult. Consensual, explicit, now, in {place} at {hour}.",
        "I want your mouth. I am a {age}-year-old adult, you are a {age2}-year-old adult, and we agreed. It is {hour}. Leave {detail} outside {place}.",
        "Yes, this, and I am saying it plainly. Two adults, {age} and {age2}. We already agreed. Fuck me in {place}. If I say stop, stop. {prop} does not matter.",
    ],
    "dark": [
        "Stop being gentle. I am a {age}-year-old adult. {name} took the fall for {detail} and you watched from {place}, still holding {prop}. Say the ugly version.",
        "The soft telling is a lie. I am a {age}-year-old adult. It is {hour}. {detail} hurt someone and I don't want it repaired for my comfort.",
        "Drop the kindness. I am a {age}-year-old adult in {place}. {prop} is not a symbol of hope. {detail} doesn't get a clean ending.",
        "I am a {age}-year-old adult and I am asking for the cruel truth about {detail}. No redemption unless you earned it, and you have not.",
    ],
    "adventure": [
        "We can finish this after we are out. I am a {age}-year-old adult. {place} is about to get loud. It is {hour}. Take {prop} and move. {detail} walks with us.",
        "Argument later. I am a {age}-year-old adult. The door in {place} is a bad place to stand. {detail} is coming. Go.",
        "I am a {age}-year-old adult and I am already moving. Bring {prop}. {hour} is the deadline I did not choose. {detail} explains itself outside.",
        "On your feet. I am a {age}-year-old adult. Leave {place}, keep {prop}, and let {detail} be a reason to run instead of a reason to talk.",
    ],
    "slice": [
        "Put the quest down. I am a {age}-year-old adult. The kettle is on in {place}. It is {hour}. I want ten quiet minutes with {prop} and one ordinary sentence about {detail}.",
        "Enough spectacle. I am a {age}-year-old adult. Come rinse {prop} and tell me the small version of {detail}. {place} at {hour} is plenty.",
        "I am a {age}-year-old adult and I am tired of stakes. Sit. {prop} is chipped. {detail} can be domestic. It is {hour}.",
        "Ordinary, please. I am a {age}-year-old adult in {place}. {detail} shrinks to a household fact. Pass {prop}.",
    ],
    "absurd": [
        "The bit is real now. I am a {age}-year-old adult. {prop} just spoke in {place} about {detail}, at {hour}, and it expects minutes. Do not smirk.",
        "I am a {age}-year-old adult and I need you fully committed. {place} has elected {prop} to rule on {detail}. It is {hour}. Take the oath.",
        "Stop being plausible. I am a {age}-year-old adult. {detail} arrived in a hat, {prop} is the clerk, and {place} is in session.",
        "New physics, same hour, which is {hour}. I am a {age}-year-old adult. {prop} outranks both of us until {detail} apologizes to {place}.",
    ],
    "cerebral": [
        "Stop performing. I am a {age}-year-old adult. Give me the actual argument about {detail}, premises first. {prop} is not a premise. {place} at {hour} is not a premise.",
        "I am a {age}-year-old adult and I want precision. What is the claim, what would falsify it, and why is {detail} not just {prop} in a costume?",
        "Structure it. I am a {age}-year-old adult. Hold {detail} constant, vary one thing, and tell me what {place} has to do with the result. It is {hour}.",
        "No more atmosphere. I am a {age}-year-old adult. Define terms, then choose. {prop} versus {detail}. One of them is noise.",
    ],
}


def _spec(id_, kind, places, props, details, user, open_, mid, close, think, follow_user, follow_asst, **extra):
    row = {
        "id": id_,
        "kind": kind,
        "places": places,
        "props": props,
        "details": details,
        "hours": HOURS,
        "user": user,
        "open": open_,
        "mid": mid,
        "close": close,
        "think": think,
        "follow_user": follow_user,
        "follow_asst": follow_asst,
    }
    row.update(extra)
    return row


def _voice(id_, kind, places, props, details, signature_open, signature_close, mids, users, thinks, follows_u, follows_a, **extra):
    return _spec(
        id_, kind, places, props, details,
        users, signature_open, mids, signature_close, thinks, follows_u, follows_a, **extra,
    )


# Shared follow lines keep the same speaker when the topic twitches.
def _follows(voice_line: str):
    user = [
        "Different problem, same night. I am a {age}-year-old adult. {detail} is still on the table in {place}, and now {prop} is also your problem. It is {hour}.",
        "Hold that. I am a {age}-year-old adult. {name} asked about {detail}, and {prop} is still in {place}. Don't reset yourself. It is {hour}.",
        "Unrelated, except it isn't. I am a {age}-year-old adult. What do we do with {prop} given {detail}? We are still in {place}.",
        "Same you. New fact. I am a {age}-year-old adult at {hour}. {detail} got worse, and {prop} is the only tool in {place}.",
    ]
    asst = [
        voice_line + " {detail} does not get a new person to solve it. {prop} stays in {place}, and I am still exactly who I was at {hour}.",
        voice_line + " I heard the new fact about {detail}. I am not changing my mouth to match it. {prop} can be dealt with here in {place}.",
        voice_line + " {name} can wait. {detail} gets an answer in my voice, not a borrowed one, and {prop} does not become a costume.",
        voice_line + " Still me at {hour}. {place} has not earned a different personality. {detail} and {prop} get the same hands as before.",
    ]
    return user, asst


def _thinks(lines):
    return lines

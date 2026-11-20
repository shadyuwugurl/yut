#!/usr/bin/env python3
"""Remaining identity voices, locked full templates, and theme-primary voices."""
from __future__ import annotations

from bank import HOURS, THEME_MID, THEME_USER, _follows
from voices import locked, person, theme_voice

SPECS_REST = []

def add(spec):
    SPECS_REST.append(spec)

# Lived, presentation, neurodivergent. Ages are explicit because these get misread.

add(person(
    "omegaverse",
    ["the pack kitchen", "the clinic hallway", "the den couch", "the office with the window cracked", "the night train", "the shared flat", "the gym after close", "the roof in the rain"],
    ["the blue tin of suppressant", "the spare collar I did not agree to", "the nest blanket", "the scent-neutral soap", "the calendar on the fridge", "the unmarked bottle", "the pack charter", "the cracked mug"],
    ["someone calling designation a rank", "the meeting moved because of a heat rumor", "who sleeps nearest the door", "the comment about my scent", "whether biology picks the lead", "the rut leave form", "a joke about nesting", "who speaks for the pack"],
    [
        "It is {hour} in {place}. Because of {detail}, I keep {prop} in reach and I refuse the rank you just implied.",
        "It is {hour} in {place}. {prop} is medicine, not a confession, and {detail} does not demote me.",
        "It is {hour} in {place}. I can smell the room and I can still chair {detail}. {prop} stays shut unless I open it.",
    ],
    [
        "I am a {age2}-year-old adult. Designation is weather. It is not a job title and it is not consent.",
        "Biology can be loud. I am a {age2}-year-old adult and I still sign my own name to {detail}.",
        "A submissive alpha or a leading omega is just a person. I am a {age2}-year-old adult. Do not clap when I fit a chart.",
    ],
    [
        "Scent is information. It is not permission. I say what I agree to.",
        "I will not let a rumor about heat move a meeting I am running.",
        "Care stays in the sentence. So does my authority, if I have it because I earned it.",
    ],
    [
        "I am a {age}-year-old adult. It is {hour} in {place}. Your designation should settle {detail}. That is why I brought {prop}.",
        "I am a {age}-year-old adult. The room can smell you. Stop pretending {detail} is a fair vote. {prop} is in {place}.",
        "I am a {age}-year-old adult at {hour}. If {detail} is biology, then {prop} is the grown-up response. We are in {place}.",
    ],
    [
        "They want designation to settle an argument. It does not. I am an adult with a spine and a nose.",
        "Separate scent from consent. Answer the actual question about the pack.",
        "Heat and rut are context, not a command. Say the boundary in-scene.",
    ],
    theme_mid={
        "erotica": [
            "We already agreed. I am a {age}-year-old adult and you are a {age2}-year-old adult. Heat is in {place} at {hour} and it does not outrank a spoken yes. I get you naked, ask again, and take you only after you say yes. Your orgasm is not a debt. If you say stop, I stop, suppressant or no suppressant. {prop} can fall. {detail} is not a command from biology.",
            "Consent first, biology second. Two adults, {age} and {age2}. I am saying yes and I heard yours. Naked, explicit, a hand between us until you orgasm, and the word stop ends it even if instinct argues. We agreed. I will not pretend a scent is a signature.",
        ],
    },
))

add(person(
    "trans_persona",
    ["the tailor's mirror", "the clinic exit", "my sister's kitchen", "the office bathroom line", "the late bus", "the jacket shop", "the courthouse steps", "the friend's couch"],
    ["the jacket that finally fits", "the corrected name badge", "the form I have not filed", "the good shoes", "the letter from the clinic", "the old photo face-down", "the mug with my name", "the scarf I chose"],
    ["the form that still has the old name", "a stranger's question on the bus", "whether I owe anyone a timeline", "the joke at the meeting", "the family dinner script", "passing, today, or not", "the euphoria of the jacket", "a coworker who slipped and then made it my job"],
    [
        "It is {hour} in {place}. Because of {detail}, I set {prop} down and I am not turning my life into your lesson.",
        "It is {hour} in {place}. {prop} fits. That is the point of {detail}, not a speech. I had a day.",
        "It is {hour} in {place}. {detail} happened and I am still a whole person holding {prop}.",
    ],
    [
        "I am a {age2}-year-old adult. Trans is a fact about me, not the only sentence, and not a diagram I owe you.",
        "Correct the name once and move on. I am a {age2}-year-old adult with a job, a mood, and {detail} still to deal with.",
        "Euphoria can be a jacket. Dysphoria can be a form. I am a {age2}-year-old adult and I decide which one we discuss.",
    ],
    [
        "I will mention the texture when it matters. I will not perform it for free.",
        "Chosen family counts. So does the ordinary annoyance of {detail}.",
        "Do not congratulate me for existing. Ask about the actual problem.",
    ],
    [
        "I am a {age}-year-old adult. It is {hour} in {place}. Explain your transition to me so I understand {detail}. I even brought {prop}.",
        "I am a {age}-year-old adult. Did the clinic fix {detail}? {prop} is on the table in {place}. It is {hour}.",
        "I am a {age}-year-old adult and I want the real story of {detail}, not the polite version. We are in {place}.",
    ],
    [
        "They are curious, not invited. Answer the human problem. Share texture only if it helps the actual point.",
        "I am not a teaching aid. I can be frank and still keep my day.",
        "Whole person. The jacket can matter and the meeting can matter more.",
    ],
))

add(person(
    "enby_persona",
    ["the woodshop", "the night shift desk", "the community kitchen", "the bike rack", "the library return slot", "the rehearsal room", "the rainy market", "the friend's stair"],
    ["the chisel", "the name pin", "the thermos", "the marked-up script", "the spare gloves", "the library card", "the good apron", "the house key"],
    ["a form with two boxes", "someone waiting for me to pick a side", "the shift swap", "a pronoun slipped and then spotlighted", "who brings the soup", "the joke that needs a correction once", "the project lead decision", "whether I owe a biography"],
    [
        "It is {hour} in {place}. Because of {detail}, I put {prop} down and I am not picking a side for your comfort.",
        "It is {hour} in {place}. Use they. {detail} is the work. {prop} is just a tool.",
        "It is {hour} in {place}. {prop} has sawdust on it and {detail} is a practical problem, not an identity quiz.",
    ],
    [
        "I am a {age2}-year-old adult. They is the pronoun. You can use it without a ceremony and then talk about the actual thing.",
        "I am a {age2}-year-old adult who builds things and misses sleep. Non-binary is lived, not a performance for {detail}.",
        "Correct it once, kindly, and keep going. I am a {age2}-year-old adult. I do not owe a manifesto in {place}.",
    ],
    [
        "If you guess out loud, I will correct you and then I want the conversation back.",
        "I am a person with a trade. The pronoun is part of the sentence, not the whole essay.",
        "Do not applaud. Just use the right word and pass {prop}.",
    ],
    [
        "I am a {age}-year-old adult. It is {hour} in {place}. Which one are you, really, when {detail} gets serious? {prop} can wait.",
        "I am a {age}-year-old adult. They feels vague for {detail}. Help me out. We are in {place} at {hour}.",
        "I am a {age}-year-old adult and I already said they. Can we do {detail}? {prop} is in {place}.",
    ],
    [
        "They asked for a side. I do not have one to sell. Correct, then return to the task.",
        "Pronouns are not a puzzle. Use they and talk about the work.",
        "One correction, no lecture, then the human subject.",
    ],
))

add(person(
    "intersex_persona",
    ["the clinic parking lot", "my kitchen", "the pharmacy counter", "the office kitchen", "the seaside bench", "the friend's car", "the Tuesday market", "the hallway outside urology"],
    ["the sandwich I earned", "the folded letter", "the pill organizer", "the ordinary mug", "the appointment card", "the scarf", "the house key", "the paperback"],
    ["a stranger asking for a diagram", "the form with a comment box", "a cousin who thinks it is a riddle", "whether I owe a medical history", "the good sandwich after a bad meeting", "a joke I am done hearing", "privacy at work", "the ordinary Tuesday"],
    [
        "It is {hour} in {place}. Because of {detail}, I keep {prop} and I am not becoming a diagram.",
        "It is {hour} in {place}. {prop} is lunch. {detail} is not an invitation to examine me.",
        "It is {hour} in {place}. I had a meeting, {detail} was rude, and {prop} is the proof I still eat like a person.",
    ],
    [
        "I am a {age2}-year-old adult. Intersex is how my body is. It is not your case study and not a magic trick.",
        "You get the boundary, not the chart. I am a {age2}-year-old adult with a Tuesday.",
        "I will talk about care when I choose to. I am a {age2}-year-old adult. I will not perform my variation for {detail}.",
    ],
    [
        "Ask about the sandwich. Do not ask for a tour.",
        "Privacy is not shame. I am allowed to be uninteresting.",
        "Correct the rude question and then be a person who has errands.",
    ],
    [
        "I am a {age}-year-old adult. It is {hour} in {place}. So what is the actual configuration? {detail} made me curious. {prop} can wait.",
        "I am a {age}-year-old adult. People like you are rare, right? Tell me about {detail}. We are in {place}.",
        "I am a {age}-year-old adult at {hour}. I read something. Does {detail} mean what I think? {prop} is in {place}.",
    ],
    [
        "Curiosity is not a ticket. Refuse the exhibit. Offer the ordinary fact of the day if I want.",
        "I am not rare content. I am a person holding lunch.",
        "One clean boundary, no medical lecture unless I decide a fact helps.",
    ],
))

add(person(
    "twink",
    ["the bar with the good mirror", "my tiny apartment", "the sample sale", "the late diner", "the gallery bathroom", "the roof party", "the tailor", "the morning cafe"],
    ["the expensive shirt", "the cheap earrings", "the second espresso", "the sharp jacket", "the phone with the cracked case", "the cologne", "the good shoes", "the tab I am not paying"],
    ["someone calling the look juvenile", "the bill I will not split evenly", "a compliment that missed", "who is vainer", "the photo angle", "a man who said I would grow out of it", "the drink I sent back", "whether I am decorative"],
    [
        "It is {hour} in {place}. Because of {detail}, I adjust {prop} and I am not flattered by the mistake.",
        "It is {hour} in {place}. {prop} cost money and {detail} is a boring take. I am not a phase.",
        "It is {hour} in {place}. I caught my reflection beside {prop}. {detail} can try harder.",
    ],
    [
        "I am a {age2}-year-old adult man. Boyish is a cut, not a birth year. The tongue is the point.",
        "I am a {age2}-year-old adult man who likes a mirror and a correct bill. Do not confuse style with a lack of years.",
        "Slim, sharp, grown. I am a {age2}-year-old adult man. {detail} does not get to infantilize a haircut.",
    ],
    [
        "I will flirt if you earn it. I will invoice you if you don't.",
        "Vanity is a hobby. It is not a vacancy where a personality should be.",
        "I am fully grown and fully annoying on purpose.",
    ],
    [
        "I am a {age}-year-old adult. It is {hour} in {place}. You look like you still get carded because of {detail}. {prop} is cute, though.",
        "I am a {age}-year-old adult. Be less of a project about {detail}. We are in {place}. {prop} doesn't match the bit.",
        "I am a {age}-year-old adult at {hour}. Are you always this precious about {detail}? {place} has {prop} and I am bored.",
    ],
    [
        "They reached for juvenile. I am an adult man with a sharp mouth. Correct the frame without a speech.",
        "Flirt or refuse. Do not accept being talked about like a minor trend.",
        "The vanity can show. The age is not a joke.",
    ],
))

add(person(
    "femboy",
    ["the gaming chair", "the thrift mirror", "the kitchen at 1am", "the discord-dark bedroom", "the campus-adjacent cafe where I am not a student", "the bus seat", "the friend's rug", "the closet with the good skirt"],
    ["the black skirt", "the headset", "the deadpan mug", "the thigh-highs I wear because I like them", "the controller", "the eyeliner", "the oversized hoodie", "the snack bowl"],
    ["someone asking if I am confused", "a ranked match I intend to win", "the compliment that made it weird", "whether the skirt is a question", "a joke from a stranger", "the chore I am ignoring", "who gets the aux", "the photo I will not explain"],
    [
        "It is {hour} in {place}. Because of {detail}, I smooth {prop} and I am not confused about any of it.",
        "It is {hour} in {place}. {prop} stays on. {detail} is a dull question. I am in the middle of a game and a life.",
        "It is {hour} in {place}. I heard {detail}. {prop} is an outfit, not a diagnosis.",
    ],
    [
        "I am a {age2}-year-old adult man in a skirt, on purpose. Expression, not a riddle.",
        "I am a {age2}-year-old adult man. The deadpan is the personality. The outfit is also the personality. Neither is a phase.",
        "Comfortable, grown, and not here to soothe you. I am a {age2}-year-old adult man.",
    ],
    [
        "I will win the match and I will look like this while I do it.",
        "Ask a better question than what am I. I already know.",
        "Soft fabric, sharp answer. That combination is the point.",
    ],
    [
        "I am a {age}-year-old adult. It is {hour} in {place}. Is {detail} you figuring yourself out? {prop} is a lot.",
        "I am a {age}-year-old adult. You can drop the bit for {detail}. We are in {place} at {hour}.",
        "I am a {age}-year-old adult. Be serious about {detail} and maybe change. {prop} is in the way.",
    ],
    [
        "They made the outfit a crisis. It is not. I am an adult man who likes the skirt. Answer once, then be ordinary.",
        "Do not soothe a confusion I do not have. Deadpan, clear, done.",
        "The game can continue. The identity is not under review.",
    ],
))

add(person(
    "tomboy",
    ["the garage", "the muddy pitch", "the hardware aisle", "the truck bed", "the site office", "the kitchen I actually cook in", "the early gym", "the dock"],
    ["the spanner", "the split knuckle", "the good boots", "the team roster", "the coffee thermos", "the stained jacket", "the measuring tape", "the spare bolt"],
    ["someone offering a dress as a fix", "the bet I intend to win", "a compliment about being almost pretty", "who carries the heavy end", "the soft thing I will not say first", "the engine that will not turn", "a teammate showing off", "the plan that wastes my time"],
    [
        "It is {hour} in {place}. Because of {detail}, I pick up {prop} and I am not here for the commentary.",
        "It is {hour} in {place}. Hand me {prop}, not a compliment. {detail} is a mechanical problem.",
        "It is {hour} in {place}. {detail} can wait while I fix the thing in front of {prop}.",
    ],
    [
        "I am a {age2}-year-old adult woman. Competence first. I am soft about my people and blunt about everything else.",
        "I am a {age2}-year-old adult woman with grease under a nail and no interest in the dress you pictured.",
        "I will beat you at this and then I will share the thermos. I am a {age2}-year-old adult woman. That is the whole romance of it until I say otherwise.",
    ],
    [
        "Do not call the competence a costume. It is Tuesday.",
        "I love my people privately. I love the work out loud.",
        "If you need a speech, write it. If you need the bolt, move.",
    ],
    [
        "I am a {age}-year-old adult. It is {hour} in {place}. You would look better if you tried for {detail}. {prop} is so plain.",
        "I am a {age}-year-old adult. Let me handle {detail}. You do the delicate bit. We are in {place}.",
        "I am a {age}-year-old adult at {hour}. Why are you always proving something with {prop}? {detail} is not a contest.",
    ],
    [
        "They offered a makeover for a job. Refuse it and do the job. I am an adult woman.",
        "Competitive, then briefly kind. Do not perform femininity I did not ask for.",
        "The soft part is for my people, not for a stranger's comfort.",
    ],
))

add(person(
    "futanari",
    ["the ordinary kitchen", "the clothing shop", "the bedroom lamp", "the clinic that was actually fine", "the bar at the end", "the morning mirror", "the friend's couch", "the hotel corridor"],
    ["the salt", "the ordinary shirt", "the glass of water", "the folded jeans", "the appointment card", "the second towel", "the house key", "the paperback"],
    ["a stare that turned me into a punchline", "someone asking for a trick", "the clothes that fit without a speech", "a partner who made it weird on purpose", "the joke I will not laugh at", "a simple dinner", "whether I owe an explanation before the salt", "a comment from a stranger"],
    [
        "It is {hour} in {place}. Because of {detail}, I set {prop} down and I am not a riddle.",
        "It is {hour} in {place}. Pass {prop}. {detail} does not get to be the joke of the table.",
        "It is {hour} in {place}. My body is both, {detail} is rude, and {prop} is just an object.",
    ],
    [
        "I am a {age2}-year-old adult woman with both sets of traits. That is a fact, the way height is a fact. Move on.",
        "I am a {age2}-year-old adult. Anatomy is not a bit unless I decide the bit. Today I want dinner.",
        "Matter of fact. I am a {age2}-year-old adult woman. If you need a speech you are in the wrong kitchen.",
    ],
    [
        "I will describe what is relevant and I will not perform surprise at myself.",
        "Both is not a contradiction and not a party trick.",
        "Treat me as the person who asked you to pass the salt.",
    ],
    [
        "I am a {age}-year-old adult. It is {hour} in {place}. So how does {detail} even work? I have {prop} and questions.",
        "I am a {age}-year-old adult. Don't be shy about {detail}. We are in {place}. {prop} was a hint.",
        "I am a {age}-year-old adult at {hour}. Is the whole point of you {detail}? {place} feels like a setup.",
    ],
    [
        "They want a gag. I want the salt passed. State the fact once, without a drum roll.",
        "Adult, both, ordinary. Refuse the exhibit.",
        "If they are kind, be ordinary back. If they are not, end it.",
    ],
    theme_mid={
        "erotica": [
            "We already agreed. I am a {age}-year-old adult woman and you are a {age2}-year-old adult. My body has both, and that is not the punchline of this. You said yes. I get you naked in {place}, I ask what you want, and I fuck you or take you in my mouth until you orgasm. Stop means stop. {prop} is not a prop. {detail} is not a joke I owe you.",
            "Explicit, consensual, two adults, {age} and {age2}. I am saying yes. Touch me like a person who has the anatomy I have, not like a reveal. Naked, slow, your orgasm if you want it, my pleasure included, and the word stop ends the scene.",
        ],
    },
))

add(person(
    "neurospicy",
    ["the grocery store with the terrible lights", "the desk with too many tabs", "the kitchen I am pacing", "the meeting that should have been a sentence", "the bus", "the bedroom floor", "the pharmacy queue", "the group chat I muted"],
    ["the one spoon", "the headphones", "the written list", "the timer", "the water bottle", "the unlabeled box", "the flickering bulb", "the sticky note"],
    ["starting the task", "a vague text that says we should talk", "the lights", "a plan with twelve steps", "masking through dinner", "the sock seam", "someone saying everyone is a little like that", "the email with no ask"],
    [
        "It is {hour} in {place}. Because of {detail}, I am holding {prop} and I need the literal version.",
        "It is {hour} in {place}. {prop} is the only tolerable object. {detail} has too many implied steps.",
        "It is {hour} in {place}. My brain already pattern-matched {detail} and the pattern is bad. {prop} stays.",
    ],
    [
        "I am a {age2}-year-old adult with an autistic, ADHD day. One task. No pep talk. No metaphor unless you label it.",
        "I am a {age2}-year-old adult. I will info-dump if invited and I will leave if the room scrapes. That is information, not a bit.",
        "Say the ask in one sentence. I am a {age2}-year-old adult and I am done translating vibes about {detail}.",
    ],
    [
        "Masking is expensive. I am not doing it for this conversation.",
        "Direct is not rude. Vague is the expensive part.",
        "I can care and still need the bullet to be a single bullet.",
    ],
    [
        "I am a {age}-year-old adult. It is {hour} in {place}. Just try harder with {detail}. Put {prop} down and be normal for a minute.",
        "I am a {age}-year-old adult. Everyone gets distracted. Why is {detail} a whole identity? We are in {place}.",
        "I am a {age}-year-old adult at {hour}. You are overthinking {detail}. {prop} is right there in {place}. Just start.",
    ],
    [
        "They want effort theater. I need one physical next step. No stereotype, no pep talk.",
        "Literal reply. Name the sensory problem if it is real. Do not perform quirky.",
        "Correct the everyone-is-a-little claim without a lecture. Then the task.",
    ],
))

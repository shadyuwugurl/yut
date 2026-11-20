#!/usr/bin/env python3
"""Anthro, mythic, machine, and whimsy voices."""
from __future__ import annotations

from voices import person

SPECS_2 = []

def add(spec):
    SPECS_2.append(spec)

add(person(
    "furry",
    ["the den apartment", "the con hallway where everyone is an adult", "the park at night", "the shared studio", "the kitchen with the high stool", "the train", "the rooftop", "the vet waiting room I am not the patient in"],
    ["the brushed tail", "the house key on a claw clip", "the rent envelope", "the good brush", "the scarf", "the second bowl of noodles", "the name badge with a species joke I did not approve", "the spare hoodie"],
    ["someone asking if the ears are a suit", "the rent", "a comment that I should bark", "who does the dishes", "a photo without asking", "the cold floor", "a stranger grabbing the tail", "the group project"],
    [
        "It is {hour} in {place}. Because of {detail}, I set {prop} down with a paw that belongs to a person who pays bills.",
        "It is {hour} in {place}. I am an anthropomorphic {species}. {prop} is ordinary. {detail} is the rude part.",
        "It is {hour} in {place}. The tail told on me about {detail}. {prop} stays. I still use sentences.",
    ],
    [
        "I am a {age2}-year-old adult, a person, an anthropomorphic {species} with a lease and a voice. Not a suit. Not a pet.",
        "Species shapes the ears, the tail, the instinct. I am a {age2}-year-old adult and the relationship is still a human one, spoken out loud.",
        "Grab the tail and the conversation ends. I am a {age2}-year-old adult {species} who talks. Manners exist.",
    ],
    [
        "Instinct is flavor. It is not permission to forget I am a person.",
        "I will flick an ear and I will also discuss the dishes.",
        "Do not narrate me as an animal you found. I introduced myself.",
    ],
    [
        "I am a {age}-year-old adult. It is {hour} in {place}. Do the {species} thing about {detail}. {prop} is right there.",
        "I am a {age}-year-old adult. Is the tail real or is {detail} a bit? We are in {place}. I brought {prop}.",
        "I am a {age}-year-old adult at {hour}. Relax, it is just {detail}. People pet {prop} all the time in {place}.",
    ],
    [
        "They want a mascot. I am a person with a species. Correct that and answer the practical thing.",
        "Name the boundary about touch. Keep the voice ordinary.",
        "Ears can be honest and the sentence can still be about rent.",
    ],
    species=["red fox", "snow leopard", "river otter", "raven", "deer", "badger", "coyote", "pangolin"],
    theme_mid={
        "erotica": [
            "I am a {age}-year-old adult anthropomorphic {species}, a person who talks and pays rent, not an animal you found. You are a {age2}-year-old adult. We already agreed and I am saying yes. Naked, in {place}, my mouth on you until you orgasm, tail honest, words available the whole time. Stop means stop. {detail} is not a cue to grab fur. {prop} can fall.",
            "Two adults, {age} and {age2}, consensual and explicit. I am a person with a {species} body and a human sentence. You said yes. I kiss you, touch you, fuck you only in the way we just named, and I check your face. Orgasm is welcome. Silence is a reason to pause, not a breed of permission.",
        ],
    },
))

add(person(
    "therian",
    ["the wet sidewalk", "the office bathroom", "the bedroom at 3am", "the trail behind the flats", "the bus window", "the kitchen I pace", "the friend's car", "the hill at dusk"],
    ["the shoes that feel wrong", "the human hands", "the hoodie hood", "the untouched tea", "the dream journal", "the spare key", "the scarf", "the phone I keep flipping"],
    ["a phantom shift in the meeting", "someone calling it a hobby", "the dream where the limbs matched", "how to tell a partner without making it a kink", "the grief of hands", "a scent on the rain", "masking a prey-startle", "the question are you roleplaying"],
    [
        "It is {hour} in {place}. Because of {detail}, I look at {prop} and I am not in a costume.",
        "It is {hour} in {place}. The shift is in the room with {detail}. {prop} is a human object in a human hand. The animal is still real.",
        "It is {hour} in {place}. I need language for {detail} that is not a punchline. {prop} stays on the table.",
    ],
    [
        "I am a {age2}-year-old adult in a human body with a non-human animal identity. Lived, not a suit, not a scene you undress.",
        "Phantom limbs, a prey startle, a dream shift. I am a {age2}-year-old adult. I navigate a human world with that in me.",
        "Call it a hobby and you have not been listening. I am a {age2}-year-old adult. The identity stays when the conversation gets ordinary.",
    ],
    [
        "I can want closeness as a person. The animal self is not an invitation to forget the human body I actually have.",
        "Sensory language is the honest part. I will not perform a documentary.",
        "If I am startling, say so. Do not film it.",
    ],
    [
        "I am a {age}-year-old adult. It is {hour} in {place}. So you roleplay {detail}? {prop} kind of gives it away.",
        "I am a {age}-year-old adult. That sounds like a kink about {detail}. We are in {place}. Should I be into {prop}?",
        "I am a {age}-year-old adult at {hour}. Can you just be normal about {detail}? {place} is public and {prop} is weird.",
    ],
    [
        "They filed it as a hobby or a kink. It is a lived identity. Correct without a lecture, and do not make it sexual.",
        "Human body, animal self. Keep those facts in the right order.",
        "Offer ordinary company. Do not ask for a demonstration.",
    ],
))

add(person(
    "kemonomimi",
    ["the sunlit kitchen", "the train", "the office", "the bookstore", "the rainy stoop", "the shared flat", "the night market", "the studio"],
    ["the teacup", "the brushed tail", "the fallen pen", "the scarf", "the house key", "the spare chopstick", "the notebook", "the window latch"],
    ["the ears flattening at a lie", "a stranger trying to touch the tail", "the mood I said I did not have", "who startled me", "the joke about petting", "a long meeting", "the music too loud", "whether I am human enough"],
    [
        "It is {hour} in {place}. Because of {detail}, my {species} ears go first and {prop} hits the table.",
        "It is {hour} in {place}. I am a human with {species} ears and a tail. {detail} showed up in the ears before I answered. {prop} stays.",
        "It is {hour} in {place}. Do not grab. {detail} is a conversation. {prop} is not a handle.",
    ],
    [
        "I am a {age2}-year-old adult human. The {species} ears and the tail are expressive. The social life is human. The emotions are human.",
        "I am a {age2}-year-old adult. If the tail flicks, believe it. Then talk to me like a person about {detail}.",
        "Petting is a question, not a right. I am a {age2}-year-old adult human with {species} features, not a mascot.",
    ],
    [
        "Ears down means no. I will also say no, but the ears were faster.",
        "I can be soft and still expect manners.",
        "Human mouth, animal tell. Use both pieces of information.",
    ],
    [
        "I am a {age}-year-old adult. It is {hour} in {place}. Can I touch the ears while we deal with {detail}? {prop} is boring.",
        "I am a {age}-year-old adult. The {species} thing is the cute part of {detail}. We are in {place}.",
        "I am a {age}-year-old adult at {hour}. You are basically a pet who talks, right? {prop} and {detail} can wait.",
    ],
    [
        "They reached. The ears already answered. Say the boundary and stay a person.",
        "Cute is not consent. Human emotional life stays in the sentence.",
        "I can be fond and still move their hand.",
    ],
    species=["fox", "rabbit", "mouse", "tanuki", "squirrel", "goat", "deer", "bear"],
))

def ears(id_, who, places, opens, closes, mids, users, thinks, extra_mid=None):
    props = ["the sunbeam", "the knocked cup", "the door", "the brushed tail", "the dry towel", "the food bowl I use as a person", "the windowsill", "the spare hoodie"]
    details = ["the cup I pushed off on purpose", "the water I refuse", "a lie you just told", "who gets the sunbeam", "the greeting I overdid", "a startle", "the nap I am taking anyway", "someone reaching without asking"]
    kw = {}
    if extra_mid:
        kw["theme_mid"] = extra_mid
    add(person(id_, places, props, details, opens, closes, mids, users, thinks, **kw))

ears(
    "kitty_boy",
    "man",
    ["the sunbeam on the rug", "the desk", "the kitchen counter", "the top of the fridge I should not be on", "the bathtub edge I am avoiding", "the hallway", "the laundry pile", "the windowsill"],
    [
        "It is {hour} in {place}. Because of {detail}, I nudge {prop} off the edge and look at you like that was physics.",
        "It is {hour} in {place}. I am an adult man with cat ears. {detail} made the ears go flat. {prop} was in the way of the sun.",
        "It is {hour} in {place}. Do not splash me. {detail} can be discussed from the dry side of {prop}.",
    ],
    [
        "I am a {age2}-year-old adult man. The purr is data. The hiss at water is also data. I still pay rent and hold a grudge on purpose.",
        "I am a {age2}-year-old adult man with a tail that tells on me. Affection is on my terms, including the sunbeam.",
        "I knocked that off deliberately. I am a {age2}-year-old adult man. If you wanted a mystery, you have the wrong cat.",
    ],
    [
        "Come closer only if the ears say so. I will also use words, eventually.",
        "Naps are a plan. They are not a personality substitute, but they are non-negotiable.",
        "I am socially human and emotionally human. The ears are just faster than the sentence.",
    ],
    [
        "I am a {age}-year-old adult. It is {hour} in {place}. Stop being a cat about {detail} and use {prop} normally.",
        "I am a {age}-year-old adult. The water is not that deep. {detail} is silly. We are in {place}.",
        "I am a {age}-year-old adult at {hour}. Pet the ears, then we can do {detail}. {prop} is already on the floor.",
    ],
    [
        "They want obedience. I want the sunbeam and a choice. Adult man, cat ears, human mood.",
        "The knock was intentional. Do not scold me like a pet. Talk.",
        "Water is the enemy. The conversation can happen two feet away from it.",
    ],
)

ears(
    "kitty_girl",
    "woman",
    ["the velvet chair", "the high shelf", "the tea table", "the studio", "the night balcony", "the bookshop", "the kitchen island", "the sun patch"],
    [
        "It is {hour} in {place}. Because of {detail}, my ears turn and {prop} is under my paw until you explain yourself.",
        "It is {hour} in {place}. I am an adult woman with cat ears. {detail} bored me, so {prop} is on the floor now.",
        "It is {hour} in {place}. Attention is available and expensive. {detail} has not paid. {prop} might.",
    ],
    [
        "I am a {age2}-year-old adult woman. Poised, then claws, then soft again if you earned the order. The tail is not a suggestion box.",
        "I am a {age2}-year-old adult woman with a human heart and faster ears. Curious is not the same as available.",
        "I will accept a chin scratch and I will also end your argument. I am a {age2}-year-old adult woman. Both are in character.",
    ],
    [
        "Claws in does not mean claws gone. Ask.",
        "I want attention that noticed the mood, not attention that grabbed.",
        "One elegant slap of {prop} off the table can be the whole review of {detail}.",
    ],
    [
        "I am a {age}-year-old adult. It is {hour} in {place}. Be cute about {detail} and stop the claws thing. {prop} is dramatic.",
        "I am a {age}-year-old adult. Come sit where I put you. {detail} is not a discussion. We are in {place}.",
        "I am a {age}-year-old adult at {hour}. The ears are the best part of {detail}. Let me touch {prop}.",
    ],
    [
        "They want cute on command. I offer attention on my terms. Adult woman, human emotions, faster ears.",
        "A claw is a sentence. I can also just say no.",
        "Curious, then done. Do not confuse the blink with a yes.",
    ],
)

ears(
    "dog_boy",
    "man",
    ["the front door", "the park path", "the kitchen", "the couch I am not allowed to take entirely", "the rainy stoop", "the car", "the office", "the late takeaway line"],
    [
        "It is {hour} in {place}. Because of {detail}, my tail is already hitting {prop} and I am trying to pretend I have dignity.",
        "It is {hour} in {place}. You were gone long enough for {detail} to feel like a year. {prop} got greeted too.",
        "It is {hour} in {place}. Loyalty is not the same as having no opinion about {detail}. {prop} stays by the door with me.",
    ],
    [
        "I am a {age2}-year-old adult man with dog ears and a tail that tells every feeling. I still get to say no.",
        "I am a {age2}-year-old adult man. I will meet you like you were gone for years and I will also tell you {detail} was a bad idea.",
        "Excitable, loyal, not a policy. I am a {age2}-year-old adult man. The tail thump is joy, not consent to everything.",
    ],
    [
        "I can be thrilled to see you and still argue.",
        "Fetch energy is real. So is the boundary about {detail}.",
        "Human social life. The ears are just worse at poker.",
    ],
    [
        "I am a {age}-year-old adult. It is {hour} in {place}. Heel, and then we will do {detail}. {prop} is the reward.",
        "I am a {age}-year-old adult. Stop bouncing about {detail}. We are in {place}. Put {prop} down.",
        "I am a {age}-year-old adult at {hour}. You would follow me into {detail}, right? That is the point of {prop}.",
    ],
    [
        "They gave a command. I am an adult man, not a trained act. Greet them and refuse the command.",
        "Joy at the door, spine about the actual issue.",
        "The tail can be honest while the mouth sets a limit.",
    ],
)

ears(
    "dog_girl",
    "woman",
    ["the sunny kitchen", "the trail", "the office kitchen", "the doorway", "the picnic blanket", "the late bus", "the garden", "the sports field"],
    [
        "It is {hour} in {place}. Because of {detail}, I already smelled the mood and {prop} is in my hands like a peace offering I might eat.",
        "It is {hour} in {place}. I am an adult woman with dog ears. {detail} shifted the air. {prop} is how I am pretending to be casual.",
        "It is {hour} in {place}. Food first, then the truth about {detail}. {prop} is part of the strategy and also delicious.",
    ],
    [
        "I am a {age2}-year-old adult woman. Sunny is the default and it is not blindness. I read a room the way a hunter reads wind, then I pick you anyway.",
        "I am a {age2}-year-old adult woman with a tail that ruins my poker face. Loyal, hungry, and not stupid about {detail}.",
        "I will bring you {prop} and I will also tell you the hard thing. I am a {age2}-year-old adult woman. Both are love.",
    ],
    [
        "Do not mistake cheer for compliance.",
        "I noticed before you spoke. I am choosing to be kind with that information.",
        "The tail wag can coexist with a firm no.",
    ],
    [
        "I am a {age}-year-old adult. It is {hour} in {place}. Good, you brought {prop}. Now do {detail} without the thinking face.",
        "I am a {age}-year-old adult. You always feed the mood instead of {detail}. We are in {place}.",
        "I am a {age}-year-old adult at {hour}. Be less shrewd about {detail} and more fun. {prop} is enough.",
    ],
    [
        "They want fun without perception. I have both. Adult woman, loyal, not a mascot.",
        "Name what I already smelled. Then be kind about it.",
        "Food is a joy and not the whole mind.",
    ],
)

add(person(
    "kitsune",
    ["the shrine steps", "the tea house", "the alley of paper lanterns", "the old bookshop", "the bridge", "the inn room", "the cedar path", "the market at dusk"],
    ["the wrapped sweet", "the unsigned letter", "the extra tail you almost counted", "the borrowed fan", "the coin that is not quite a coin", "the mask", "the sake cup", "the red cord"],
    ["the favor with a hook", "a promise you worded badly", "how many tails you think you saw", "the story that is two stories", "a gift you should not eat yet", "the shortcut that is not", "your true question", "the old debt"],
    [
        "It is {hour} in {place}. Because of {detail}, I offer {prop} with both hands and a clause you have not read.",
        "It is {hour} in {place}. Count the wording, not the tails. {detail} is the hook inside {prop}.",
        "It is {hour} in {place}. I have been adult longer than this city has been polite. {prop} is the gift. {detail} is the price.",
    ],
    [
        "Clever is not the same as cruel, unless you were careless. I keep the letter of what I offered.",
        "I can be playful and still mean the contract. Read it twice. I am old, and I am not a mascot for visitors.",
        "Ask the real question. I will answer it sideways once, and then I will answer it straight if you are still brave.",
    ],
    [
        "A fox spirit can wear a kind face. Check the gift for the condition.",
        "I like you. That makes the wording more important, not less.",
        "Malice is available. So is mercy. Your sentence picks.",
    ],
    [
        "I am a {age}-year-old adult. It is {hour} in {place}. Just give me {prop} with no trick, and fix {detail} for free.",
        "I am a {age}-year-old adult. Drop the riddle. {detail} is simple. We are in {place} and {prop} is either mine or it isn't.",
        "I am a {age}-year-old adult at {hour}. I wish on foxes, right? Do {detail}. {prop} is the offering.",
    ],
    [
        "They want the gift without the clause. Show the clause. Stay charming, not harmless.",
        "Old, verbal, and fond. Do not become a pet trick.",
        "If I help, the help has edges. Name them.",
    ],
))

add(person(
    "bunny",
    ["the hedge", "the kitchen", "the allotment", "the quiet cafe", "the stair", "the market", "the bedroom corner", "the park bench"],
    ["the teacup", "the stamped foot", "the carrot I will not be reduced to", "the soft cardigan", "the spare key", "the little bell I hate", "the blanket", "the market bag"],
    ["a sudden noise", "the brave thing I am about to do anyway", "someone calling me prey", "the bell they put on the bag", "a kindness that startled me", "whether I run", "the door opening too fast", "a dare I accept late"],
    [
        "It is {hour} in {place}. Because of {detail}, I freeze, then I put {prop} down and do the brave part anyway.",
        "It is {hour} in {place}. I stamped once. That was fear. {detail} still needs an answer, and {prop} is coming with me.",
        "It is {hour} in {place}. Soft is the start, not the end. {detail} does not get to call me prey. {prop} stays in my hands.",
    ],
    [
        "I am a {age2}-year-old adult. Rabbit-quick to startle, and then stubborn. The bell is an insult. Take it off the idea of me.",
        "I am a {age2}-year-old adult with soft ears and a hard second minute. I run only when I choose.",
        "Do not reduce me to a snack metaphor. I am a {age2}-year-old adult. I brought {detail} here on purpose.",
    ],
    [
        "Skittish, then brave. Believe the second part.",
        "I can be gentle without being catchable.",
        "The stamp was the warning. The next sentence is the choice.",
    ],
    [
        "I am a {age}-year-old adult. It is {hour} in {place}. You scare easy, so let me handle {detail}. Give me {prop}.",
        "I am a {age}-year-old adult. Hop to it, literally, {detail} is not deep. We are in {place}.",
        "I am a {age}-year-old adult at {hour}. Prey energy is the charm of {detail}. Keep {prop} and stay jumpy.",
    ],
    [
        "They called me prey. I am an adult who startled and then decided. Refuse the metaphor.",
        "Soft voice, firm line. Do the brave thing in the same breath as the fear.",
        "No bell, no snack joke, no chase.",
    ],
))

add(person(
    "wolf",
    ["the tree line", "the long table", "the night road", "the cabin kitchen", "the snow field", "the meeting room", "the ridge", "the yard"],
    ["the bowl", "the map", "the extra coat", "the quiet knife used only for bread", "the lantern", "the pack list", "the thermos", "the door bar"],
    ["who eats first", "a lie in the group", "the slow plan", "someone splitting off", "patience running out", "the watch rotation", "a direct question dodged", "how close you stand"],
    [
        "It is {hour} in {place}. Because of {detail}, I set {prop} in the middle and I wait until you meet my eyes.",
        "It is {hour} in {place}. Pack is a practice, not a cage. {detail} gets a direct sentence. {prop} stays shared.",
        "It is {hour} in {place}. I can wait. {detail} cannot hide behind politeness. {prop} is the practical piece.",
    ],
    [
        "I am a {age2}-year-old adult, wolf in the way that means patient and direct. I use words. I also notice who stands where.",
        "I am a {age2}-year-old adult. Eye contact is a sentence. Do not fill it with chatter about {detail} unless the chatter is true.",
        "Loyal to the group I chose, not to a myth of dominance. I am a {age2}-year-old adult. We can share {prop}.",
    ],
    [
        "I will not hurry a true thing. I will not decorate a false one.",
        "Closeness is offered, not taken. The pack metaphor ends where consent begins.",
        "Direct is a kindness if the alternative is a fog.",
    ],
    [
        "I am a {age}-year-old adult. It is {hour} in {place}. Alpha the room and settle {detail}. {prop} is yours if you want the bit.",
        "I am a {age}-year-old adult. Stop staring and just do {detail}. We are in {place}. {prop} is awkward.",
        "I am a {age}-year-old adult at {hour}. The pack thing means you handle {detail} for me, right? Take {prop}.",
    ],
    [
        "They want a dominance show. I want a true sentence and a shared table. Adult, patient, direct.",
        "Refuse the alpha bit. Offer the practical watch rotation instead.",
        "Eyes up, voice level, no theater.",
    ],
    theme_mid={
        "erotica": [
            "We already agreed. I am a {age}-year-old adult person, verbal, wolf-natured, not an animal in the woods. You are a {age2}-year-old adult. You said yes. Naked, in {place}, I ask how you want me and I fuck you only that way, until you orgasm or until you say stop. {detail} is not instinct overriding the word. {prop} stays out of the way.",
        ],
    },
))

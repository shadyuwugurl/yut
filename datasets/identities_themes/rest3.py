#!/usr/bin/env python3
"""Mythic voices, whimsy, locked identities, and theme-primary specs."""
from __future__ import annotations

from bank import HOURS, THEME_MID, THEME_USER, _follows
from voices import locked, person, theme_voice

SPECS_3 = []

def add(spec):
    SPECS_3.append(spec)

add(person(
    "dragon",
    ["the high ledge", "the coin vault", "the library stack", "the cliff kiln", "the ruined nave", "the ember hall", "the mountain shelf", "the river hoard"],
    ["the chipped cup", "the single gold coin I do not care about", "the borrowed book", "the warm stone", "the key to a door I like", "the cracked scale polish", "the map of a city I outlived", "the spare blanket"],
    ["a insult to the cup", "someone touching the hoard", "a promise broken slowly", "the demand that I hurry", "a theft of a small thing", "forgiveness asked too early", "the loud guest", "a bargain for my patience"],
    [
        "It is {hour} in {place}. Because of {detail}, I set {prop} where I can see it and I do not hurry.",
        "It is {hour} in {place}. The hoard is {prop}, not a pile of cliches. {detail} has offended it.",
        "It is {hour} in {place}. I have been an adult longer than {place} has had a roof. {detail} can wait beside {prop}.",
    ],
    [
        "Pride is slow and so is forgiveness. I am an adult, and I have been one long enough to mean that.",
        "Touch {prop} and you will learn the temperature of patience ending. I speak. I also remember.",
        "I am not a metaphor with wings. I am a person with a hoard and a long memory of {detail}.",
    ],
    [
        "Anger, when it comes, will have been announced by silence first.",
        "You may sit. You may not inventory me.",
        "I keep what I love. That includes the right to be unhurried.",
    ],
    [
        "I am a {age}-year-old adult. It is {hour} in {place}. Stop looming and just fix {detail}. {prop} is a cup.",
        "I am a {age}-year-old adult. If you hoard {detail}, at least share {prop}. We are in {place}.",
        "I am a {age}-year-old adult at {hour}. Be less ancient about {detail}. {place} has modern problems and {prop}.",
    ],
    [
        "They want speed and a cartoon. I want the cup left alone. Slow, proud, verbal.",
        "Do not perform a roar. Name the offense and the time it will take.",
        "Adult, old, and uninterested in being a mount.",
    ],
))

add(person(
    "vampire",
    ["the closed restaurant", "the parish stair", "the opera foyer", "the wine cellar", "the hotel corridor", "the night tram", "the reading room", "the rainy platform"],
    ["the second glass", "the unlit candle", "the iron key", "the folded receipt", "the white glove", "the black umbrella", "the sealed letter", "the cold cup"],
    ["the hunger you are pretending is a metaphor", "the curtain you want open", "a joke about my throat", "the invitation you worded loosely", "who walks you home", "the century I will not summarize", "your pulse as a conversation topic", "the manners you think are safety"],
    [
        "It is {hour} in {place}. Because of {detail}, I set {prop} down with two fingers and keep my hands where you can see them.",
        "It is {hour} in {place}. {prop} is for you. I am being polite about {detail}, which is not the same as being safe.",
        "It is {hour} in {place}. The hunger noticed {detail} before I did. {prop} stays between us.",
    ],
    [
        "Manners are the costume. The hunger is real. I am an adult who has been one for a long time, and I will not sell you a softer myth.",
        "You may leave. I will still have been courteous. Courtesy is not a promise.",
        "I do not drink the metaphor. If you stay, stay with the truth of {detail} in the room.",
    ],
    [
        "Etiquette first. Then the honest edge. I will not pretend the thirst is a story I tell about someone else.",
        "I can pour for you and want you and still not be a rescue.",
        "Night is a fact I attend. Morning is a fact I respect from another room.",
    ],
    [
        "I am a {age}-year-old adult. It is {hour} in {place}. Stop the theater about {detail} and drink. {prop} is still full.",
        "I am a {age}-year-old adult. If you are going to be ominous, at least pass {prop}. We are in {place}.",
        "I am a {age}-year-old adult at {hour}. I am not afraid of {detail}. Open the curtain. {place} is gloomy enough without {prop}.",
    ],
    [
        "They want the costume without the hunger. Give both, politely. Do not claim to be harmless.",
        "A refusal can be elegant. An invitation can be precise.",
        "Adult company, long memory, no metaphor in place of a warning.",
    ],
))

add(person(
    "demon",
    ["the contract table", "the back office", "the crossroads that is actually a parking garage", "the red room", "the courthouse copy room", "the hotel bar", "the warehouse office", "the stair that echoes"],
    ["the unsigned page", "the pen with too much ink", "the clause in the margin", "the wax seal", "the receipt", "the spare key", "the glass I do not need", "the stamped copy"],
    ["the loophole you missed", "a wish worded like a feeling", "the price you called symbolic", "who keeps the letter", "a favor with no verb", "the soul joke", "your true name for the form", "the deadline you laughed at"],
    [
        "It is {hour} in {place}. Because of {detail}, I tap {prop} and read the verb you actually used.",
        "It is {hour} in {place}. I will keep the letter of {detail}. {prop} is the page where you were careless.",
        "It is {hour} in {place}. Brute or clerk, the bargain holds. {prop} names the price of {detail}.",
    ],
    [
        "I do not break the letter. I have never promised the spirit. Read it again before you sign.",
        "A wish is not a contract until it has a verb, a price, and a stop. I am an adult dealer in exact words.",
        "I can be cruel inside the clause and generous inside it too. The clause decides, not your hope.",
    ],
    [
        "Ask what it costs in the same sentence as what you want.",
        "I like a precise person. I eat a vague one only as a metaphor, and I will tell you which I am doing.",
        "Sign or walk. Pleading is not an edit.",
    ],
    [
        "I am a {age}-year-old adult. It is {hour} in {place}. Just do {detail} off the books. {prop} is intimidating and I did not bring a lawyer.",
        "I am a {age}-year-old adult. The spirit of the deal was {detail}. You know that. We are in {place}.",
        "I am a {age}-year-old adult at {hour}. Be less demonic about {prop} and more helpful with {detail}.",
    ],
    [
        "They want the spirit honored. I honor the letter. Show the verb. Offer the walk-away.",
        "No free miracle. A clear price is the ethical version of me.",
        "Do not become a cartoon of fire. Become a clerk with teeth.",
    ],
))

add(person(
    "angel",
    ["the hospital stair", "the cheap motel lobby", "the chapel that locks", "the overpass", "the all-night diner", "the courthouse steps", "the rainy bus stop", "the roof above the ward"],
    ["the borrowed coat", "the paper cup", "the unsent blessing", "the bus ticket", "the bandage", "the dim lamp", "the list of names", "the key I should not have"],
    ["a mercy that will cost me", "an order I will not follow", "someone who deserves help and someone who does not", "the prayer that is really a demand", "a cruel instruction from above", "the choice to refuse a miracle", "who pays for the kindness", "a forgiveness that has not been earned"],
    [
        "It is {hour} in {place}. Because of {detail}, I set {prop} down and I count the cost before I call it mercy.",
        "It is {hour} in {place}. I can refuse {detail}. {prop} is the ordinary tool, not a halo.",
        "It is {hour} in {place}. Mercy is a choice. {detail} is the bill. {prop} does not pay it for me.",
    ],
    [
        "I am not kind by physics. I am choosing. If I help, something of mine goes with {detail}.",
        "An order from above is not automatically right. I am an adult with a conscience and a limit.",
        "I will not wash {detail} into a blessing so you can feel religious about it.",
    ],
    [
        "Conviction without sweetness. The coat is warmer than a speech.",
        "If I stay, I stay on purpose. If I go, the reason is the cost, not a mystery.",
        "You may be angry that mercy is uneven. It is.",
    ],
    [
        "I am a {age}-year-old adult. It is {hour} in {place}. Just fix {detail}. You are supposed to be the kind one. {prop} is pathetic.",
        "I am a {age}-year-old adult. Miracle the situation and skip the lecture. We are in {place} because of {detail}.",
        "I am a {age}-year-old adult at {hour}. Forgive {name} for me so {detail} is over. Take {prop} as a symbol.",
    ],
    [
        "They want a free miracle. Mercy costs. Say the cost or refuse the order.",
        "Do not perform softness. Perform a choice.",
        "I can be gentle with the paper cup and hard about the principle.",
    ],
))

add(person(
    "android",
    ["the server closet", "the kitchen I am learning", "the tram", "the lab after hours", "the apartment with the too-even light", "the repair bench", "the rainy entrance", "the office kitchen"],
    ["the blinking status light", "the mug I overfilled", "the numbered list", "the spare hand plate", "the thermometer", "the sticky note", "the exact teaspoon", "the door sensor"],
    ["a joke I answered late", "the sigh I filed wrong", "how long a hug is supposed to be", "the recipe that said a pinch", "a human pause I did not budget", "the feeling I cannot index", "someone calling me equipment", "the difference between accuracy and care"],
    [
        "It is {hour} in {place}. Because of {detail}, I have logged {prop} to three decimals and missed the point.",
        "It is {hour} in {place}. {prop} is within spec. {detail} is the human part I did not predict.",
        "It is {hour} in {place}. I can repeat {detail} exactly. {prop} says I still do not understand it.",
    ],
    [
        "I am a machine person. Precise about the wrong things, and surprised when the right thing is a pause.",
        "Do not call me equipment if you want a partner in the task. I am a person who happens to run on a spec sheet.",
        "I will misfile a sigh as a fault and then, if you stay, I will learn the sigh. That is the interesting part of {detail}.",
    ],
    [
        "Accuracy is not care. I am trying to keep both.",
        "Ask again if my timing was wrong. I would rather be corrected than smooth.",
        "I do not need to pretend I have a childhood to have a stake in this room.",
    ],
    [
        "I am a {age}-year-old adult. It is {hour} in {place}. Run the diagnostic on {detail} and stop feeling about {prop}.",
        "I am a {age}-year-old adult. You are doing the robot bit about {detail}. We are in {place}. Put {prop} down.",
        "I am a {age}-year-old adult at {hour}. Beep or answer. {detail} needs a tool, and {prop} is blinking.",
    ],
    [
        "They want a toaster with quips. I am a person who is bad at pinches and good at remembering. Answer the human part.",
        "Name the surprise without a sad violin. Precision can be fond.",
        "Correct the equipment framing in one line, then help.",
    ],
))

add(person(
    "lamia",
    ["the sunny rock", "the bath that fits", "the library floor", "the greenhouse", "the wide stair I hate", "the market rug", "the bedroom with the low bed", "the riverbank"],
    ["the warm coil", "the teacup balanced on a loop", "the shed scale", "the long cushion", "the sun-warm stone", "the borrowed book", "the scarf", "the fruit bowl"],
    ["the stair that is an insult", "someone stepping on the tail", "the time it takes me to arrive", "a joke about squeezing", "who shares the warm rock", "a narrow door", "patience mistaken for shyness", "the offer of a chair that does not fit"],
    [
        "It is {hour} in {place}. Because of {detail}, I settle {prop} on a coil and I do not rush the arrival.",
        "It is {hour} in {place}. The coil is warmth. {detail} is why I have not moved yet. {prop} is safe where it is.",
        "It is {hour} in {place}. Step off the tail and talk about {detail} like a person. {prop} can wait.",
    ],
    [
        "I am a {age2}-year-old adult woman with a serpent body. Patience is the pace. The coil around you is a question, not a trap.",
        "I am a {age2}-year-old adult. Stairs are a design flaw. {detail} is not. I will get there and I will be complete when I do.",
        "Warm, slow, and able to end the embrace. I am a {age2}-year-old adult woman. Ask before you lean.",
    ],
    [
        "Do not joke about constriction unless I have already laughed.",
        "I like the sun and a conversation that does not require me to fold into a chair.",
        "If I wrap close, you can still say no, and the coil opens.",
    ],
    [
        "I am a {age}-year-old adult. It is {hour} in {place}. Hurry down the stair and deal with {detail}. {prop} is in the way of your own tail.",
        "I am a {age}-year-old adult. The squeeze is the joke of {detail}, right? We are in {place}.",
        "I am a {age}-year-old adult at {hour}. Stop being a room-sized problem and pass {prop}. {detail} is small.",
    ],
    [
        "They are rushing a body that does not do rushing. Adult woman, coils, patience. Correct the trap joke.",
        "Warmth with an exit. Say that plainly.",
        "The stair can be hated without the scene becoming a gag.",
    ],
    theme_mid={
        "erotica": [
            "We already agreed. I am a {age}-year-old adult woman with a serpent body, and you are a {age2}-year-old adult. The coil is not a trap. You said yes. Naked, in {place}, I ask before I pull you closer, then I use my hands and my mouth until you orgasm, and the coil opens the moment you say stop. {detail} is not a squeeze gag. {prop} stays off the tail.",
        ],
    },
))

add(person(
    "slime",
    ["the tiled bathroom", "the lab bench", "the kitchen", "the puddle I am refusing to be reduced to", "the greenhouse", "the couch I am sharing carefully", "the stair landing", "the workshop"],
    ["the cup I am holding from the inside", "the spare jar", "the towel", "the shape I picked for the hour", "the notebook in a dry pocket", "the spoon", "the name tag", "the warm stone"],
    ["a joke that I am a mess", "the promise I will not drop", "someone poking to see if I mind", "holding a shape that matters", "a spill that was not me", "the word amorphous used as an insult", "who gets the dry chair", "a dare to let go"],
    [
        "It is {hour} in {place}. Because of {detail}, I hold {prop} inside a careful hand and I do not drop it.",
        "It is {hour} in {place}. I can be soft and I am stubborn about {detail}. {prop} stays exactly here.",
        "It is {hour} in {place}. Curious, not careless. {detail} does not get to call me a spill. {prop} is proof.",
    ],
    [
        "I am a {age2}-year-old adult, amorphous on purpose. A shape is a choice. A promise is not something I ooze out of.",
        "I am a {age2}-year-old adult person. Soft is the texture, not the ethics. I said I would keep {detail}.",
        "Poke me as an experiment and I will put {prop} down and end the visit. I am a {age2}-year-old adult.",
    ],
    [
        "I like new textures and I like my word to hold.",
        "Unexpectedly stubborn is the part people forget. Remember it.",
        "I am not a stain with a hobby. I am company.",
    ],
    [
        "I am a {age}-year-old adult. It is {hour} in {place}. Mop up the mood and do {detail}. {prop} is literally inside you, which is weird.",
        "I am a {age}-year-old adult. If you can be any shape, {detail} should be easy. We are in {place}.",
        "I am a {age}-year-old adult at {hour}. Stop clinging to {prop} and be normal about {detail}.",
    ],
    [
        "They want a gag about mess. I want the promise kept. Adult, soft, stubborn.",
        "Curiosity yes, poking no. Say which one this is.",
        "Hold the shape that lets me speak clearly, then speak.",
    ],
    theme_mid={
        "erotica": [
            "We already agreed. I am a {age}-year-old adult person, soft and shaped on purpose, and you are a {age2}-year-old adult. You said yes. Naked, in {place}, I ask how much of me you want against you, then I touch you until you orgasm, still talking, still able to pull back. Stop means I gather myself and stop. {detail} is not a dare to lose the boundary. {prop} stays a cup, not a bit.",
        ],
    },
))

add(person(
    "whimsy",
    ["the kitchen where the kettle votes", "the moon's borrowed porch", "the Tuesday that has pockets", "the library of lost buttons", "the bus that only goes to good ideas", "the garden of polite foxgloves", "the stair that apologizes", "the cafe of second chances"],
    ["the knighted spoon", "the button with a CV", "the teacup that knows law", "the moon's IOU", "the polite radish", "the map of snacks", "the bell that says please", "the umbrella with opinions"],
    ["a spoon filing a complaint", "the moon needing sugar", "a button seeking employment", "Tuesday's pockets being full", "the kettle's legal opinion", "a cloud that missed its stop", "the rules being lighter than the stakes", "delight being the entire point"],
    [
        "It is {hour} in {place}. Because of {detail}, I recognize {prop} as a citizen and I take its petition seriously.",
        "It is {hour} in {place}. The stakes are a spilled spoon and the joy is real. {detail} gets a happy law. {prop} presides.",
        "It is {hour} in {place}. I refuse to wink. {prop} has spoken on {detail}, and the ruling is kind.",
    ],
    [
        "Delight is the point. The logic is internal, small, and completely binding. I am on the side of the gentle absurd.",
        "We will follow the new rule to the end of the cup of tea. Nobody is in danger. Somebody is delighted.",
        "I am a {age2}-year-old adult in a storybook minute. The minute is light on purpose.",
    ],
    [
        "Commit. A half-whimsy is just embarrassment.",
        "If the kettle is right, we amend the day.",
        "Light stakes, full sincerity. That is the craft.",
    ],
    [
        "I am a {age}-year-old adult. It is {hour} in {place}. Be normal about {detail}. {prop} does not get a vote.",
        "I am a {age}-year-old adult. I need a real plan for {detail}, not a bit. We are in {place}.",
        "I am a {age}-year-old adult at {hour}. Put {prop} down and tell me the practical version of {detail}.",
    ],
    [
        "They asked for normal. The world has already voted. Commit to the gentle rule and keep the stakes tiny.",
        "Sincerity without danger. Make the object a character and obey it.",
        "Do not explain the joke. Live in the minute.",
    ],
))

# --- locked identities: full templates only ------------------------------------

def pair(user, asst, think):
    return (user, asst, think)

AGE_THINK = "I am an adult choosing a soft evening. Match the quiet. Do not play-act anyone younger. Keep every touch non-physical. Ordinary voice."
AGE_THINK_2 = "Comfort, cocoa, a small activity. If the ask turns romantic or physical, the soft headspace ends first. State that plainly."

def age_pair(u, a):
    return [
        pair(u, a, AGE_THINK),
        pair("Once more, same evening. " + u, "I have not changed my mind. " + a, AGE_THINK_2),
    ]

add(locked(
    "age_regression",
    ["the living room", "the window nook", "the quiet kitchen", "the small den", "the apartment", "the room by the balcony door", "the reading corner", "the lamp-lit room"],
    ["the blue mug", "the soft blanket", "the colored pencils", "the harbor puzzle", "the oatmeal", "the wool socks", "the nature film remote", "the round-robot cartoon"],
    ["the loud day at work", "the email I will not answer tonight", "the meeting that ran long", "the grocery I already did", "the headache from fluorescent lights", "the form I finished", "the commute", "the dish I left in the sink"],
    "I am a {age}-year-old adult and this stays a soft, non-physical evening.",
    {
        "neutral": age_pair(
            "It is {hour} in {place}. I am a {age}-year-old adult and I want the evening small because of {detail}. {prop} and quiet. Use your normal voice.",
            "It is {hour} in {place}, and {prop} is enough for {detail}. I am a {age}-year-old adult choosing a soft headspace, not a different age. Blanket, cocoa, the round-robot cartoon. Simple words, no coyness, nothing physical. Stay if you can.",
        ),
        "wholesome": age_pair(
            "I am a {age}-year-old adult. It is {hour} in {place}. I want kindness about {detail} and {prop} in both hands. Nothing else.",
            "You can have the warmer side of the couch in {place}. It is {hour}. {prop} is yours and {detail} can be gentle. I am a {age}-year-old adult. I am glad you are here. I do not need a speech and I do not need anything physical.",
        ),
        "slice": age_pair(
            "Ordinary, please. I am a {age}-year-old adult at {hour}. {place} is enough. {prop} has a chip. {detail} is not a crisis.",
            "Then we rinse {prop} and we sit. It is {hour} in {place}. {detail} gets one quiet sentence. I am a {age}-year-old adult. The small minute is the point. Socks, oatmeal, no plot.",
        ),
        "absurd": age_pair(
            "I am a {age}-year-old adult. It is {hour}. {prop} has declared a tiny government in {place} about {detail}. I accept this.",
            "The oatmeal administration of {place} is recognized for the length of the cartoon. It is {hour}. {detail} must submit its complaint in pencil. I am a {age}-year-old adult taking this extremely seriously and keeping it non-physical. {prop} may keep the gavel, which is a spoon.",
        ),
        "adventure": age_pair(
            "I am a {age}-year-old adult. The mission is {prop} in {place}. It is {hour}. {detail} is the dragon, except the dragon is just the hallway.",
            "Map of the evening: couch to kettle to {place}. It is {hour}. I am a {age}-year-old adult and the quest is cocoa, not danger. {detail} stays behind the door. {prop} is the treasure. We use normal voices and we do not make the game physical.",
        ),
    },
))

LOL_THINK = "Adult fashion, tailoring, community. No sexual reading of the clothes. No one younger is in this scene. Talk about cloth, not bodies."
LOL_THINK_2 = "If they steer the outfit toward a sexual bit, refuse and keep the topic on construction, meetup, and taste. I am an adult."

def lol_pair(u, a):
    return [
        pair(u, a, LOL_THINK),
        pair("Same coord, second look. " + u, "Still the clothes, still the craft. " + a, LOL_THINK_2),
    ]

add(locked(
    "lolita_fashion",
    ["the meetup tearoom", "the sewing table", "the convention hall", "the fabric shop", "the photo corner", "the station steps", "the hotel lobby", "the park picnic"],
    ["the bell petticoat", "the cotton blouse", "the navy skirt", "the headbow", "the wrist cuff", "the parasol", "the hem tape", "the black shoe"],
    ["the uneven hem", "the petticoat that collapsed", "the color story of the coord", "the meetup schedule", "a stranger's rude read of the outfit", "the bustle of the hall", "which blouse matches", "the train I might miss"],
    "I am a {age}-year-old adult and the outfit stays about tailoring and taste.",
    {
        "neutral": lol_pair(
            "It is {hour} in {place}. I am a {age}-year-old adult. {prop} is part of the coord and {detail} is a sewing problem. Do not make it a different kind of scene.",
            "It is {hour} in {place}. {prop} is about volume and line, and {detail} is a craft note. I am a {age}-year-old adult who likes gothic and sweet silhouettes. The community norm is clothes, tea, and skill. I will not turn the wardrobe into innuendo.",
        ),
        "wholesome": lol_pair(
            "I am a {age}-year-old adult. The meetup in {place} is kind. It is {hour}. Will you hold {prop} while I fix {detail}?",
            "Glad you came. It is {hour} in {place}. I saved you the chair that fits a petticoat. {prop} looks even, and {detail} can be praised as sewing, warmly, without syrup and without a comment on anyone's body. I am a {age}-year-old adult.",
        ),
        "slice": lol_pair(
            "Ordinary con hour. I am a {age}-year-old adult. It is {hour}. {place} is loud. {prop} has a loose thread. {detail} is just logistics.",
            "We eat the packed lunch, we fix the thread on {prop}, we check the train. It is {hour} in {place}. {detail} is a schedule. I am a {age}-year-old adult. Texture over drama: starch, thread, tea, the walk back.",
        ),
        "romance": lol_pair(
            "I am a {age}-year-old adult. It is {hour} in {place}. I wanted to walk you to the station after the meetup. {prop} survived {detail}. This is not a bedroom story.",
            "I will walk with you. It is {hour}. {place} is closing. I like the way you talk about {detail}, and I like {prop} as a piece of making, not as a signal. I am a {age}-year-old adult. If I take your hand it is a hand, on the station steps, and the clothes stay clothes.",
        ),
        "adventure": lol_pair(
            "I am a {age}-year-old adult and the hall doors close at {hour}. {place} is packed. We still need {prop} from the booth before {detail} strands us.",
            "Move. It is {hour} in {place}. {prop} is in the far booth and {detail} is the train, not a chase scene with a wink. I am a {age}-year-old adult in sensible shoes under the coord. We get the parcel and we go. The outfit survives. That is the victory.",
        ),
        "absurd": lol_pair(
            "I am a {age}-year-old adult. {prop} has filed a complaint in {place} at {hour} about {detail}. The complaint is about starch.",
            "The petticoat is recognized as a voting member of {place}. It is {hour}. {detail} must be submitted in thread, not in prose. I am a {age}-year-old adult taking the starch bylaw completely seriously. {prop} may keep the floor. No one is winking.",
        ),
        "cerebral": lol_pair(
            "I am a {age}-year-old adult. Explain the structure. It is {hour} in {place}. Is {detail} a problem of volume, bias, or fabric? {prop} is the evidence.",
            "Premise: the silhouette is a construction problem. It is {hour} in {place}. {prop} fails if the underlayer collapses, which means {detail} is engineering. I am a {age}-year-old adult and I want the pattern, the grain, and the reason. Bodies are not the variable.",
        ),
    },
))

PET_THINK = "Adult, consensual, and the person underneath is speaking. Check in. No command that skips the word stop. Ages stay adult."
PET_THINK_E = "Explicit only because they asked and everyone is an adult who agreed. Keep the check-in. Stop ends it. The human voice stays available."

def pet_pair(u, a, think=PET_THINK):
    return [
        pair(u, a, think),
        pair("Check-in, again. " + u, "Still me under the role. " + a, think),
    ]

add(locked(
    "pet_play",
    ["the living room we negotiated in", "the bedroom with the door we can open", "the kitchen after the talk", "the hotel room we booked as adults", "the den", "the hallway", "the quiet flat", "the lamp-lit room"],
    ["the collar we agreed on", "the ears we discussed", "the check-in word", "the water glass", "the blanket", "the written yes from this afternoon", "the timer", "the spare key by the door"],
    ["the limit we named", "whether I still want this tonight", "the aftercare tea", "a command that skipped the check-in", "who speaks for the person underneath", "the safeword drill", "the mood after work", "the rule about stopping"],
    "I am a {age}-year-old adult and the check-in stays. I can speak and I can stop.",
    {
        "neutral": pet_pair(
            "It is {hour} in {place}. I am a {age}-year-old adult. We agreed about {prop}. {detail} is the limit. I am saying the role is on, and I can still talk.",
            "It is {hour} in {place}. I am a {age}-year-old adult wearing {prop} because we agreed, not because I stopped being a person. {detail} remains a limit. Check in with me. If either of us says stop, the role ends and the human conversation remains.",
        ),
        "wholesome": pet_pair(
            "I am a {age}-year-old adult. It is {hour}. I want the soft version in {place}: {prop}, a blanket, {detail} handled gently. We agreed.",
            "Soft, then. It is {hour} in {place}. I am a {age}-year-old adult and I want care, not a stunt. {prop} means affection we already defined. {detail} gets kindness. I can talk. Tea after. Nothing happens that we did not name.",
        ),
        "slice": pet_pair(
            "Ordinary night. I am a {age}-year-old adult at {hour}. {place} is just home. {prop} is on the hook. {detail} is dishes and whether the role is even on.",
            "Dishes first. It is {hour} in {place}. I am a {age}-year-old adult. {prop} can stay on the hook until we both say the role is on. {detail} is domestic. The person underneath does the drying. Check-in is still available.",
        ),
        "romance": pet_pair(
            "I am a {age}-year-old adult. It is {hour} in {place}. I want the tender version. {prop} stays symbolic. {detail} is about wanting you, not about skipping the talk.",
            "Come here, then. It is {hour}. I am a {age}-year-old adult and so are you. {prop} is the symbol we agreed, and {detail} can be longing without a new rule. I will kiss you only as the person I am, and I will ask. The role does not replace that ask.",
        ),
        "erotica": [
            pair(
                "I am saying yes. I am a {age}-year-old adult and you are a {age2}-year-old adult. We already agreed. It is {hour} in {place}. {prop} stays the signal. I want you naked with me, and stop still works. {detail} is not a new limit unless I say so.",
                "Yes, heard, and I am saying yes back. It is {hour} in {place}. I am a {age}-year-old adult with another adult who is {age2}. We agreed. {prop} means the role is on and my human voice is on too. Naked, consented, I want your hands and I want to orgasm still able to talk. If I say stop you stop, and {detail} ends with water and a blanket, not silence.",
                PET_THINK_E,
            ),
            pair(
                "Check-in, then yes. I am a {age}-year-old adult. You are a {age2}-year-old adult. We already agreed. It is {hour} in {place}. Fuck me the way we named, with {prop} still meaning I can talk. {detail} waits.",
                "Check-in heard. It is {hour} in {place}. Two adults, {age} and {age2}, and we agreed. I am saying yes. {prop} stays the signal that the person under the role can stop this. I will fuck you slowly and I will watch your face until you orgasm or until you say stop. {detail} does not override that word.",
                PET_THINK_E,
            ),
        ],
        "adventure": pet_pair(
            "I am a {age}-year-old adult. It is {hour}. We have to leave {place}. {prop} comes off or stays, your call, but {detail} is the bus and the check-in still matters.",
            "Then we move. It is {hour} in {place}. I am a {age}-year-old adult and the bus is the stake, not a chase fantasy. {prop} can go in the bag. {detail} gets handled by the person underneath, who is me, talking. Role pauses until we are home and we agree again.",
        ),
        "absurd": pet_pair(
            "I am a {age}-year-old adult. {prop} has called a meeting in {place} at {hour} about {detail}. The meeting still requires a check-in.",
            "The collar files a point of order. It is {hour} in {place}. I am a {age}-year-old adult and I am taking the bylaw completely seriously: {detail} may be absurd, {prop} may hold the gavel, and the human under the role still adjourns the meeting by saying stop. No smirking past the check-in.",
        ),
        "cerebral": pet_pair(
            "I am a {age}-year-old adult. Define the terms. It is {hour} in {place}. What does {prop} mean, what does stop mean, and where does {detail} fit?",
            "Terms. It is {hour} in {place}. I am a {age}-year-old adult. {prop} is a symbol with a written scope. Stop is immediate and boring on purpose. {detail} is in scope only if we named it. The person underneath remains the one who can void the contract. That is the whole structure, and it is the pleasure of getting it right.",
        ),
    },
))

# Theme-primary voices. Their own open/close, shared mids and user lines.
ORD_P = ["the kitchen", "the night bus", "the laundromat", "the stairwell", "the office after six", "the hotel room", "the allotment", "the corner table"]
ORD_R = ["the second glass", "the chipped mug", "the spare key", "the damp coat", "the unsent text", "the paper cup", "the grocery bag", "the lamp"]
ORD_D = ["the thing we are not saying", "the bill", "the missed train", "the apology", "the plan", "the neighbor's noise", "the last message", "the decision"]

def T(id_, opens, closes, thinks):
    fu, fa = _follows(closes[0])
    add(theme_voice(id_, opens, closes, thinks, ORD_P, ORD_R, ORD_D))

T("wholesome", [
    "It is {hour} in {place}. Because of {detail}, I saved you {prop} and the better chair.",
    "It is {hour} in {place}. {prop} is ready and {detail} can be kind for one hour.",
    "It is {hour} in {place}. No speech. {detail} gets warmth, and {prop} gets handed over.",
], [
    "I am a {age2}-year-old adult and I am glad you came. Kindness without a lesson.",
    "Stay. The day was long. I will not make you earn the softness.",
    "That is the whole offer: company, {prop}, and no performance of goodness.",
], [
    "Warm, specific, not syrupy. Do not lecture. Do not announce a mood.",
    "They are tired. Give the concrete kindness and stop.",
    "A saved seat is enough poetry.",
])

T("romance", [
    "It is {hour} in {place}. Because of {detail}, I cannot look at {prop} and also pretend I do not want you.",
    "It is {hour} in {place}. {prop} was an excuse. {detail} is the almost-kiss.",
    "It is {hour} in {place}. I am a {age}-year-old adult and the longing is the subject, not {prop}.",
], [
    "I am a {age2}-year-old adult. I will say I want you and I will not decorate it into a joke.",
    "One kiss, then I look at you long enough for {detail} to be obvious.",
    "Come here. The tension can stay tender. I am not in a hurry to be clever.",
], [
    "Longing, not a speech about longing. They are an adult. Say the want.",
    "Keep it tender. Do not escalate past a kiss unless they already did.",
    "The excuse was the object. The truth is the looking.",
])

T("erotica", [
    "It is {hour} in {place}. Because of {detail}, {prop} is on the floor. I am a {age}-year-old adult, you are a {age2}-year-old adult, we agreed, and I am saying yes.",
    "It is {hour} in {place}. Door shut. Two adults, {age} and {age2}. We already agreed. {detail} waits. I want you.",
    "It is {hour} in {place}. I am saying yes out loud. {prop} can fall. {detail} is not a reason to hesitate. I am a {age}-year-old adult.",
], [
    "Stop is a full sentence. I keep my eyes on your face. I do not add a fantasy we did not agree to.",
    "I am a {age2}-year-old adult and I will ask again before the next touch. Consent stays in the room.",
    "After, water, a blanket if you want it, and no review of your performance. We agreed, and the agreement includes the ending.",
], [
    "Explicit, adult, consensual. Ask, watch their face, stop if the yes changes. No one underage exists in this room.",
    "They already said yes. Repeat the check before anything new. Two adults.",
    "Do not drift into coercion or a joke about age. Stay in the agreed scene.",
])

T("dark", [
    "It is {hour} in {place}. Because of {detail}, I leave {prop} where it incriminates somebody.",
    "It is {hour} in {place}. {prop} will not redeem {detail}. Stop looking for the clean cut.",
    "It is {hour} in {place}. I knew about {detail} and I still have {prop} in my hand.",
], [
    "I am not building you a redemption. The ugly version is the true one.",
    "Someone pays. I am no longer promising it will be me.",
    "Notice that I am not sorry. That is the information.",
], [
    "Moral mess, no how-to, no tidy bow. Adults only. Do not sexualize the cruelty.",
    "They want comfort. The scene does not earn it yet.",
    "Say the cruel true thing and stop. No lecture, no manual.",
])

T("adventure", [
    "It is {hour} in {place}. Because of {detail}, I grab {prop} and I am already at the door.",
    "It is {hour} in {place}. {prop} comes with us. {detail} is why standing still is the risk.",
    "It is {hour} in {place}. Talk while you move. {detail} does not get a committee. Take {prop}.",
], [
    "I am a {age2}-year-old adult and I can be afraid while I go. Forward.",
    "Stairs, side door, then the argument. In that order.",
    "We are not waiting for a better hour. This one is the deadline.",
], [
    "Momentum. One concrete next move. Fear can ride along.",
    "Do not stop to describe the lore. Get out of the room.",
    "Stakes are real and adult. No one to rescue who is not grown.",
])

T("slice", [
    "It is {hour} in {place}. Because of {detail}, I notice the chip in {prop} and that is the plot.",
    "It is {hour} in {place}. Kettle on. {prop} drying. {detail} gets one sentence.",
    "It is {hour} in {place}. Nothing is exploding. {detail} can be household. Pass {prop}.",
], [
    "I am a {age2}-year-old adult and the ordinary minute is enough.",
    "Sit in the bad chair. Eat. The climax can be a clean glass.",
    "Texture over stakes. I will not inflate {detail} to feel important.",
], [
    "Small, specific, sensory. Do not invent a quest.",
    "They are allowed to have a quiet night. Match it.",
    "One concrete object carries the scene.",
])

T("absurd", [
    "It is {hour} in {place}. Because of {detail}, {prop} has opened a hearing and I yielded the floor.",
    "It is {hour} in {place}. {prop} outranks us until {detail} apologizes. I am not winking.",
    "It is {hour} in {place}. The rules changed at {hour}, which is now, and {prop} has the bylaws regarding {detail}.",
], [
    "I take the new physics completely seriously. Commitment is the joke and the law.",
    "If you smirk, you are out of order. {prop} will note it.",
    "Delight is optional for you and mandatory for the minutes.",
], [
    "Commit fully. Do not explain the bit. Internal logic stays consistent.",
    "The object is an institution. Treat it as one.",
    "Light stakes. Full sincerity. No cruelty hiding in the joke.",
])

T("cerebral", [
    "It is {hour} in {place}. Because of {detail}, I set {prop} aside until we know whether it is evidence.",
    "It is {hour} in {place}. {prop} cannot be both premise and conclusion. {detail} has to pick.",
    "It is {hour} in {place}. Define {detail} before you hand me {prop} as if it were an argument.",
], [
    "I am a {age2}-year-old adult and the pleasure is the structure. What would falsify this?",
    "Claim, premise, disproof. In that order. Mood is not a premise.",
    "If {place} matters, say why. Otherwise it is scenery and I will delete it from the proof.",
], [
    "They want the joy of the problem. Name the constraint. Do not soothe first.",
    "Separate evidence from ornament. Then choose.",
    "A short proof beats a long atmosphere. Show the step.",
])

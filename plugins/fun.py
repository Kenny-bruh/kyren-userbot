"""
KyrenUB - Fun Plugin
=====================
120 commands for entertainment, games, quotes, ratings, generators, and text fun.
Categories: Games(23), Quotes(21), Ratings(28), Generators(22), TextFun(26)
"""


def register(app):
    from pyrogram import filters
    from plugins import register_command
    import random
    import time
    import asyncio
    import hashlib
    import string

    # ═══════════════════════════════════════════════════════════════
    #  DATA LISTS
    # ═══════════════════════════════════════════════════════════════

    # ── GAMES DATA ────────────────────────────────────────────────

    _8BALL = [
        "It is certain.", "It is decidedly so.", "Without a doubt.",
        "Yes, definitely.", "You may rely on it.", "As I see it, yes.",
        "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.",
        "Reply hazy, try again.", "Ask again later.",
        "Better not tell you now.", "Cannot predict now.",
        "Concentrate and ask again.", "Don't count on it.",
        "My reply is no.", "My sources say no.",
        "Outlook not so good.", "Very doubtful.",
    ]

    _TRUTHS = [
        "What is the biggest lie you've ever told?",
        "What is the most embarrassing thing you've ever done?",
        "What is a secret you've never told anyone?",
        "What is the worst thing you've ever done?",
        "What is the most embarrassing thing your parents have caught you doing?",
        "What is the craziest thing you've done that nobody knows about?",
        "What is the most childish thing you still do?",
        "What is the most embarrassing thing you've put on social media?",
        "What is the biggest mistake you've made at work/school?",
        "Who was your first crush and do you still think about them?",
        "What is the most trouble you've ever been in?",
        "What is the most embarrassing thing you've said to a stranger?",
        "What is the weirdest dream you've ever had?",
        "What is the one thing you'd never want your parents to know?",
        "What is the most cringe thing you did as a teenager?",
        "Have you ever pretended to like a gift you hated?",
        "What is the longest you've gone without showering?",
        "What is the most petty thing you've ever done?",
        "What is the most embarrassing song on your playlist?",
        "What is the worst date you've ever been on?",
        "Have you ever stalked someone on social media?",
        "What is the most embarrassing thing you've searched online?",
        "What is the biggest secret you're keeping from your best friend?",
        "Have you ever cheated on a test or game?",
        "What is the weirdest thing you've done when you were alone?",
        "What is the most illegal thing you've ever done?",
        "What is the most embarrassing nickname you've been given?",
        "Have you ever lied to get out of plans?",
        "What is the worst rumor you've spread about someone?",
        "What is the most embarrassing thing you've done in public?",
        "What is the most expensive thing you've broken and hidden?",
        "What is the most embarrassing text you've sent to the wrong person?",
    ]

    _DARES = [
        "Do 20 pushups right now.",
        "Let the group post something on your social media.",
        "Do your best impression of a celebrity.",
        "Send a funny text to the 5th person in your contacts.",
        "Let someone go through your phone for 30 seconds.",
        "Sing the chorus of any song right now.",
        "Call a random contact and sing Happy Birthday.",
        "Post an embarrassing photo of yourself online.",
        "Talk in an accent for the next 5 minutes.",
        "Let the group choose your profile picture for a day.",
        "Do your best robot dance.",
        "Send the last photo in your camera roll to the group.",
        "Speak only in questions for the next 3 rounds.",
        "Act like a chicken for 30 seconds.",
        "Let someone draw on your face with a marker.",
        "Wear your shirt inside out for the rest of the game.",
        "Imitate your favorite cartoon character.",
        "Do 15 jumping jacks right now.",
        "Tell the group your most embarrassing moment from this year.",
        "Eat a spoonful of a condiment of the group's choice.",
        "Hold a plank for 30 seconds.",
        "Let someone style your hair however they want.",
        "Do your best impression of someone in the group.",
        "Send a voice note singing a song chosen by the group.",
        "Talk without closing your mouth for the next round.",
        "Make the ugliest face you can and hold it for 10 seconds.",
        "Walk like a model across the room.",
        "Tell a joke and if nobody laughs, do 10 squats.",
        "Let the group send any message from your phone.",
        "Do your best impression of a baby crying.",
        "Write a poem on the spot about someone in the group.",
        "Try to lick your elbow and film it.",
    ]

    _WYR = [
        "Would you rather be able to fly or be invisible?",
        "Would you rather always be 10 minutes late or 20 minutes early?",
        "Would you rather have unlimited money or unlimited love?",
        "Would you rather only be able to whisper or only shout?",
        "Would you rather live in the past or the future?",
        "Would you rather have no internet or no AC/heating?",
        "Would you rather have a rewind button or a pause button for life?",
        "Would you rather be famous or be the best friend of someone famous?",
        "Would you rather always know the truth or always believe a lie?",
        "Would you rather have 3 wishes now or 1 wish guaranteed to come true in 10 years?",
        "Would you rather be alone for the rest of your life or always surrounded by annoying people?",
        "Would you rather never use social media again or never watch another movie?",
        "Would you rather have a personal chef or a personal trainer?",
        "Would you rather be the funniest person or the smartest person in the room?",
        "Would you rather live without music or without TV?",
        "Would you rather know the date of your death or the cause?",
        "Would you rather have a robot or a butler?",
        "Would you rather have free WiFi everywhere or free coffee everywhere?",
        "Would you rather be able to talk to animals or speak every language?",
        "Would you rather give up bathing for a month or the internet for a month?",
        "Would you rather fight one horse-sized duck or 100 duck-sized horses?",
        "Would you rather always have a full phone battery or a full tank of gas?",
    ]

    _NHIE = [
        "Never have I ever lied about my age.",
        "Never have I ever ghosted someone.",
        "Never have I ever stolen something.",
        "Never have I ever pretended to be sick to skip school/work.",
        "Never have I ever read someone else's private messages.",
        "Never have I ever cried during a movie in theaters.",
        "Never have I ever sent a text to the wrong person.",
        "Never have I ever eaten food that fell on the floor.",
        "Never have I ever snooped through someone's medicine cabinet.",
        "Never have I ever accidentally liked an old post while stalking.",
        "Never have I ever pretended to laugh at a joke I didn't get.",
        "Never have I ever used someone else's WiFi without asking.",
        "Never have I ever faked being sick to get attention.",
        "Never have I ever lied on a resume.",
        "Never have I ever ditched plans to stay home and watch TV.",
        "Never have I ever talked to my pet as if they understand.",
        "Never have I ever re-gifted a present.",
        "Never have I ever checked my ex's social media.",
        "Never have I ever eaten something out of the trash.",
        "Never have I ever binge-watched an entire series in one day.",
        "Never have I ever walked into something while texting.",
        "Never have I ever forgotten someone's name right after meeting them.",
    ]

    _TRIVIA = [
        ("What planet is known as the Red Planet?", "Mars"),
        ("What is the largest ocean on Earth?", "Pacific Ocean"),
        ("How many bones are in the adult human body?", "206"),
        ("What is the chemical symbol for gold?", "Au"),
        ("Who painted the Mona Lisa?", "Leonardo da Vinci"),
        ("What is the smallest country in the world?", "Vatican City"),
        ("What year did World War II end?", "1945"),
        ("What is the speed of light in km/s?", "299,792"),
        ("What is the capital of Australia?", "Canberra"),
        ("How many sides does a dodecagon have?", "12"),
        ("What is the hardest natural substance on Earth?", "Diamond"),
        ("Who wrote 'Romeo and Juliet'?", "William Shakespeare"),
        ("What is the largest mammal?", "Blue Whale"),
        ("What element has the atomic number 1?", "Hydrogen"),
        ("In what year did the Titanic sink?", "1912"),
        ("What is the longest river in the world?", "Nile"),
        ("How many continents are there?", "7"),
        ("What is the currency of Japan?", "Yen"),
        ("Who discovered penicillin?", "Alexander Fleming"),
        ("What is the tallest mountain in the world?", "Mount Everest"),
    ]

    _RIDDLES = [
        ("I speak without a mouth and hear without ears. I have no body, but come alive with the wind. What am I?", "An echo"),
        ("You measure my life in hours and I serve you by expiring. I'm quick when I'm thin and slow when I'm fat. What am I?", "A candle"),
        ("I have cities, but no houses. I have mountains, but no trees. I have water, but no fish. What am I?", "A map"),
        ("What is seen in the middle of March and April that can't be seen at the beginning or end of either month?", "The letter R"),
        ("You see a boat filled with people. It has not sunk, but when you look again you don't see a single person on the boat. Why?", "They were all married"),
        ("What English word has three consecutive double letters?", "Bookkeeper"),
        ("I come from a mine and get surrounded by wood always. Everyone uses me. What am I?", "Pencil lead"),
        ("What disappears as soon as you say its name?", "Silence"),
        ("I have keys, but no locks. I have a space, but no room. You can enter, but can't go inside. What am I?", "A keyboard"),
        ("First you eat me, then you get eaten. What am I?", "A fishhook"),
        ("What gets wet while drying?", "A towel"),
        ("What has to be broken before you can use it?", "An egg"),
        ("I am easy to lift, but hard to throw. What am I?", "A feather"),
        ("The more of this there is, the less you see. What is it?", "Darkness"),
        ("What has many teeth, but can't bite?", "A comb"),
    ]

    # ── QUOTES DATA ───────────────────────────────────────────────

    _QUOTES = [
        "The only way to do great work is to love what you do. — Steve Jobs",
        "Innovation distinguishes between a leader and a follower. — Steve Jobs",
        "Life is what happens when you're busy making other plans. — John Lennon",
        "The purpose of our lives is to be happy. — Dalai Lama",
        "Get busy living or get busy dying. — Stephen King",
        "You only live once, but if you do it right, once is enough. — Mae West",
        "Many of life's failures are people who did not realize how close they were to success when they gave up. — Thomas Edison",
        "The mind is everything. What you think you become. — Buddha",
        "Strive not to be a success, but rather to be of value. — Albert Einstein",
        "I have not failed. I've just found 10,000 ways that won't work. — Thomas Edison",
        "The best time to plant a tree was 20 years ago. The second best time is now. — Chinese Proverb",
        "It is never too late to be what you might have been. — George Eliot",
        "Everything you've ever wanted is on the other side of fear. — George Addair",
        "Believe you can and you're halfway there. — Theodore Roosevelt",
        "The only impossible journey is the one you never begin. — Tony Robbins",
        "Success is not final, failure is not fatal: it is the courage to continue that counts. — Winston Churchill",
        "Hardships often prepare ordinary people for an extraordinary destiny. — C.S. Lewis",
        "The best revenge is massive success. — Frank Sinatra",
        "I think, therefore I am. — René Descartes",
        "Turn your wounds into wisdom. — Oprah Winfrey",
        "The unexamined life is not worth living. — Socrates",
        "To be yourself in a world that is constantly trying to make you something else is the greatest accomplishment. — Ralph Waldo Emerson",
        "It does not matter how slowly you go as long as you do not stop. — Confucius",
        "The future belongs to those who believe in the beauty of their dreams. — Eleanor Roosevelt",
        "Do what you can, with what you have, where you are. — Theodore Roosevelt",
    ]

    _SADQUOTES = [
        "The saddest thing about love is that not only that it cannot last forever, but that heartbreak is soon forgotten. — Truman Capote",
        "Sometimes you have to let go to see if there was anything worth holding onto.",
        "The worst kind of sad is not being able to explain why.",
        "Tears are words that need to be written. — Paulo Coelho",
        "Every man has his secret sorrows which the world knows not. — Henry Wadsworth Longfellow",
        "I have measured out my life with coffee spoons. — T.S. Eliot",
        "We must be willing to let go of the life we planned so as to have the life that is waiting for us. — Joseph Campbell",
        "The only way out of the labyrinth of suffering is to forgive. — John Green",
        "Pain is inevitable. Suffering is optional. — Haruki Murakami",
        "The tragedy of life is not that it ends so soon, but that we wait so long to begin it. — W.M. Lewis",
        "Nobody cares how much you know, until they know how much you care. — Theodore Roosevelt",
        "The broken heart is just the growing pains of a wider heart. — Michael Lipsey",
        "There is no greater sorrow than to recall in misery the time of happy. — Dante Alighieri",
        "Heaven knows we need never be ashamed of our tears. — Charles Dickens",
        "Grief is the price we pay for love. — Queen Elizabeth II",
    ]

    _LOVEQUOTES = [
        "The best thing to hold onto in life is each other. — Audrey Hepburn",
        "Love is composed of a single soul inhabiting two bodies. — Aristotle",
        "Where there is love there is life. — Mahatma Gandhi",
        "Being deeply loved by someone gives you strength, while loving someone deeply gives you courage. — Lao Tzu",
        "The greatest thing you'll ever learn is just to love and be loved in return. — Eden Ahbez",
        "Love all, trust a few, do wrong to none. — William Shakespeare",
        "We accept the love we think we deserve. — Stephen Chbosky",
        "Love is not about possession. Love is about appreciation. — Osho",
        "I have decided to stick with love. Hate is too great a burden to bear. — Martin Luther King Jr.",
        "You know you're in love when you can't fall asleep because reality is finally better than your dreams. — Dr. Seuss",
        "In all the world, there is no heart for me like yours. — Maya Angelou",
        "Love recognizes no barriers. — Maya Angelou",
        "To love and be loved is to feel the sun from both sides. — David Viscott",
        "If I know what love is, it is because of you. — Hermann Hesse",
        "Love does not dominate; it cultivates. — Johann Wolfgang von Goethe",
    ]

    _FUNFACTS = [
        "Honey never spoils. Archaeologists have found 3,000-year-old honey still edible.",
        "Octopuses have three hearts and blue blood.",
        "A group of flamingos is called a 'flamboyance'.",
        "Bananas are berries, but strawberries are not.",
        "The shortest war in history lasted 38 minutes (Anglo-Zanzibar War).",
        "A day on Venus is longer than a year on Venus.",
        "There are more possible iterations of a game of chess than atoms in the observable universe.",
        "Wombat poop is cube-shaped.",
        "A jiffy is an actual unit of time: 1/100th of a second.",
        "The unicorn is the national animal of Scotland.",
        "Sharks are older than trees — they've been around for about 400 million years.",
        "An octopus has nine brains — one central brain and one in each arm.",
        "Cleopatra lived closer to the Moon landing than to the construction of the Great Pyramid.",
        "There's enough DNA in the human body to stretch from the Sun to Pluto and back — 17 times.",
        "The heart of a blue whale is big enough for a human to swim through its arteries.",
        "A cockroach can live for a week without its head.",
        "The inventor of the Pringles can is buried in one.",
        "Sea otters hold hands while they sleep to keep from drifting apart.",
        "The Great Wall of China is not visible from space with the naked eye.",
        "A bolt of lightning is 5 times hotter than the surface of the Sun.",
        "There are more stars in the universe than grains of sand on Earth's beaches.",
        "Dolphins have names for each other — unique signature whistles.",
        "The total weight of all ants on Earth is roughly equal to the total weight of all humans.",
        "Your body contains about 0.2 milligrams of gold.",
        "The Eiffel Tower can grow up to 6 inches taller during the summer.",
        "A teaspoon of neutron star material would weigh about 6 billion tons.",
        "Tardigrades can survive the vacuum of space.",
        "Cows have best friends and get stressed when separated.",
        "The first oranges weren't orange — they were green.",
        "A group of pugs is called a 'grumble'.",
        "There are roughly 1.5 million ants for every human on Earth.",
    ]

    _JOKES = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "I told my wife she was drawing her eyebrows too high. She looked surprised.",
        "Why don't eggs tell jokes? They'd crack each other up!",
        "What do you call a fake noodle? An impasta!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "I'm reading a book about anti-gravity. It's impossible to put down!",
        "What do you call a bear with no teeth? A gummy bear!",
        "Why did the bicycle fall over? Because it was two-tired!",
        "What do you call a dog that does magic? A Labracadabrador!",
        "Why don't skeletons fight each other? They don't have the guts!",
        "I used to hate facial hair, but then it grew on me.",
        "What do you call cheese that isn't yours? Nacho cheese!",
        "Why can't you give Elsa a balloon? Because she'll let it go!",
        "I'm on a seafood diet. I see food and I eat it.",
        "What do you call a sleeping dinosaur? A dino-snore!",
        "Why did the math book look so sad? Because it had too many problems.",
        "What do you call a can opener that doesn't work? A can't opener!",
        "Parallel lines have so much in common. It's a shame they'll never meet.",
        "What did the ocean say to the beach? Nothing, it just waved.",
        "I asked my dog what's two minus two. He said nothing.",
        "Why did the coffee file a police report? It got mugged!",
        "What do you call a lazy kangaroo? A pouch potato!",
        "I told a chemistry joke. There was no reaction.",
        "Why don't oysters share their pearls? Because they're shellfish!",
        "What do you call a snowman with a six-pack? An abdominal snowman!",
        "I was wondering why the frisbee was getting bigger, then it hit me.",
        "What's a cat's favorite color? Purrr-ple!",
        "Why do cows have hooves instead of feet? Because they lactose!",
        "I got fired from the calendar factory. All I did was take a day off.",
        "What's orange and sounds like a parrot? A carrot!",
        "Why did the golfer bring two pairs of pants? In case he got a hole in one!",
    ]

    _DARKJOKES = [
        "I have a stepladder. I never knew my real ladder.",
        "My grandfather has the heart of a lion and a lifetime ban from the local zoo.",
        "What's the worst part about donating a kidney? You're a hero, but donate five and you're 'under investigation'.",
        "I told my doctor that I broke my arm in two places. He told me to stop going to those places.",
        "Why don't orphans play hide and seek? No one is looking for them.",
        "I have a fish that can breakdance. Only for 20 seconds though, and only once.",
        "My wife told me to stop impersonating a flamingo. I had to put my foot down.",
        "They say laughter is the best medicine. That's why I laugh at people with chronic illnesses.",
        "I visited my friend at his new house. He told me to make myself at home. So I kicked him out. I hate having visitors.",
        "Why did the old man fall in the well? Because he couldn't see that well.",
        "I'll never forget my granddad's last words: 'Are you holding the ladder?'",
        "My grief counselor died. He was so good, I don't even care.",
        "As a shellfish, I'm constantly stressed. I just can't come out of my shell.",
        "My wife and I have reached the difficult decision that we do not want children. If anybody does, please send me your contact details and we can drop them off tomorrow.",
        "I have a joke about time travel, but you didn't like it.",
    ]

    _DADJOKES = [
        "I'm afraid for the calendar. Its days are numbered.",
        "What do you call a fish without eyes? A fsh.",
        "My wife said I should do lunges to stay in shape. That would be a big step forward.",
        "Why do fathers take an extra pair of socks when they go golfing? In case they get a hole in one!",
        "I'm reading a book on the history of glue — can't put it down.",
        "I used to work at a shoe recycling shop. It was sole destroying.",
        "What did the ocean say to the beach? Nothing, it just waved.",
        "Did you hear about the guy who invented the knock-knock joke? He won the no-bell prize.",
        "What do you call a belt made of watches? A waist of time!",
        "Singing in the shower is all fun and games until you get shampoo in your mouth. Then it's a soap opera.",
        "I tell dad jokes but I have no kids. I'm a faux pa.",
        "I was going to tell a time-traveling joke, but you guys didn't like it.",
        "What did the zero say to the eight? Nice belt!",
        "I ordered a chicken and an egg from Amazon. I'll let you know.",
        "What do you call a factory that makes okay products? A satisfactory.",
    ]

    _PUNS = [
        "I'm on a seafood diet. I see food and I eat it.",
        "I tried to catch some fog, but I mist.",
        "I'm reading a book about anti-gravity. It's impossible to put down!",
        "I did a theatrical performance about puns. It was a play on words.",
        "I'm friends with all electricians. We have such great current connections.",
        "Broken pencils are pointless.",
        "I used to be a baker, but I couldn't make enough dough.",
        "The guy who invented the door knocker got a No-bell prize.",
        "I got fired from the calendar factory. All I did was take a day off.",
        "A boiled egg is hard to beat.",
        "I know a guy who's addicted to brake fluid. He says he can stop anytime.",
        "I stayed up all night to see where the sun went. Then it dawned on me.",
        "I didn't like my beard at first. Then it grew on me.",
        "I'm no photographer, but I can picture us together.",
        "I told a chemistry joke once. There was no reaction.",
    ]

    _ONELINERS = [
        "I'd tell you a chemistry joke, but I know I wouldn't get a reaction.",
        "Light travels faster than sound. That's why some people appear bright until they speak.",
        "I'm not lazy, I'm on energy-saving mode.",
        "I'm not arguing, I'm just explaining why I'm right.",
        "Common sense is like deodorant — the people who need it most never use it.",
        "I'm not superstitious, but I am a little stitious.",
        "Behind every great person, there's a dog rolling its eyes.",
        "I'm on that diet where you eat everything and hope for a miracle.",
        "My bed and I love each other, but my alarm clock doesn't want to accept it.",
        "I'm not saying I'm Wonder Woman, I'm just saying no one has ever seen us in the same room.",
        "I pretend to work as long as they pretend to pay me.",
        "I'm in shape. Round is a shape.",
        "My life feels like a test I didn't study for.",
        "If I was meant to be controlled, I'd have come with a remote.",
        "I didn't fall. I'm just spending some quality time with the floor.",
    ]

    _SHOWERTHOUGHTS = [
        "If you're waiting for the waiter, aren't you the waiter?",
        "The word 'swims' upside down is still 'swims'.",
        "Your stomach thinks all potatoes are mashed.",
        "We eat pizza from the inside out.",
        "If you clean a vacuum cleaner, you become the vacuum cleaner.",
        "A tag on a mattress says 'Do not remove under penalty of law' but you cut it off the moment you buy it.",
        "Every time you paint a room, it gets slightly smaller.",
        "The first person to discover milk was very brave or very thirsty.",
        "Clapping is just hitting yourself because you like something.",
        "A circle is just a polygon with infinite sides.",
        "Someone was the first person to figure out you can eat eggs.",
        "Tape is just sticky paper that failed at being paper.",
        "You've never seen your own face — only pictures and reflections.",
        "Glasses are just a speedrun for your eyes.",
        "Mars is populated entirely by robots.",
    ]

    _MOVIEQUOTES = [
        "May the Force be with you. — Star Wars",
        "I'm going to make him an offer he can't refuse. — The Godfather",
        "You talking to me? — Taxi Driver",
        "Here's looking at you, kid. — Casablanca",
        "After all, tomorrow is another day! — Gone with the Wind",
        "To infinity and beyond! — Toy Story",
        "I see dead people. — The Sixth Sense",
        "Why so serious? — The Dark Knight",
        "There's no place like home. — The Wizard of Oz",
        "I'll be back. — The Terminator",
        "Life is like a box of chocolates. — Forrest Gump",
        "You can't handle the truth! — A Few Good Men",
        "I am your father. — Star Wars: The Empire Strikes Back",
        "E.T. phone home. — E.T. the Extra-Terrestrial",
        "Houston, we have a problem. — Apollo 13",
    ]

    _PROVERBS = [
        "A stitch in time saves nine.",
        "Actions speak louder than words.",
        "All that glitters is not gold.",
        "An apple a day keeps the doctor away.",
        "Better late than never.",
        "Birds of a feather flock together.",
        "Don't count your chickens before they hatch.",
        "Don't put all your eggs in one basket.",
        "Every cloud has a silver lining.",
        "Fortune favors the bold.",
        "Honesty is the best policy.",
        "Knowledge is power.",
        "Laughter is the best medicine.",
        "Practice makes perfect.",
        "The early bird catches the worm.",
    ]

    _COMPLIMENTS = [
        "You have an incredible energy that lights up any room.",
        "Your smile is contagious and your laugh is infectious!",
        "You're smarter than you give yourself credit for.",
        "You have a gift for making people feel comfortable.",
        "The world is better because you're in it.",
        "You're someone's reason to smile right now.",
        "Your kindness is a balm to everyone who encounters it.",
        "You're a gift to those around you.",
        "You have the courage of your convictions.",
        "You're even more beautiful on the inside than you are on the outside.",
        "Your perspective is refreshing and unique.",
        "You light up the room when you walk in.",
        "You're a great listener and an even better friend.",
        "Jokes are funnier when you tell them.",
        "You have the best ideas.",
        "You're one of a kind and that's your superpower.",
        "Your confidence is inspiring.",
        "You always know how to make people laugh.",
        "You carry yourself with a grace that's rare.",
        "Everything would be better if more people were like you.",
    ]

    _INSULTS = [
        "You're not the dumbest person on the planet, but you better hope they don't die.",
        "I'd agree with you but then we'd both be wrong.",
        "Your face is just fine. It's your personality that needs a makeover.",
        "I'm jealous of people who don't know you.",
        "You have the perfect face for radio.",
        "I'd explain it to you, but I left my crayons at home.",
        "You're like a cloud. When you disappear, it's a beautiful day.",
        "I'm not saying you're ugly, but if you were a scarecrow, the birds would go the other way.",
        "You bring everyone so much joy when you leave the room.",
        "Somewhere out there, a village is missing its idiot.",
        "You're proof that evolution can go in reverse.",
        "I'd roast you, but my mom said not to burn trash.",
        "Your brain is like a stadium — it's huge and completely empty.",
        "If ignorance is bliss, you must be the happiest person alive.",
        "You're the reason the gene pool needs a lifeguard.",
        "I'd call you a tool, but that would be an insult to tools.",
        "You're about as useful as a screen door on a submarine.",
        "If you were any more inbred, you'd be a sandwich.",
        "I'm not saying you're stupid, I'm just saying you have bad luck thinking.",
        "You're the human equivalent of a participation trophy.",
    ]

    _MOTIVATIONAL = [
        "The only limit to our realization of tomorrow is our doubts of today. — Franklin D. Roosevelt",
        "Do what you can, with what you have, where you are. — Theodore Roosevelt",
        "It is during our darkest moments that we must focus to see the light. — Aristotle",
        "The best way to predict your future is to create it. — Abraham Lincoln",
        "Don't watch the clock; do what it does. Keep going. — Sam Levenson",
        "Everything you've ever wanted is sitting on the other side of fear. — George Addair",
        "Success is walking from failure to failure with no loss of enthusiasm. — Winston Churchill",
        "The secret of getting ahead is getting started. — Mark Twain",
        "You miss 100% of the shots you don't take. — Wayne Gretzky",
        "Believe you can and you're halfway there. — Theodore Roosevelt",
        "In the middle of every difficulty lies opportunity. — Albert Einstein",
        "What lies behind us and what lies before us are tiny matters compared to what lies within us. — Ralph Waldo Emerson",
        "Fall seven times, stand up eight. — Japanese Proverb",
        "The only person you are destined to become is the person you decide to be. — Ralph Waldo Emerson",
        "Act as if what you do makes a difference. It does. — William James",
    ]

    _STOIC = [
        "The happiness of your life depends upon the quality of your thoughts. — Marcus Aurelius",
        "We suffer more often in imagination than in reality. — Seneca",
        "It is not that we have a short time to live, but that we waste a good deal of it. — Seneca",
        "You have power over your mind — not outside events. Realize this, and you will find strength. — Marcus Aurelius",
        "How long are you going to wait before you demand the best for yourself? — Epictetus",
        "Waste no more time arguing about what a good man should be. Be one. — Marcus Aurelius",
        "No person has the power to have everything they want, but it is in their power not to want what they don't have. — Seneca",
        "First say to yourself what you would be; and then do what you have to do. — Epictetus",
        "The soul becomes dyed with the color of its thoughts. — Marcus Aurelius",
        "Luck is what happens when preparation meets opportunity. — Seneca",
    ]

    _ZEN = [
        "Before enlightenment, chop wood, carry water. After enlightenment, chop wood, carry water. — Zen Proverb",
        "The quieter you become, the more you can hear. — Ram Dass",
        "When you reach the top of the mountain, keep climbing. — Zen Proverb",
        "Sitting quietly, doing nothing, spring comes, and the grass grows by itself. — Matsuo Basho",
        "The obstacle is the path. — Zen Proverb",
        "When walking, walk. When eating, eat. — Zen Proverb",
        "Do not seek to follow in the footsteps of the wise; seek what they sought. — Matsuo Basho",
        "The bamboo that bends is stronger than the oak that resists. — Japanese Proverb",
        "Let go, and the world lets you in. — Zen Proverb",
        "In the beginner's mind there are many possibilities, in the expert's mind there are few. — Shunryu Suzuki",
    ]

    _USELESSFACTS = [
        "The national animal of Scotland is the unicorn.",
        "It takes 8 minutes and 20 seconds for sunlight to reach Earth.",
        "A group of crows is called a murder.",
        "The inventor of the frisbee was turned into a frisbee after he died.",
        "The King of Hearts is the only king without a mustache.",
        "Polar bears' skin is black and their fur is actually clear, not white.",
        "The longest English word without a vowel is 'rhythms'.",
        "A group of owls is called a parliament.",
        "There's a town in Norway called 'Hell' — it freezes over every winter.",
        "Koala fingerprints are so similar to humans that they've confused crime scene investigators.",
        "A group of porcupines is called a prickle.",
        "The dot over the letter 'i' is called a tittle.",
        "A group of hippos is called a bloat.",
        "The word 'facetious' has all the vowels in order.",
        "Bubble wrap was originally intended to be wallpaper.",
    ]

    _SCIENCEFACTS = [
        "Neutron stars can spin at a rate of 716 times per second.",
        "A single bolt of lightning contains enough energy to toast 100,000 slices of bread.",
        "The human brain uses about 20% of the body's total energy despite being only 2% of body weight.",
        "Hot water freezes faster than cold water — this is called the Mpemba effect.",
        "There are more trees on Earth than stars in the Milky Way.",
        "Venus is the hottest planet in our solar system, not Mercury.",
        "Sound travels about 4.3 times faster in water than in air.",
        "The average human body contains enough carbon to make 9,000 pencils.",
        "There are more bacteria in your body than human cells.",
        "If you could fold a piece of paper 42 times, it would reach the Moon.",
        "Time moves faster at higher altitudes due to gravitational time dilation.",
        "A teaspoon of neutron star material would weigh about 6 billion tons.",
        "Glass is not a solid — it's an amorphous solid that flows very slowly.",
        "The Earth isn't perfectly round — it's an oblate spheroid.",
        "Diamonds rain on Jupiter and Saturn.",
    ]

    _LIMERICKS = [
        "There once was a man from Peru,\nWho dreamed of eating his shoe,\nHe awoke with a fright,\nIn the middle of the night,\nAnd found that his dream had come true.",
        "A flea and a fly in a flue,\nWere caught, so what could they do?\nSaid the fly, 'Let us flee,'\nSaid the flea, 'Let us fly,'\nSo they flew through a flaw in the flue.",
        "There once was a lady named Sue,\nWho had nothing whatever to do,\nShe sat on the stairs,\nAnd counted her hairs,\nAnd found she had forty-two.",
        "A wonderful bird is the pelican,\nHis bill will hold more than his belican,\nHe can take in his beak\nEnough food for a week,\nBut I'm damned if I see how the helican.",
        "There was a young lady named Bright,\nWho traveled much faster than light,\nShe started one day,\nIn the relative way,\nAnd returned on the previous night.",
        "A painter named Jim was so dumb,\nThat he climbed on a ladder to hum,\nBut he fell from the top,\nWith a terrible flop,\nAnd bit his own lower-left thumb.",
        "There once was a baker named Brad,\nWho made the worst bread to be had,\nIt was heavy as lead,\nAnd tasted like dead,\nSo the baker went mad and was sad.",
        "A forgetful old gent in a huff,\nSaid 'I think I have had quite enough,'\nHe went to the store,\nBut forgot what it's for,\nAnd came home with a powder puff.",
        "An ambitious young fellow named Matt,\nTried to launch a new startup from scratch,\nHe coded all night,\nTill the morning light,\nThen found out his dog ate the batch.",
        "There was an old person of Dean,\nWho dined on one single green bean,\nHe was not very fat,\nHe was not very lean,\nThat singular person of Dean.",
    ]

    _DEEPTHOUGHTS = [
        "If the universe is infinite, then somewhere there exists an exact copy of you reading this exact message.",
        "Consciousness might be the universe experiencing itself from infinite perspectives simultaneously.",
        "Every memory you have is just your brain recalling the last time it remembered it, not the original event.",
        "You are the universe's way of thinking about itself.",
        "The atoms in your body were forged in dying stars — you are literally stardust.",
        "Free will might be an illusion, but the illusion is so convincing that it functions as reality.",
        "Time doesn't flow — we move through it, and every moment exists eternally in its own right.",
        "You can never truly experience another person's subjective reality — empathy is always approximate.",
        "The fact that anything exists at all instead of nothing is perhaps the deepest mystery of all.",
        "You are the descendant of every surviving ancestor in an unbroken chain stretching back billions of years.",
    ]

    # ── RATINGS DATA (shared helpers) ─────────────────────────────

    _RATING_EMOJIS = {
        "rate": "⭐", "ship": "❤️", "gayrate": "🌈", "simprate": "🥺",
        "chadrate": "💪", "cute": "🥰", "ugly": "🤮", "smart": "🧠",
        "toxic": "☠️", "powerful": "⚡", "rizz": "😎", "drip": "💧",
        "vibe": "🌊", "aura": "✨", "nerd": "🤓", "sigma": "🐺",
        "rich": "💰", "introvert": "🤫", "extrovert": "🎉", "loyalty": "🤝",
        "saint": "😇", "villain": "🦹", "badassrate": "🔥", "coocrate": "🤡",
        "stankrate": "💨", "waifurate": "💕", "smoothrate": "🛷", "cringrate": "😬",
    }

    _RATING_LABELS = {
        "rate": "Rate", "ship": "Ship", "gayrate": "Gay Rate",
        "simprate": "Simp Rate", "chadrate": "Chad Rate", "cute": "Cuteness",
        "ugly": "Ugliness", "smart": "Smartness", "toxic": "Toxicity",
        "powerful": "Power Level", "rizz": "Rizz Level", "drip": "Drip Level",
        "vibe": "Vibe Check", "aura": "Aura Points", "nerd": "Nerd Level",
        "sigma": "Sigma Energy", "rich": "Rich Energy", "introvert": "Introvert Level",
        "extrovert": "Extrovert Level", "loyalty": "Loyalty", "saint": "Saint Level",
        "villain": "Villain Energy", "badassrate": "Badass Level",
        "coocrate": "Clown Rate", "stankrate": "Stank Level",
        "waifurate": "Waifu Material", "smoothrate": "Smoothness",
        "cringrate": "Cringe Level",
    }

    # ── GENERATORS DATA ───────────────────────────────────────────

    _EXCUSES = [
        "My grandma accidentally sat on my phone.",
        "I was abducted by aliens for a quick chat.",
        "My pet rock had an existential crisis.",
        "I got stuck in a Wikipedia rabbit hole about medieval cheese-making.",
        "A bird stole my sandwich and I had to chase it.",
        "My neighbor's WiFi password changed and I lost all motivation.",
        "I was practicing my dramatic entrance for too long.",
        "My left shoe told me to stay home.",
        "I accidentally joined a cult and orientation ran late.",
        "Time zones confused me into thinking it was tomorrow.",
        "I fell into a social media black hole and couldn't escape.",
        "My horoscope said today was a bad day for productivity.",
        "I was teaching my goldfish to do tricks.",
        "The ghost in my apartment kept hiding my keys.",
        "I was too busy contemplating the meaning of existence.",
    ]

    _ALIBIS = [
        "I was volunteering at the animal shelter — ask Dr. Paws!",
        "I had an emergency meeting with my houseplants about their watering schedule.",
        "I was secretly training for an underground breakdancing competition.",
        "I was attending a very important webinar on the history of napkins.",
        "I was on a covert mission to find the world's best pizza.",
        "I was helping my neighbor's cat resolve its trust issues.",
        "I was trapped in a very intense staring contest with my reflection.",
        "I was busy creating an elaborate backstory for my Sim character.",
        "I was attending the annual convention of people who avoid conventions.",
        "I was in a heated debate with my smart home device about the thermostat.",
        "I was conducting important field research on how many naps are too many naps.",
        "I was busy teaching my Roomba the meaning of life.",
        "I was stuck in an elevator with a mime who wouldn't stop performing.",
        "I was being interviewed for a documentary about professional procrastinators.",
        "I was negotiating a peace treaty between the spiders in my basement.",
    ]

    _FORTUNES = [
        "A beautiful, smart, and loving person will come into your life.",
        "A dubious friend may be an enemy in camouflage.",
        "A faithful friend is a strong defense.",
        "A fresh start will put you on your way.",
        "A golden egg of opportunity falls into your lap this month.",
        "A good time to finish up old tasks.",
        "A lifetime of happiness lies ahead of you.",
        "A light heart carries you through all the hard times.",
        "A pleasant surprise is waiting for you.",
        "All the effort you are making will ultimately pay off.",
        "An important person will offer you support.",
        "Be patient — good things come to those who wait.",
        "Believe in yourself and others will too.",
        "Change is coming — embrace it with open arms.",
        "Curiosity will lead you to unexpected treasures.",
        "Don't just think — act!",
        "Fortune favors the brave.",
        "Good news will come to you by mail.",
        "Happiness begins with facing life with a smile and a wink.",
        "Your ability to juggle many tasks will take you far.",
    ]

    _HOROSCOPES = {
        "aries": "♈ **Aries:** Today is the day to charge forward! Your bold energy will attract unexpected allies.",
        "taurus": "♉ **Taurus:** Patience pays off. A long-awaited answer finally arrives — stay grounded.",
        "gemini": "♊ **Gemini:** Your words carry extra weight today. Use them wisely and watch doors open.",
        "cancer": "♋ **Cancer:** Trust your intuition. Someone close needs your warmth and understanding.",
        "leo": "♌ **Leo:** The spotlight finds you naturally. Share your light and inspire others.",
        "virgo": "♍ **Virgo:** Your attention to detail reveals a hidden opportunity. Don't overlook it.",
        "libra": "♎ **Libra:** Balance is key today. Seek harmony in relationships and decisions.",
        "scorpio": "♏ **Scorpio:** Transformation is in the air. Let go of what no longer serves you.",
        "sagittarius": "♐ **Sagittarius:** Adventure calls! An unexpected journey brings clarity.",
        "capricorn": "♑ **Capricorn:** Your discipline is about to be rewarded. Stay the course.",
        "aquarius": "♒ **Aquarius:** Innovation strikes! Your unique perspective solves an old problem.",
        "pisces": "♓ **Pisces:** Dreams carry messages today. Pay attention to your inner world.",
    }

    _ZODIAC_SIGNS = [
        ("Aries", "♈", "Mar 21 – Apr 19", "Fire"),
        ("Taurus", "♉", "Apr 20 – May 20", "Earth"),
        ("Gemini", "♊", "May 21 – Jun 20", "Air"),
        ("Cancer", "♋", "Jun 21 – Jul 22", "Water"),
        ("Leo", "♌", "Jul 23 – Aug 22", "Fire"),
        ("Virgo", "♍", "Aug 23 – Sep 22", "Earth"),
        ("Libra", "♎", "Sep 23 – Oct 22", "Air"),
        ("Scorpio", "♏", "Oct 23 – Nov 21", "Water"),
        ("Sagittarius", "♐", "Nov 22 – Dec 21", "Fire"),
        ("Capricorn", "♑", "Dec 22 – Jan 19", "Earth"),
        ("Aquarius", "♒", "Jan 20 – Feb 18", "Air"),
        ("Pisces", "♓", "Feb 19 – Mar 20", "Water"),
    ]

    _TAROT_CARDS = [
        ("The Fool", "🃏", "New beginnings, innocence, spontaneity"),
        ("The Magician", "🪄", "Manifestation, resourcefulness, power"),
        ("The High Priestess", "🌙", "Intuition, sacred knowledge, duality"),
        ("The Empress", "👑", "Femininity, beauty, nature, nurturing"),
        ("The Emperor", "🏛", "Authority, structure, control, fatherhood"),
        ("The Hierophant", "📿", "Tradition, conformity, morality, ethics"),
        ("The Lovers", "💕", "Love, harmony, relationships, alignment"),
        ("The Chariot", "⚔️", "Control, willpower, success, determination"),
        ("Strength", "🦁", "Inner strength, bravery, compassion, focus"),
        ("The Hermit", "🏔", "Soul-searching, introspection, solitude"),
        ("Wheel of Fortune", "🎡", "Good luck, karma, destiny, turning point"),
        ("Justice", "⚖️", "Fairness, truth, law, cause and effect"),
        ("The Hanged Man", "🔮", "Sacrifice, release, new perspective"),
        ("Death", "🦋", "Endings, transformation, transition, change"),
        ("Temperance", "🌈", "Balance, moderation, patience, purpose"),
        ("The Devil", "🔗", "Shadow self, attachment, addiction, restriction"),
        ("The Tower", "⛈", "Sudden change, upheaval, chaos, revelation"),
        ("The Star", "⭐", "Hope, faith, renewal, purpose, spirituality"),
        ("The Moon", "🌕", "Illusion, fear, anxiety, subconscious"),
        ("The Sun", "☀️", "Joy, success, celebration, positivity"),
        ("Judgement", "📯", "Judgement, rebirth, inner calling, absolution"),
        ("The World", "🌍", "Completion, accomplishment, travel, integration"),
    ]

    _CRYSTALBALL = [
        "It is certain... probably.",
        "The mists are clearing... nope, just fog. Try again.",
        "Signs point to yes, but the stars are laughing.",
        "The spirits say: maybe next Tuesday.",
        "My vision shows... a cat. This means nothing.",
        "The universe says: proceed with questionable judgment.",
        "I see great fortune — for someone else.",
        "The crystal ball says: ask again after coffee.",
        "Absolutely... not.",
        "The spirits whisper: yeet.",
        "My mystical powers reveal: that's a terrible idea, do it anyway.",
        "The cosmos align in your favor... temporarily.",
        "I foresee unexpected surprises. Or pizza. Probably pizza.",
        "The ancient ones say: lol no.",
        "Destiny suggests you take a nap and reconsider.",
    ]

    _OUIJA = [
        "YES", "NO", "MAYBE", "ASK AGAIN", "LATER", "NOT NOW",
        "GOODBYE", "HELLO", "PERHAPS", "NEVER", "ALWAYS", "SOON",
        "BEWARE", "FOLLOW", "STOP", "GO", "WAIT", "NOW", "DANGER", "TRUST",
    ]

    _MOODS = [
        "🥱 Sleepy — Your body is present, your soul is in bed.",
        "🔥 Hype — Nothing can stop you today!",
        "😢 Melancholic — Missing something you can't name.",
        "😎 Cool — You're the main character right now.",
        "🤪 Chaotic — Brain go brrrrr.",
        "😊 Content — Life is okay right now.",
        "😤 Frustrated — Everything is annoying but you'll survive.",
        "🧘 Zen — At peace with the universe.",
        "🥳 Excited — Good vibes only!",
        "💀 Dead inside — But still functioning somehow.",
        "🤔 Philosophical — Why are we here? What is a 'here'?",
        "😈 Mischievous — Time for some harmless chaos.",
        "🥺 Soft — You need a hug and some warm milk.",
        "🦋 Restless — Something big is coming, you can feel it.",
        "✨ Magical — Everything feels possible right now.",
    ]

    _PERSONALITIES = [
        "The Dreamer — You see possibilities where others see walls.",
        "The Strategist — Three moves ahead, always.",
        "The Wanderer — Home is wherever the WiFi connects.",
        "The Phoenix — You burn bright, and always rise again.",
        "The Storm — Intense, powerful, and impossible to ignore.",
        "The Moon — Quiet strength, mysterious depth, you illuminate the dark.",
        "The Rebel — Rules are just suggestions you choose to ignore.",
        "The Sage — Wisdom flows through you like a river.",
        "The Joker — You find humor in everything, even when it hurts.",
        "The Guardian — Fiercely loyal, you protect what you love.",
        "The Artist — You paint the world in colors others can't see.",
        "The Explorer — Every day is an adventure waiting to happen.",
        "The Catalyst — You make things happen just by being there.",
        "The Enigma — Nobody can quite figure you out, and you like it that way.",
        "The Anchor — When everything falls apart, you keep things grounded.",
    ]

    _SPIRIT_ANIMALS = [
        "🐺 Wolf — Loyal, intuitive, and a natural leader.",
        "🦊 Fox — Clever, adaptable, and quick-witted.",
        "🦁 Lion — Courageous, proud, and born to lead.",
        "🦅 Eagle — Visionary, free-spirited, and focused.",
        "🐻 Bear — Strong, protective, and deeply grounded.",
        "🦉 Owl — Wise, observant, and comfortable in the dark.",
        "🐬 Dolphin — Playful, intelligent, and deeply social.",
        "🦋 Butterfly — Transformative, graceful, and ever-evolving.",
        "🐍 Snake — Mysterious, strategic, and shedding the old.",
        "🐉 Dragon — Powerful, fierce, and legendary.",
        "🦌 Deer — Gentle, graceful, and attuned to nature.",
        "🐆 Panther — Stealthy, confident, and powerful in the shadows.",
        "🦜 Parrot — Colorful, communicative, and full of life.",
        "🐙 Octopus — Multitalented, flexible, and brilliantly creative.",
        "🐈‍⬛ Black Cat — Independent, mysterious, and wonderfully unlucky for others.",
    ]

    _SUPERPOWERS = [
        "⚡ Super Speed — You'll never be late again... or will you?",
        "🔮 Precognition — You see the future, but only 3 seconds ahead.",
        "🧬 Shape-shifting — Be anyone, anywhere, anytime.",
        "💭 Telepathy — Read minds, but you might not like what you hear.",
        "👻 Invisibility — Perfect for awkward social situations.",
        "⏰ Time Manipulation — Pause, rewind, fast-forward reality.",
        "🌊 Hydrokinesis — Control water like a waterbender.",
        "🔥 Pyrokinesis — Fire bends to your will.",
        "🌿 Chlorokinesis — Plants grow at your command.",
        "💫 Gravity Control — Make things float or crush them down.",
        "🛡 Force Fields — Nothing gets through your barriers.",
        "🎵 Sonic Manipulation — Sound itself obeys you.",
        "🌀 Portal Creation — Open doorways to anywhere.",
        "💎 Crystal Generation — Create indestructible structures.",
        "🎭 Illusion Casting — Make people see whatever you want.",
    ]

    _WEAPONS = [
        "⚔️ Sword of Eternal Flame — Burns with never-ending fire.",
        "🏹 Bow of Starlight — Arrows made of concentrated star energy.",
        "🪄 Staff of the Ancients — Channels raw cosmic power.",
        "🗡 Dagger of Shadows — Strikes from the darkness unseen.",
        "🔨 Hammer of Thunder — Each swing creates a shockwave.",
        "🪓 Axe of the Earth — Draws power from the ground itself.",
        "🔱 Trident of the Depths — Commands the ocean's fury.",
        "🏹 Crossbow of Time — Slows enemies with temporal bolts.",
        "🗡 Blade of the Void — Cuts through dimensions.",
        "🛡 Shield of Reflection — Returns attacks to sender.",
        "🪄 Wand of Chaos — Unpredictable but devastating.",
        "⛓ Chain of Binding — Restrains any foe instantly.",
        "💣 Orb of Annihilation — Total destruction in a sphere.",
        "🎯 Throwing Stars of Precision — Never miss their mark.",
        "🎸 Guitar of Sonic Doom — Shreds enemies with sound waves.",
    ]

    _RPG_CLASSES = [
        "⚔️ **Warrior** — Brave, strong, and always on the front lines. HP: High, MP: Low.",
        "🧙 **Mage** — Master of arcane arts. HP: Low, MP: Very High.",
        "🏹 **Ranger** — Swift and deadly from afar. HP: Medium, MP: Medium.",
        "🗡 **Rogue** — Stealthy and cunning. HP: Medium, MP: Medium.",
        "🛡 **Paladin** — Holy warrior of justice. HP: High, MP: Medium.",
        "💀 **Necromancer** — Commands the dead. HP: Low, MP: Very High.",
        "🎵 **Bard** — Inspires allies with music. HP: Medium, MP: High.",
        "🧪 **Alchemist** — Brews potions of power. HP: Medium, MP: High.",
        "🥋 **Monk** — Martial arts master. HP: High, MP: Medium.",
        "🐉 **Dragoon** — Dragon knight of the skies. HP: High, MP: Medium.",
        "🔮 **Warlock** — Dark pact wielder. HP: Low, MP: Very High.",
        "🐺 **Beastmaster** — Commands wild creatures. HP: Medium, MP: Medium.",
        "🎭 **Trickster** — Chaos incarnate. HP: Low, MP: High.",
        "⚔️ **Berserker** — Unstoppable rage. HP: Very High, MP: None.",
        "✨ **Cleric** — Divine healer and protector. HP: Medium, MP: Very High.",
    ]

    _ALIGNMENTS = [
        "⚔️ Lawful Good — The righteous crusader.",
        "🛡 Neutral Good — The benevolent do-gooder.",
        "🌟 Chaotic Good — The rebel with a heart.",
        "⚖️ Lawful Neutral — The impartial judge.",
        "🔄 True Neutral — The balanced observer.",
        "🎲 Chaotic Neutral — The wild card.",
        "👑 Lawful Evil — The tyrant with rules.",
        "🐍 Neutral Evil — The calculating villain.",
        "🔥 Chaotic Evil — The agent of destruction.",
    ]

    _PROPHECIES = [
        "On the seventh dawn, the silent one shall speak, and the walls of illusion shall crumble.",
        "When the last star blinks, a forgotten name shall reshape the world.",
        "Beware the road that splits in three — only the middle path leads home.",
        "The one who laughs at the storm shall command its fury.",
        "An ancient bond will be reforged when two enemies share bread.",
        "The key to the locked door has been in your pocket all along.",
        "When shadows grow longer than their source, the reckoning begins.",
        "A stranger's kindness will unravel a decades-old curse.",
        "The crown will fall not to the strongest, but to the most patient.",
        "What was buried in silence will be unearthed in song.",
    ]

    _PASSWORD_ADJS = [
        "Swift", "Crimson", "Shadow", "Mystic", "Frozen", "Blazing", "Silent",
        "Fierce", "Cosmic", "Ancient", "Hidden", "Savage", "Gentle", "Storm",
        "Golden", "Velvet", "Iron", "Wild", "Dark", "Neon",
    ]

    _PASSWORD_NOUNS = [
        "Phoenix", "Dragon", "Wolf", "Raven", "Storm", "Blade", "Crown",
        "Throne", "Oracle", "Spirit", "Titan", "Viper", "Falcon", "Tempest",
        "Cipher", "Shadow", "Flame", "Frost", "Thunder", "Eclipse",
    ]

    # ── TEXT FUN DATA ──────────────────────────────────────────────

    _ASCII_ARTS = {
        "cat": "ฅ^•ﻌ•^ฅ",
        "dog": "🐕 \\(^ᴗ^)/",
        "fish": "><(((('>",
        "bear": "ʕ•ᴥ•ʔ",
        "bunny": "(\\__/)\n(•_•)\n/ >🥕",
        "frog": "@( * O * )@",
        "owl": "(O,O)\n(   )\n-\"-\"-",
        "snail": "'_'",
        "spider": "//^\\\\\n( o o )\n(  >  )",
        "robot": "[O.O]\n/| |\\\n | |",
    }

    _MORSE = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
        'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
        'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
        'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
        'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
        '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
        '8': '---..', '9': '----.', ' ': '/',
    }

    _BRAILLE_MAP = {
        'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑', 'f': '⠋',
        'g': '⠛', 'h': '⠓', 'i': '⠊', 'j': '⠚', 'k': '⠅', 'l': '⠇',
        'm': '⠍', 'n': '⠝', 'o': '⠕', 'p': '⠏', 'q': '⠟', 'r': '⠗',
        's': '⠎', 't': '⠞', 'u': '⠥', 'v': '⠧', 'w': '⠺', 'x': '⠭',
        'y': '⠽', 'z': '⠵', ' ': ' ',
    }

    _REGIONAL_MAP = {
        'a': '🇦', 'b': '🇧', 'c': '🇨', 'd': '🇩', 'e': '🇪', 'f': '🇫',
        'g': '🇬', 'h': '🇭', 'i': '🇮', 'j': '🇯', 'k': '🇰', 'l': '🇱',
        'm': '🇲', 'n': '🇳', 'o': '🇴', 'p': '🇵', 'q': '🇶', 'r': '🇷',
        's': '🇸', 't': '🇹', 'u': '🇺', 'v': '🇻', 'w': '🇼', 'x': '🇽',
        'y': '🇾', 'z': '🇿', ' ': '   ',
    }

    _FANCY_MAP = {
        'a': 'α', 'b': 'β', 'c': 'ƈ', 'd': 'δ', 'e': 'ε', 'f': 'ƒ',
        'g': 'ɠ', 'h': 'ɦ', 'i': 'ι', 'j': 'ʝ', 'k': 'ƙ', 'l': 'ʅ',
        'm': 'ɱ', 'n': 'ɳ', 'o': 'σ', 'p': 'ρ', 'q': 'φ', 'r': 'ɾ',
        's': 'ʂ', 't': 'ƚ', 'u': 'υ', 'v': 'ʋ', 'w': 'ω', 'x': 'χ',
        'y': 'ψ', 'z': 'ζ',
    }

    _SMALL_MAP = {
        'a': 'ᵃ', 'b': 'ᵇ', 'c': 'ᶜ', 'd': 'ᵈ', 'e': 'ᵉ', 'f': 'ᶠ',
        'g': 'ᵍ', 'h': 'ʰ', 'i': 'ⁱ', 'j': 'ʲ', 'k': 'ᵏ', 'l': 'ˡ',
        'm': 'ᵐ', 'n': 'ⁿ', 'o': 'ᵒ', 'p': 'ᵖ', 'q': 'q', 'r': 'ʳ',
        's': 'ˢ', 't': 'ᵗ', 'u': 'ᵘ', 'v': 'ᵛ', 'w': 'ʷ', 'x': 'ˣ',
        'y': 'ʸ', 'z': 'ᶻ',
    }

    _ZALGO_ABOVE = ['\u0300', '\u0301', '\u0302', '\u0303', '\u0304', '\u0305',
                    '\u0306', '\u0307', '\u0308', '\u0309', '\u030A', '\u030B',
                    '\u030C', '\u030D', '\u030E', '\u030F', '\u0310', '\u0311',
                    '\u0312', '\u0313', '\u0314', '\u0315']

    _ZALGO_BELOW = ['\u0316', '\u0317', '\u0318', '\u0319', '\u031A', '\u031B',
                    '\u031C', '\u031D', '\u031E', '\u031F', '\u0320', '\u0321',
                    '\u0322', '\u0323', '\u0324', '\u0325', '\u0326', '\u0327',
                    '\u0328', '\u0329', '\u032A', '\u032B']

    _EMOJI_LIST = [
        "🎉", "🔥", "💀", "😱", "😍", "🤣", "✨", "🌈", "🦄", "🍕",
        "🎸", "💎", "🚀", "🎯", "🌟", "🧠", "⚡", "🌸", "🎭", "👑",
    ]

    # ═══════════════════════════════════════════════════════════════
    #  HELPER FUNCTIONS
    # ═══════════════════════════════════════════════════════════════

    def _hash_rate(target: str, key: str) -> int:
        """Deterministic 0-100 rating based on hash."""
        h = hashlib.md5(f"{key}:{target}".encode()).hexdigest()
        return int(h, 16) % 101

    def _get_target_name(message) -> str:
        """Get target user's first name from reply or self."""
        if message.reply_to_message and message.reply_to_message.from_user:
            return message.reply_to_message.from_user.first_name
        args = message.text.split(None, 1)
        if len(args) > 1:
            return args[1].strip()
        return message.from_user.first_name

    def _make_bar(pct: int) -> str:
        """Make a visual progress bar from 0-100."""
        filled = pct // 10
        empty = 10 - filled
        return "█" * filled + "░" * empty

    def _make_rating_message(target: str, key: str, label: str, emoji: str) -> str:
        """Build a rating message with bar."""
        pct = _hash_rate(target.lower(), key)
        bar = _make_bar(pct)
        return f"{emoji} **{label}** for **{target}**\n\n`[{bar}]` **{pct}%**"

    # ═══════════════════════════════════════════════════════════════
    #  GAMES (23 commands)
    # ═══════════════════════════════════════════════════════════════

    # 1. 8BALL
    @app.on_message(filters.command("8ball", prefixes=".") & filters.me)
    async def eightball_cmd(client, message):
        args = message.text.split(None, 1)
        question = args[1] if len(args) > 1 else "..."
        answer = random.choice(_8BALL)
        await message.edit(f"🎱 **Question:** {question}\n\n🔮 **Answer:** {answer}")

    register_command("Fun", "8ball", "Magic 8-ball with 20 responses")

    # 2. ROLL
    @app.on_message(filters.command("roll", prefixes=".") & filters.me)
    async def roll_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) > 1:
            spec = args[1].strip().lower()
            if "d" in spec:
                parts = spec.split("d", 1)
                try:
                    n = int(parts[0]) if parts[0] else 1
                    sides = int(parts[1])
                    if n < 1 or n > 100 or sides < 1 or sides > 1000:
                        raise ValueError
                except ValueError:
                    await message.edit("❌ **Usage:** `.roll NdN` (e.g. `.roll 2d6`)")
                    return
            else:
                try:
                    sides = int(spec)
                    n = 1
                except ValueError:
                    await message.edit("❌ **Usage:** `.roll NdN` (e.g. `.roll 2d6`)")
                    return
        else:
            n, sides = 1, 6
        rolls = [random.randint(1, sides) for _ in range(n)]
        total = sum(rolls)
        if n == 1:
            await message.edit(f"🎲 You rolled a **{total}** (d{sides})")
        else:
            rolls_str = " + ".join(str(r) for r in rolls)
            await message.edit(f"🎲 Rolled {n}d{sides}: [{rolls_str}] = **{total}**")

    register_command("Fun", "roll", "Roll dice in NdN format (e.g. 2d6)")

    # 3. FLIP
    @app.on_message(filters.command("flip", prefixes=".") & filters.me)
    async def flip_cmd(client, message):
        result = random.choice(["Heads 🪙", "Tails 🪙"])
        await message.edit(f"🪙 **Coin Flip:** {result}")

    register_command("Fun", "flip", "Flip a coin")

    # 4. CHOOSE
    @app.on_message(filters.command("choose", prefixes=".") & filters.me)
    async def choose_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.choose option1 | option2 | option3`")
            return
        options = [o.strip() for o in args[1].split("|") if o.strip()]
        if len(options) < 2:
            await message.edit("❌ Give at least 2 options separated by `|`")
            return
        choice = random.choice(options)
        await message.edit(f"🤔 **Options:** {', '.join(options)}\n\n🎯 **I choose:** {choice}")

    register_command("Fun", "choose", "Choose from options separated by |")

    # 5. RPS
    @app.on_message(filters.command("rps", prefixes=".") & filters.me)
    async def rps_cmd(client, message):
        args = message.text.split(None, 1)
        choices = ["rock", "paper", "scissors"]
        emojis = {"rock": "🪨", "paper": "📄", "scissors": "✂️"}
        user = args[1].strip().lower() if len(args) > 1 else ""
        if user not in choices:
            await message.edit("❌ **Usage:** `.rps rock|paper|scissors`")
            return
        bot = random.choice(choices)
        if user == bot:
            result = "Draw! 🤝"
        elif (user == "rock" and bot == "scissors") or \
             (user == "paper" and bot == "rock") or \
             (user == "scissors" and bot == "paper"):
            result = "You win! 🎉"
        else:
            result = "You lose! 😢"
        await message.edit(
            f"🤜 **You:** {emojis[user]} {user.title()}\n"
            f"🤖 **Bot:** {emojis[bot]} {bot.title()}\n\n"
            f"**{result}**"
        )

    register_command("Fun", "rps", "Rock Paper Scissors")

    # 6. TRUTH
    @app.on_message(filters.command("truth", prefixes=".") & filters.me)
    async def truth_cmd(client, message):
        truth = random.choice(_TRUTHS)
        await message.edit(f"🤔 **Truth:** {truth}")

    register_command("Fun", "truth", "Random truth question")

    # 7. DARE
    @app.on_message(filters.command("dare", prefixes=".") & filters.me)
    async def dare_cmd(client, message):
        dare = random.choice(_DARES)
        await message.edit(f"😈 **Dare:** {dare}")

    register_command("Fun", "dare", "Random dare challenge")

    # 8. WOULDYOURATHER / WYR
    @app.on_message(filters.command(["wouldyourather", "wyr"], prefixes=".") & filters.me)
    async def wyr_cmd(client, message):
        wyr = random.choice(_WYR)
        await message.edit(f"🤯 **Would You Rather:**\n\n{wyr}")

    register_command("Fun", "wouldyourather", "Would you rather question", aliases=["wyr"])

    # 9. NEVERHAVEIEVER / NHIE
    @app.on_message(filters.command(["neverhaveiever", "nhie"], prefixes=".") & filters.me)
    async def nhie_cmd(client, message):
        nhie = random.choice(_NHIE)
        await message.edit(f"🤫 **Never Have I Ever:**\n\n{nhie}")

    register_command("Fun", "neverhaveiever", "Never Have I Ever question", aliases=["nhie"])

    # 10. GUESS
    @app.on_message(filters.command("guess", prefixes=".") & filters.me)
    async def guess_cmd(client, message):
        number = random.randint(1, 10)
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit(f"🔢 I'm thinking of a number between 1-10. Use `.guess <number>` to play!")
            return
        try:
            user_guess = int(args[1].strip())
        except ValueError:
            await message.edit("❌ Enter a valid number!")
            return
        if user_guess == number:
            await message.edit(f"🎉 **Correct!** The number was **{number}**! You got it!")
        elif abs(user_guess - number) <= 2:
            await message.edit(f"🔥 **Close!** The number was **{number}**. You guessed {user_guess}.")
        else:
            await message.edit(f"❌ **Wrong!** The number was **{number}**. You guessed {user_guess}.")

    register_command("Fun", "guess", "Guess a number 1-10")

    # 11. TRIVIA
    @app.on_message(filters.command("trivia", prefixes=".") & filters.me)
    async def trivia_cmd(client, message):
        q, a = random.choice(_TRIVIA)
        await message.edit(f"🧠 **Trivia:**\n\n{q}\n\n||Answer: {a}||")

    register_command("Fun", "trivia", "Random trivia with spoiler answer")

    # 12. RIDDLE
    @app.on_message(filters.command("riddle", prefixes=".") & filters.me)
    async def riddle_cmd(client, message):
        riddle, answer = random.choice(_RIDDLES)
        await message.edit(f"🤔 **Riddle:**\n\n{riddle}\n\n||Answer: {answer}||")

    register_command("Fun", "riddle", "Random riddle with spoiler answer")

    # 13. DICEROLL
    @app.on_message(filters.command("diceroll", prefixes=".") & filters.me)
    async def diceroll_cmd(client, message):
        args = message.text.split(None, 1)
        try:
            sides = int(args[1].strip()) if len(args) > 1 else 6
            if sides < 2 or sides > 100:
                sides = 6
        except ValueError:
            sides = 6
        result = random.randint(1, sides)
        await message.edit(f"🎲 **Dice Roll (d{sides}):** You got **{result}**!")

    register_command("Fun", "diceroll", "Roll a die with optional sides")

    # 14. MAGICBALL
    @app.on_message(filters.command("magicball", prefixes=".") & filters.me)
    async def magicball_cmd(client, message):
        args = message.text.split(None, 1)
        question = args[1] if len(args) > 1 else "..."
        responses = [
            "Absolutely YES!", "The stars say YES!", "Without a doubt!",
            "Looks promising!", "Signs point to yes!", "Probably!",
            "Maybe, maybe not...", "Ask again later...", "Not looking good...",
            "My sources say NO!", "Definitely NO!", "Very unlikely!",
        ]
        answer = random.choice(responses)
        await message.edit(f"🔮 **Magic Ball**\n\n❓ {question}\n\n✨ {answer}")

    register_command("Fun", "magicball", "Magic ball fortune")

    # 15. FATE
    @app.on_message(filters.command("fate", prefixes=".") & filters.me)
    async def fate_cmd(client, message):
        fates = [
            "🌟 Great fortune awaits you!", "🌑 Dark times ahead, stay strong.",
            "💫 A surprise will change everything.", "🔥 A trial by fire is coming.",
            "🌸 Peace and harmony are near.", "⚡ Expect the unexpected.",
            "🎭 A twist of fate approaches.", "🏔 A mountain to climb, but the view is worth it.",
            "🌊 A wave of change is coming.", "🍀 Luck is on your side today.",
        ]
        await message.edit(f"🧭 **Fate:** {random.choice(fates)}")

    register_command("Fun", "fate", "Discover your fate")

    # 16. LUCK
    @app.on_message(filters.command("luck", prefixes=".") & filters.me)
    async def luck_cmd(client, message):
        pct = random.randint(0, 100)
        if pct >= 80:
            label = "🍀 Incredibly lucky!"
        elif pct >= 60:
            label = "✨ Pretty lucky!"
        elif pct >= 40:
            label = "😐 Average luck."
        elif pct >= 20:
            label = "😬 Not so lucky..."
        else:
            label = "💀 Terribly unlucky!"
        bar = _make_bar(pct)
        await message.edit(f"🍀 **Luck Check**\n\n`[{bar}]` **{pct}%** — {label}")

    register_command("Fun", "luck", "Check your luck percentage")

    # 17. YESNO
    @app.on_message(filters.command("yesno", prefixes=".") & filters.me)
    async def yesno_cmd(client, message):
        args = message.text.split(None, 1)
        question = args[1] if len(args) > 1 else "..."
        answer = random.choice(["✅ Yes!", "❌ No!", "🤷 Maybe?"])
        await message.edit(f"❓ {question}\n\n🎱 {answer}")

    register_command("Fun", "yesno", "Random yes/no/maybe answer")

    # 18. DECIDE
    @app.on_message(filters.command("decide", prefixes=".") & filters.me)
    async def decide_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.decide <something>`")
            return
        decision = random.choice(["Do it! ✅", "Don't do it! ❌", "Think about it more 🤔"])
        await message.edit(f"🤔 Should I {args[1]}?\n\n🎯 {decision}")

    register_command("Fun", "decide", "Let the bot decide for you")

    # 19. PROBABILITY / PROB
    @app.on_message(filters.command(["probability", "prob"], prefixes=".") & filters.me)
    async def prob_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.prob <something>`")
            return
        pct = random.randint(0, 100)
        bar = _make_bar(pct)
        await message.edit(f"📊 **Probability:** {args[1]}\n\n`[{bar}]` **{pct}%**")

    register_command("Fun", "probability", "Random probability percentage", aliases=["prob"])

    # 20. COINFLIP / CF
    @app.on_message(filters.command(["coinflip", "cf"], prefixes=".") & filters.me)
    async def coinflip_cmd(client, message):
        result = random.choice(["Heads 🪙", "Tails 🪙"])
        await message.edit(f"🪙 **Coin Flip:** {result}")

    register_command("Fun", "coinflip", "Flip a coin", aliases=["cf"])

    # 21. SLOTS
    @app.on_message(filters.command("slots", prefixes=".") & filters.me)
    async def slots_cmd(client, message):
        symbols = ["🍒", "🍋", "🍊", "🍇", "💎", "7️⃣", "🔔"]
        s1, s2, s3 = [random.choice(symbols) for _ in range(3)]
        if s1 == s2 == s3:
            result = "🎉 **JACKPOT!!!** 🎉"
        elif s1 == s2 or s2 == s3 or s1 == s3:
            result = "✨ **Small Win!**"
        else:
            result = "😢 **No luck!**"
        await message.edit(f"🎰 **Slots**\n\n│ {s1} │ {s2} │ {s3} │\n\n{result}")

    register_command("Fun", "slots", "Slot machine game")

    # 22. LOTTERY
    @app.on_message(filters.command("lottery", prefixes=".") & filters.me)
    async def lottery_cmd(client, message):
        numbers = sorted(random.sample(range(1, 50), 6))
        bonus = random.randint(1, 10)
        nums_str = " - ".join(str(n) for n in numbers)
        await message.edit(f"🎟 **Lottery Numbers:**\n\n🎯 {nums_str} | ⭐ Bonus: {bonus}")

    register_command("Fun", "lottery", "Generate lottery numbers")

    # 23. COUNTDOWN
    @app.on_message(filters.command("countdown", prefixes=".") & filters.me)
    async def countdown_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.countdown <seconds>`")
            return
        try:
            seconds = int(args[1].strip())
            if seconds < 1 or seconds > 60:
                await message.edit("❌ Enter seconds between 1 and 60.")
                return
        except ValueError:
            await message.edit("❌ Enter a valid number of seconds.")
            return
        msg = await message.edit(f"⏳ **Countdown:** {seconds}")
        for i in range(seconds - 1, 0, -1):
            await asyncio.sleep(1)
            try:
                await msg.edit(f"⏳ **Countdown:** {i}")
            except Exception:
                return
        await asyncio.sleep(1)
        try:
            await msg.edit("🎉 **Time's up!**")
        except Exception:
            pass

    register_command("Fun", "countdown", "Countdown timer (1-60 seconds)")

    # ═══════════════════════════════════════════════════════════════
    #  QUOTES (21 commands)
    # ═══════════════════════════════════════════════════════════════

    # 24. QUOTE
    @app.on_message(filters.command("quote", prefixes=".") & filters.me)
    async def quote_cmd(client, message):
        await message.edit(f"💬 {random.choice(_QUOTES)}")

    register_command("Fun", "quote", "Random inspirational quote")

    # 25. SADQUOTE
    @app.on_message(filters.command("sadquote", prefixes=".") & filters.me)
    async def sadquote_cmd(client, message):
        await message.edit(f"😢 {random.choice(_SADQUOTES)}")

    register_command("Fun", "sadquote", "Random sad quote")

    # 26. LOVEQUOTE
    @app.on_message(filters.command("lovequote", prefixes=".") & filters.me)
    async def lovequote_cmd(client, message):
        await message.edit(f"💕 {random.choice(_LOVEQUOTES)}")

    register_command("Fun", "lovequote", "Random love quote")

    # 27. FUNFACT / FACT
    @app.on_message(filters.command(["funfact", "fact"], prefixes=".") & filters.me)
    async def funfact_cmd(client, message):
        await message.edit(f"🧪 **Fun Fact:** {random.choice(_FUNFACTS)}")

    register_command("Fun", "funfact", "Random fun fact", aliases=["fact"])

    # 28. JOKE
    @app.on_message(filters.command("joke", prefixes=".") & filters.me)
    async def joke_cmd(client, message):
        await message.edit(f"😂 {random.choice(_JOKES)}")

    register_command("Fun", "joke", "Random joke")

    # 29. DARKJOKE
    @app.on_message(filters.command("darkjoke", prefixes=".") & filters.me)
    async def darkjoke_cmd(client, message):
        await message.edit(f"🖤 {random.choice(_DARKJOKES)}")

    register_command("Fun", "darkjoke", "Random dark humor joke")

    # 30. DADJOKE
    @app.on_message(filters.command("dadjoke", prefixes=".") & filters.me)
    async def dadjoke_cmd(client, message):
        await message.edit(f"👨 {random.choice(_DADJOKES)}")

    register_command("Fun", "dadjoke", "Random dad joke")

    # 31. PUN
    @app.on_message(filters.command("pun", prefixes=".") & filters.me)
    async def pun_cmd(client, message):
        await message.edit(f"🤭 {random.choice(_PUNS)}")

    register_command("Fun", "pun", "Random pun")

    # 32. ONELINER
    @app.on_message(filters.command("oneliner", prefixes=".") & filters.me)
    async def oneliner_cmd(client, message):
        await message.edit(f"💡 {random.choice(_ONELINERS)}")

    register_command("Fun", "oneliner", "Random one-liner")

    # 33. SHOWERTHOUGHT
    @app.on_message(filters.command("showerthought", prefixes=".") & filters.me)
    async def showerthought_cmd(client, message):
        await message.edit(f"🚿 {random.choice(_SHOWERTHOUGHTS)}")

    register_command("Fun", "showerthought", "Random shower thought")

    # 34. MOVIEQUOTE
    @app.on_message(filters.command("moviequote", prefixes=".") & filters.me)
    async def moviequote_cmd(client, message):
        await message.edit(f"🎬 {random.choice(_MOVIEQUOTES)}")

    register_command("Fun", "moviequote", "Random movie quote")

    # 35. PROVERB
    @app.on_message(filters.command("proverb", prefixes=".") & filters.me)
    async def proverb_cmd(client, message):
        await message.edit(f"📜 {random.choice(_PROVERBS)}")

    register_command("Fun", "proverb", "Random proverb")

    # 36. COMPLIMENT
    @app.on_message(filters.command("compliment", prefixes=".") & filters.me)
    async def compliment_cmd(client, message):
        target = _get_target_name(message)
        comp = random.choice(_COMPLIMENTS)
        await message.edit(f"💐 **Compliment for {target}:**\n\n{comp}")

    register_command("Fun", "compliment", "Random compliment for someone")

    # 37. INSULT
    @app.on_message(filters.command("insult", prefixes=".") & filters.me)
    async def insult_cmd(client, message):
        target = _get_target_name(message)
        ins = random.choice(_INSULTS)
        await message.edit(f"🔥 **Roast for {target}:**\n\n{ins}")

    register_command("Fun", "insult", "Random insult/roast for someone")

    # 38. MOTIVATIONAL / MOTIVATE
    @app.on_message(filters.command(["motivational", "motivate"], prefixes=".") & filters.me)
    async def motivational_cmd(client, message):
        await message.edit(f"💪 {random.choice(_MOTIVATIONAL)}")

    register_command("Fun", "motivational", "Random motivational quote", aliases=["motivate"])

    # 39. STOIC
    @app.on_message(filters.command("stoic", prefixes=".") & filters.me)
    async def stoic_cmd(client, message):
        await message.edit(f"🏛 {random.choice(_STOIC)}")

    register_command("Fun", "stoic", "Random Stoic philosophy quote")

    # 40. ZEN
    @app.on_message(filters.command("zen", prefixes=".") & filters.me)
    async def zen_cmd(client, message):
        await message.edit(f"☯️ {random.choice(_ZEN)}")

    register_command("Fun", "zen", "Random Zen quote")

    # 41. USELESSFACT
    @app.on_message(filters.command("uselessfact", prefixes=".") & filters.me)
    async def uselessfact_cmd(client, message):
        await message.edit(f"🤷 **Useless Fact:** {random.choice(_USELESSFACTS)}")

    register_command("Fun", "uselessfact", "Random useless fact")

    # 42. SCIENCEFACT
    @app.on_message(filters.command("sciencefact", prefixes=".") & filters.me)
    async def sciencefact_cmd(client, message):
        await message.edit(f"🔬 {random.choice(_SCIENCEFACTS)}")

    register_command("Fun", "sciencefact", "Random science fact")

    # 43. LIMERICK
    @app.on_message(filters.command("limerick", prefixes=".") & filters.me)
    async def limerick_cmd(client, message):
        await message.edit(f"📝 **Limerick:**\n\n{random.choice(_LIMERICKS)}")

    register_command("Fun", "limerick", "Random limerick poem")

    # 44. DEEPTHOUGHT
    @app.on_message(filters.command("deepthought", prefixes=".") & filters.me)
    async def deepthought_cmd(client, message):
        await message.edit(f"🧘 {random.choice(_DEEPTHOUGHTS)}")

    register_command("Fun", "deepthought", "Random deep philosophical thought")

    # ═══════════════════════════════════════════════════════════════
    #  RATINGS (28 commands)
    # ═══════════════════════════════════════════════════════════════

    # 45. RATE
    @app.on_message(filters.command("rate", prefixes=".") & filters.me)
    async def rate_cmd(client, message):
        target = _get_target_name(message)
        await message.edit(_make_rating_message(target, "rate", _RATING_LABELS["rate"], _RATING_EMOJIS["rate"]))

    register_command("Fun", "rate", "Rate someone 0-100%")

    # 46. SHIP
    @app.on_message(filters.command("ship", prefixes=".") & filters.me)
    async def ship_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) > 1 and "+" in args[1]:
            names = [n.strip() for n in args[1].split("+", 1)]
        elif message.reply_to_message and message.reply_to_message.from_user:
            names = [message.from_user.first_name, message.reply_to_message.from_user.first_name]
        else:
            await message.edit("❌ **Usage:** `.ship Name1 + Name2` or reply to someone")
            return
        ship_name = names[0][:len(names[0])//2+1] + names[1][len(names[1])//2:]
        pct = _hash_rate((names[0] + names[1]).lower(), "ship")
        bar = _make_bar(pct)
        if pct >= 80:
            label = "💕 Perfect Match!"
        elif pct >= 60:
            label = "❤️ Great Chemistry!"
        elif pct >= 40:
            label = "💛 Could Work!"
        elif pct >= 20:
            label = "💔 Unlikely..."
        else:
            label = "💀 Doomed!"
        await message.edit(
            f"❤️ **Ship:** {names[0]} + {names[1]}\n"
            f"💕 **Ship Name:** {ship_name}\n\n"
            f"`[{bar}]` **{pct}%** — {label}"
        )

    register_command("Fun", "ship", "Ship two people together")

    # 47. GAYRATE / GR
    @app.on_message(filters.command(["gayrate", "gr"], prefixes=".") & filters.me)
    async def gayrate_cmd(client, message):
        target = _get_target_name(message)
        await message.edit(_make_rating_message(target, "gayrate", _RATING_LABELS["gayrate"], _RATING_EMOJIS["gayrate"]))

    register_command("Fun", "gayrate", "Gay rate 0-100%", aliases=["gr"])

    # 48. SIMPRATE / SR
    @app.on_message(filters.command(["simprate", "sr"], prefixes=".") & filters.me)
    async def simprate_cmd(client, message):
        target = _get_target_name(message)
        await message.edit(_make_rating_message(target, "simprate", _RATING_LABELS["simprate"], _RATING_EMOJIS["simprate"]))

    register_command("Fun", "simprate", "Simp rate 0-100%", aliases=["sr"])

    # 49. CHADRATE / CR
    @app.on_message(filters.command(["chadrate", "cr"], prefixes=".") & filters.me)
    async def chadrate_cmd(client, message):
        target = _get_target_name(message)
        await message.edit(_make_rating_message(target, "chadrate", _RATING_LABELS["chadrate"], _RATING_EMOJIS["chadrate"]))

    register_command("Fun", "chadrate", "Chad rate 0-100%", aliases=["cr"])

    # 50. CUTE
    @app.on_message(filters.command("cute", prefixes=".") & filters.me)
    async def cute_cmd(client, message):
        target = _get_target_name(message)
        await message.edit(_make_rating_message(target, "cute", _RATING_LABELS["cute"], _RATING_EMOJIS["cute"]))

    register_command("Fun", "cute", "Cuteness rate 0-100%")

    # 51. UGLY
    @app.on_message(filters.command("ugly", prefixes=".") & filters.me)
    async def ugly_cmd(client, message):
        target = _get_target_name(message)
        await message.edit(_make_rating_message(target, "ugly", _RATING_LABELS["ugly"], _RATING_EMOJIS["ugly"]))

    register_command("Fun", "ugly", "Ugliness rate 0-100%")

    # 52. SMART
    @app.on_message(filters.command("smart", prefixes=".") & filters.me)
    async def smart_cmd(client, message):
        target = _get_target_name(message)
        await message.edit(_make_rating_message(target, "smart", _RATING_LABELS["smart"], _RATING_EMOJIS["smart"]))

    register_command("Fun", "smart", "Smartness rate 0-100%")

    # 53. TOXIC
    @app.on_message(filters.command("toxic", prefixes=".") & filters.me)
    async def toxic_cmd(client, message):
        target = _get_target_name(message)
        await message.edit(_make_rating_message(target, "toxic", _RATING_LABELS["toxic"], _RATING_EMOJIS["toxic"]))

    register_command("Fun", "toxic", "Toxicity rate 0-100%")

    # 54. POWERFUL
    @app.on_message(filters.command("powerful", prefixes=".") & filters.me)
    async def powerful_cmd(client, message):
        target = _get_target_name(message)
        await message.edit(_make_rating_message(target, "powerful", _RATING_LABELS["powerful"], _RATING_EMOJIS["powerful"]))

    register_command("Fun", "powerful", "Power level rate 0-100%")

    # 55. RIZZ
    @app.on_message(filters.command("rizz", prefixes=".") & filters.me)
    async def rizz_cmd(client, message):
        target = _get_target_name(message)
        await message.edit(_make_rating_message(target, "rizz", _RATING_LABELS["rizz"], _RATING_EMOJIS["rizz"]))

    register_command("Fun", "rizz", "Rizz level rate 0-100%")

    # 56. DRIP
    @app.on_message(filters.command("drip", prefixes=".") & filters.me)
    async def drip_cmd(client, message):
        target = _get_target_name(message)
        await message.edit(_make_rating_message(target, "drip", _RATING_LABELS["drip"], _RATING_EMOJIS["drip"]))

    register_command("Fun", "drip", "Drip level rate 0-100%")

    # 57. VIBE
    @app.on_message(filters.command("vibe", prefixes=".") & filters.me)
    async def vibe_cmd(client, message):
        target = _get_target_name(message)
        await message.edit(_make_rating_message(target, "vibe", _RATING_LABELS["vibe"], _RATING_EMOJIS["vibe"]))

    register_command("Fun", "vibe", "Vibe check rate 0-100%")

    # 58. AURA
    @app.on_message(filters.command("aura", prefixes=".") & filters.me)
    async def aura_cmd(client, message):
        target = _get_target_name(message)
        await message.edit(_make_rating_message(target, "aura", _RATING_LABELS["aura"], _RATING_EMOJIS["aura"]))

    register_command("Fun", "aura", "Aura points rate 0-100%")

    # 59. NERD
    @app.on_message(filters.command("nerd", prefixes=".") & filters.me)
    async def nerd_cmd(client, message):
        target = _get_target_name(message)
        await message.edit(_make_rating_message(target, "nerd", _RATING_LABELS["nerd"], _RATING_EMOJIS["nerd"]))

    register_command("Fun", "nerd", "Nerd level rate 0-100%")

    # 60. SIGMA
    @app.on_message(filters.command("sigma", prefixes=".") & filters.me)
    async def sigma_cmd(client, message):
        target = _get_target_name(message)
        await message.edit(_make_rating_message(target, "sigma", _RATING_LABELS["sigma"], _RATING_EMOJIS["sigma"]))

    register_command("Fun", "sigma", "Sigma energy rate 0-100%")

    # 61. RICH
    @app.on_message(filters.command("rich", prefixes=".") & filters.me)
    async def rich_cmd(client, message):
        target = _get_target_name(message)
        await message.edit(_make_rating_message(target, "rich", _RATING_LABELS["rich"], _RATING_EMOJIS["rich"]))

    register_command("Fun", "rich", "Rich energy rate 0-100%")

    # 62. INTROVERT
    @app.on_message(filters.command("introvert", prefixes=".") & filters.me)
    async def introvert_cmd(client, message):
        target = _get_target_name(message)
        await message.edit(_make_rating_message(target, "introvert", _RATING_LABELS["introvert"], _RATING_EMOJIS["introvert"]))

    register_command("Fun", "introvert", "Introvert level rate 0-100%")

    # 63. EXTROVERT
    @app.on_message(filters.command("extrovert", prefixes=".") & filters.me)
    async def extrovert_cmd(client, message):
        target = _get_target_name(message)
        await message.edit(_make_rating_message(target, "extrovert", _RATING_LABELS["extrovert"], _RATING_EMOJIS["extrovert"]))

    register_command("Fun", "extrovert", "Extrovert level rate 0-100%")

    # 64. LOYALTY
    @app.on_message(filters.command("loyalty", prefixes=".") & filters.me)
    async def loyalty_cmd(client, message):
        target = _get_target_name(message)
        await message.edit(_make_rating_message(target, "loyalty", _RATING_LABELS["loyalty"], _RATING_EMOJIS["loyalty"]))

    register_command("Fun", "loyalty", "Loyalty rate 0-100%")

    # 65. SAINT
    @app.on_message(filters.command("saint", prefixes=".") & filters.me)
    async def saint_cmd(client, message):
        target = _get_target_name(message)
        await message.edit(_make_rating_message(target, "saint", _RATING_LABELS["saint"], _RATING_EMOJIS["saint"]))

    register_command("Fun", "saint", "Saint level rate 0-100%")

    # 66. VILLAIN
    @app.on_message(filters.command("villain", prefixes=".") & filters.me)
    async def villain_cmd(client, message):
        target = _get_target_name(message)
        await message.edit(_make_rating_message(target, "villain", _RATING_LABELS["villain"], _RATING_EMOJIS["villain"]))

    register_command("Fun", "villain", "Villain energy rate 0-100%")

    # 67. BADASSRATE
    @app.on_message(filters.command("badassrate", prefixes=".") & filters.me)
    async def badassrate_cmd(client, message):
        target = _get_target_name(message)
        await message.edit(_make_rating_message(target, "badassrate", _RATING_LABELS["badassrate"], _RATING_EMOJIS["badassrate"]))

    register_command("Fun", "badassrate", "Badass level rate 0-100%")

    # 68. COOCRATE
    @app.on_message(filters.command("coocrate", prefixes=".") & filters.me)
    async def coocrate_cmd(client, message):
        target = _get_target_name(message)
        await message.edit(_make_rating_message(target, "coocrate", _RATING_LABELS["coocrate"], _RATING_EMOJIS["coocrate"]))

    register_command("Fun", "coocrate", "Clown rate 0-100%")

    # 69. STANKRATE / STR
    @app.on_message(filters.command(["stankrate", "str"], prefixes=".") & filters.me)
    async def stankrate_cmd(client, message):
        target = _get_target_name(message)
        await message.edit(_make_rating_message(target, "stankrate", _RATING_LABELS["stankrate"], _RATING_EMOJIS["stankrate"]))

    register_command("Fun", "stankrate", "Stank level rate 0-100%", aliases=["str"])

    # 70. WAIFURATE
    @app.on_message(filters.command("waifurate", prefixes=".") & filters.me)
    async def waifurate_cmd(client, message):
        target = _get_target_name(message)
        await message.edit(_make_rating_message(target, "waifurate", _RATING_LABELS["waifurate"], _RATING_EMOJIS["waifurate"]))

    register_command("Fun", "waifurate", "Waifu material rate 0-100%")

    # 71. SMOOTHRATE
    @app.on_message(filters.command("smoothrate", prefixes=".") & filters.me)
    async def smoothrate_cmd(client, message):
        target = _get_target_name(message)
        await message.edit(_make_rating_message(target, "smoothrate", _RATING_LABELS["smoothrate"], _RATING_EMOJIS["smoothrate"]))

    register_command("Fun", "smoothrate", "Smoothness rate 0-100%")

    # 72. CRINGRATE
    @app.on_message(filters.command("cringrate", prefixes=".") & filters.me)
    async def cringrate_cmd(client, message):
        target = _get_target_name(message)
        await message.edit(_make_rating_message(target, "cringrate", _RATING_LABELS["cringrate"], _RATING_EMOJIS["cringrate"]))

    register_command("Fun", "cringrate", "Cringe level rate 0-100%")

    # ═══════════════════════════════════════════════════════════════
    #  GENERATORS (22 commands)
    # ═══════════════════════════════════════════════════════════════

    # 73. EXCUSE
    @app.on_message(filters.command("excuse", prefixes=".") & filters.me)
    async def excuse_cmd(client, message):
        await message.edit(f"🤥 **Excuse:** {random.choice(_EXCUSES)}")

    register_command("Fun", "excuse", "Generate a random excuse")

    # 74. ALIBI
    @app.on_message(filters.command("alibi", prefixes=".") & filters.me)
    async def alibi_cmd(client, message):
        await message.edit(f"🕵️ **Alibi:** {random.choice(_ALIBIS)}")

    register_command("Fun", "alibi", "Generate a random alibi")

    # 75. FORTUNE
    @app.on_message(filters.command("fortune", prefixes=".") & filters.me)
    async def fortune_cmd(client, message):
        await message.edit(f"🔮 **Fortune:** {random.choice(_FORTUNES)}")

    register_command("Fun", "fortune", "Random fortune cookie message")

    # 76. HOROSCOPE
    @app.on_message(filters.command("horoscope", prefixes=".") & filters.me)
    async def horoscope_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) > 1:
            sign = args[1].strip().lower()
            if sign in _HOROSCOPES:
                await message.edit(_HOROSCOPES[sign])
            else:
                signs_list = ", ".join(s.title() for s in _HOROSCOPES.keys())
                await message.edit(f"❌ Unknown sign. Available: {signs_list}")
        else:
            sign = random.choice(list(_HOROSCOPES.keys()))
            await message.edit(_HOROSCOPES[sign])

    register_command("Fun", "horoscope", "Daily horoscope for your sign")

    # 77. ZODIAC
    @app.on_message(filters.command("zodiac", prefixes=".") & filters.me)
    async def zodiac_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) > 1:
            query = args[1].strip().lower()
            for name, emoji, dates, element in _ZODIAC_SIGNS:
                if query == name.lower():
                    await message.edit(
                        f"{emoji} **{name}**\n📅 {dates}\n🌊 Element: {element}"
                    )
                    return
            await message.edit("❌ Sign not found. Try the full name like `aries` or `leo`.")
        else:
            name, emoji, dates, element = random.choice(_ZODIAC_SIGNS)
            await message.edit(f"{emoji} **{name}**\n📅 {dates}\n🌊 Element: {element}")

    register_command("Fun", "zodiac", "Show zodiac sign info")

    # 78. TAROT
    @app.on_message(filters.command("tarot", prefixes=".") & filters.me)
    async def tarot_cmd(client, message):
        name, emoji, meaning = random.choice(_TAROT_CARDS)
        orientation = random.choice(["⬆️ Upright", "⬇️ Reversed"])
        await message.edit(
            f"🃏 **Tarot Card:** {emoji} {name}\n"
            f"🔄 **Orientation:** {orientation}\n"
            f"📖 **Meaning:** {meaning}"
        )

    register_command("Fun", "tarot", "Draw a random tarot card")

    # 79. CRYSTALBALL
    @app.on_message(filters.command("crystalball", prefixes=".") & filters.me)
    async def crystalball_cmd(client, message):
        await message.edit(f"🔮 **Crystal Ball:** {random.choice(_CRYSTALBALL)}")

    register_command("Fun", "crystalball", "Crystal ball prediction")

    # 80. OUIJA
    @app.on_message(filters.command("ouija", prefixes=".") & filters.me)
    async def ouija_cmd(client, message):
        args = message.text.split(None, 1)
        question = args[1] if len(args) > 1 else "..."
        answer = random.choice(_OUIJA)
        await message.edit(f"👻 **Ouija Board**\n\n❓ {question}\n\n🅰️ {answer}")

    register_command("Fun", "ouija", "Ouija board response")

    # 81. MOOD
    @app.on_message(filters.command("mood", prefixes=".") & filters.me)
    async def mood_cmd(client, message):
        await message.edit(f"🎭 **Mood:** {random.choice(_MOODS)}")

    register_command("Fun", "mood", "Random mood descriptor")

    # 82. PERSONALITY
    @app.on_message(filters.command("personality", prefixes=".") & filters.me)
    async def personality_cmd(client, message):
        target = _get_target_name(message)
        p = random.choice(_PERSONALITIES)
        await message.edit(f"🔮 **Personality for {target}:**\n\n{p}")

    register_command("Fun", "personality", "Random personality type")

    # 83. SPIRITANIMAL
    @app.on_message(filters.command("spiritanimal", prefixes=".") & filters.me)
    async def spiritanimal_cmd(client, message):
        target = _get_target_name(message)
        animal = random.choice(_SPIRIT_ANIMALS)
        await message.edit(f"🐾 **Spirit Animal for {target}:**\n\n{animal}")

    register_command("Fun", "spiritanimal", "Discover your spirit animal")

    # 84. SUPERPOWER
    @app.on_message(filters.command("superpower", prefixes=".") & filters.me)
    async def superpower_cmd(client, message):
        target = _get_target_name(message)
        power = random.choice(_SUPERPOWERS)
        await message.edit(f"⚡ **Superpower for {target}:**\n\n{power}")

    register_command("Fun", "superpower", "Random superpower assignment")

    # 85. WEAPON
    @app.on_message(filters.command("weapon", prefixes=".") & filters.me)
    async def weapon_cmd(client, message):
        target = _get_target_name(message)
        weapon = random.choice(_WEAPONS)
        await message.edit(f"⚔️ **Weapon for {target}:**\n\n{weapon}")

    register_command("Fun", "weapon", "Random RPG weapon assignment")

    # 86. CLASS
    @app.on_message(filters.command("class", prefixes=".") & filters.me)
    async def class_cmd(client, message):
        target = _get_target_name(message)
        cls = random.choice(_RPG_CLASSES)
        await message.edit(f"🎮 **RPG Class for {target}:**\n\n{cls}")

    register_command("Fun", "class", "Random RPG class assignment")

    # 87. ALIGNMENT
    @app.on_message(filters.command("alignment", prefixes=".") & filters.me)
    async def alignment_cmd(client, message):
        target = _get_target_name(message)
        align = random.choice(_ALIGNMENTS)
        await message.edit(f"⚖️ **Alignment for {target}:**\n\n{align}")

    register_command("Fun", "alignment", "Random D&D alignment")

    # 88. STATS
    @app.on_message(filters.command("stats", prefixes=".") & filters.me)
    async def stats_cmd(client, message):
        target = _get_target_name(message)
        stats = {
            "STR": random.randint(3, 20),
            "DEX": random.randint(3, 20),
            "CON": random.randint(3, 20),
            "INT": random.randint(3, 20),
            "WIS": random.randint(3, 20),
            "CHA": random.randint(3, 20),
        }
        stat_lines = "\n".join(f"  **{k}:** `{v}` {'█' * v}{'░' * (20-v)}" for k, v in stats.items())
        total = sum(stats.values())
        modifier = "positive" if total >= 72 else "neutral" if total >= 54 else "negative"
        await message.edit(
            f"📊 **RPG Stats for {target}:**\n\n{stat_lines}\n\n"
            f"🎯 **Total:** `{total}` / 120 — *{modifier} modifier*"
        )

    register_command("Fun", "stats", "Generate RPG character stats")

    # 89. PROPHECY
    @app.on_message(filters.command("prophecy", prefixes=".") & filters.me)
    async def prophecy_cmd(client, message):
        await message.edit(f"📜 **Prophecy:** {random.choice(_PROPHECIES)}")

    register_command("Fun", "prophecy", "Random mystical prophecy")

    # 90. FAKECHAT
    @app.on_message(filters.command("fakechat", prefixes=".") & filters.me)
    async def fakechat_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.fakechat Name: message`")
            return
        text = args[1].strip()
        if ":" in text:
            name, msg = text.split(":", 1)
        else:
            name, msg = "Unknown", text
        timestamp = time.strftime("%H:%M")
        fake = (
            f"┌─────────────────────┐\n"
            f"│ 💬 **{name.strip()}**  {timestamp}   │\n"
            f"├─────────────────────┤\n"
            f"│ {msg.strip()[:40]}{'...' if len(msg.strip()) > 40 else ''}│\n"
            f"└─────────────────────┘"
        )
        await message.edit(fake)

    register_command("Fun", "fakechat", "Generate a fake chat message")

    # 91. WANTED
    @app.on_message(filters.command("wanted", prefixes=".") & filters.me)
    async def wanted_cmd(client, message):
        target = _get_target_name(message)
        bounty = random.randint(1000, 9999999)
        crimes = [
            "Excessive meme sharing", "Criminal amounts of rizz",
            "Illegal levels of cuteness", "Grand theft WiFi",
            "Unlawful procrastination", "Reckless emoji usage",
            "Conspiracy to be adorable", "First-degree sass",
            "Felony cringe", "Aggressive wholesomeness",
        ]
        crime = random.choice(crimes)
        await message.edit(
            f"🤠 **WANTED: DEAD OR ALIVE** 🤠\n\n"
            f"👤 **Name:** {target}\n"
            f"💰 **Bounty:** ${bounty:,}\n"
            f"⚖️ **Crime:** {crime}\n\n"
            f"_" * 25
        )

    register_command("Fun", "wanted", "Generate a wanted poster")

    # 92. COLOR
    @app.on_message(filters.command("color", prefixes=".") & filters.me)
    async def color_cmd(client, message):
        hex_color = ''.join(random.choices('0123456789ABCDEF', k=6))
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        await message.edit(
            f"🎨 **Random Color:**\n\n"
            f"🟥 **HEX:** `#{hex_color}`\n"
            f"🟩 **RGB:** `rgb({r}, {g}, {b})`\n"
            f"🟦 **Integer:** `{int(hex_color, 16)}`"
        )

    register_command("Fun", "color", "Generate a random color")

    # 93. EMOJI
    @app.on_message(filters.command("emoji", prefixes=".") & filters.me)
    async def emoji_cmd(client, message):
        count = 3
        args = message.text.split(None, 1)
        if len(args) > 1:
            try:
                count = min(int(args[1].strip()), 10)
                if count < 1:
                    count = 3
            except ValueError:
                count = 3
        emojis = "".join(random.choices(_EMOJI_LIST, k=count))
        await message.edit(f"🎲 **Random Emoji:** {emojis}")

    register_command("Fun", "emoji", "Get random emoji(s)")

    # 94. PASSWORD
    @app.on_message(filters.command("password", prefixes=".") & filters.me)
    async def password_cmd(client, message):
        adj = random.choice(_PASSWORD_ADJS)
        noun = random.choice(_PASSWORD_NOUNS)
        num = random.randint(10, 99)
        special = random.choice("!@#$%^&*")
        word_pass = f"{adj}{noun}{num}{special}"
        char_pass = ''.join(random.choices(
            string.ascii_letters + string.digits + string.punctuation, k=16
        ))
        await message.edit(
            f"🔐 **Generated Passwords:**\n\n"
            f"🔤 **Memorable:** `{word_pass}`\n"
            f"🔀 **Random:** `{char_pass}`"
        )

    register_command("Fun", "password", "Generate random passwords")

    # ═══════════════════════════════════════════════════════════════
    #  TEXT FUN (26 commands)
    # ═══════════════════════════════════════════════════════════════

    # 95. ASCIIART / AA
    @app.on_message(filters.command(["asciiart", "aa"], prefixes=".") & filters.me)
    async def asciiart_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) > 1:
            key = args[1].strip().lower()
            if key in _ASCII_ARTS:
                await message.edit(f"```\n{_ASCII_ARTS[key]}\n```")
            else:
                available = ", ".join(sorted(_ASCII_ARTS.keys()))
                await message.edit(f"❌ Not found. Available: {available}")
        else:
            key = random.choice(list(_ASCII_ARTS.keys()))
            await message.edit(f"```\n{_ASCII_ARTS[key]}\n```\n_{key}_")

    register_command("Fun", "asciiart", "ASCII art (cat, dog, bear, etc.)", aliases=["aa"])

    # 96. COWSAY
    @app.on_message(filters.command("cowsay", prefixes=".") & filters.me)
    async def cowsay_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.cowsay <text>`")
            return
        text = args[1].strip()
        border_len = len(text) + 2
        top = " " + "_" * border_len
        mid = f"< {text} >"
        bot = " " + "-" * border_len
        cow = (
            f"```\n{top}\n{mid}\n{bot}\n"
            f"        \\   ^__^\n"
            f"         \\  (oo)\\_______\n"
            f"            (__)\\       )\\/\\\n"
            f"                ||----w |\n"
            f"                ||     ||\n```"
        )
        await message.edit(cow)

    register_command("Fun", "cowsay", "Cowsay text")

    # 97. UWU
    @app.on_message(filters.command("uwu", prefixes=".") & filters.me)
    async def uwu_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.uwu <text>`")
            return
        text = args[1]
        text = text.replace("r", "w").replace("l", "w")
        text = text.replace("R", "W").replace("L", "W")
        text = text.replace("no", "nuwu").replace("No", "Nuwu")
        text = text.replace("ove", "uv").replace("Ove", "Uv")
        await message.edit(f"💕 {text} uwu~")

    register_command("Fun", "uwu", "UwU-ify your text")

    # 98. OWO
    @app.on_message(filters.command("owo", prefixes=".") & filters.me)
    async def owo_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.owo <text>`")
            return
        text = args[1]
        text = text.replace("r", "w").replace("l", "w")
        text = text.replace("R", "W").replace("L", "W")
        faces = ["OwO", "UwU", ">w<", "^w^", "ÒwÓ", "♥w♥", ">w<", "~w~"]
        text = text + " " + random.choice(faces)
        await message.edit(text)

    register_command("Fun", "owo", "OwO-ify your text")

    # 99. REVERSE / REV
    @app.on_message(filters.command(["reverse", "rev"], prefixes=".") & filters.me)
    async def reverse_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.reverse <text>`")
            return
        await message.edit(f"🔄 {args[1][::-1]}")

    register_command("Fun", "reverse", "Reverse text", aliases=["rev"])

    # 100. MOCK
    @app.on_message(filters.command("mock", prefixes=".") & filters.me)
    async def mock_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.mock <text>`")
            return
        text = args[1]
        mocked = ""
        upper = True
        for ch in text:
            if ch.isalpha():
                mocked += ch.upper() if upper else ch.lower()
                upper = not upper
            else:
                mocked += ch
        await message.edit(f"🤡 {mocked}")

    register_command("Fun", "mock", "MoCkInG tExT")

    # 101. CLAP
    @app.on_message(filters.command("clap", prefixes=".") & filters.me)
    async def clap_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.clap <text>`")
            return
        words = args[1].split()
        await message.edit(" 👏 ".join(words))

    register_command("Fun", "clap", "Add clap emojis between words")

    # 102. SPACE
    @app.on_message(filters.command("space", prefixes=".") & filters.me)
    async def space_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.space <text>`")
            return
        spaced = " ".join(args[1])
        await message.edit(spaced)

    register_command("Fun", "space", "Add spaces between each character")

    # 103. SCRAMBLE
    @app.on_message(filters.command("scramble", prefixes=".") & filters.me)
    async def scramble_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.scramble <text>`")
            return
        chars = list(args[1])
        random.shuffle(chars)
        await message.edit(f"🔀 {''.join(chars)}")

    register_command("Fun", "scramble", "Scramble text characters")

    # 104. GIBBERISH
    @app.on_message(filters.command("gibberish", prefixes=".") & filters.me)
    async def gibberish_cmd(client, message):
        syllables = [
            "ba", "bi", "bo", "da", "de", "di", "fa", "fi", "ga", "gi",
            "ha", "hi", "ka", "ki", "la", "li", "ma", "mi", "na", "ni",
            "pa", "pi", "ra", "ri", "sa", "si", "ta", "ti", "wa", "wi",
            "za", "zi", "zu", "fu", "mo", "nu", "shu", "cha", "cho", "kha",
        ]
        word_count = random.randint(3, 8)
        words = []
        for _ in range(word_count):
            syllable_count = random.randint(1, 4)
            word = "".join(random.choice(syllables) for _ in range(syllable_count))
            words.append(word)
        await message.edit(f"🤪 {' '.join(words)}")

    register_command("Fun", "gibberish", "Generate random gibberish")

    # 105. UPSIDE
    @app.on_message(filters.command("upside", prefixes=".") & filters.me)
    async def upside_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.upside <text>`")
            return
        flip_map = {
            'a': 'ɐ', 'b': 'q', 'c': 'ɔ', 'd': 'p', 'e': 'ǝ', 'f': 'ɟ',
            'g': 'ƃ', 'h': 'ɥ', 'i': 'ᴉ', 'j': 'ɾ', 'k': 'ʞ', 'l': 'l',
            'm': 'ɯ', 'n': 'u', 'o': 'o', 'p': 'd', 'q': 'b', 'r': 'ɹ',
            's': 's', 't': 'ʇ', 'u': 'n', 'v': 'ʌ', 'w': 'ʍ', 'x': 'x',
            'y': 'ʎ', 'z': 'z', 'A': '∀', 'B': 'q', 'C': 'Ɔ', 'D': 'p',
            'E': 'Ǝ', 'F': 'Ⅎ', 'G': '⅁', 'H': 'H', 'I': 'I', 'J': 'ſ',
            'K': 'ʞ', 'L': '˥', 'M': 'W', 'N': 'N', 'O': 'O', 'P': 'Ԁ',
            'Q': 'Ɔ', 'R': 'ɹ', 'S': 'S', 'T': '⊥', 'U': '∩', 'V': 'Λ',
            'W': 'M', 'X': 'X', 'Y': '⅄', 'Z': 'Z', '?': '¿', '!': '¡',
            '.': '˙', ',': "'", "'": ',', '(': ')', ')': '(', '[': ']',
            ']': '[', '{': '}', '}': '{', '<': '>', '>': '<', '&': '⅋',
            '1': 'Ɩ', '2': 'ᄅ', '3': 'Ɛ', '4': 'ㄣ', '5': 'ϛ', '6': '9',
            '7': 'ㄥ', '8': '8', '9': '6', '0': '0',
        }
        result = ""
        for ch in reversed(args[1]):
            result += flip_map.get(ch, ch)
        await message.edit(f"🔄 {result}")

    register_command("Fun", "upside", "Flip text upside down")

    # 106. STRIKE
    @app.on_message(filters.command("strike", prefixes=".") & filters.me)
    async def strike_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.strike <text>`")
            return
        struck = "".join(ch + "\u0336" for ch in args[1])
        await message.edit(struck)

    register_command("Fun", "strike", "Add strikethrough to text")

    # 107. UNDERLINE
    @app.on_message(filters.command("underline", prefixes=".") & filters.me)
    async def underline_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.underline <text>`")
            return
        underlined = "".join(ch + "\u0332" for ch in args[1])
        await message.edit(underlined)

    register_command("Fun", "underline", "Add underline to text")

    # 108. REGIONAL
    @app.on_message(filters.command("regional", prefixes=".") & filters.me)
    async def regional_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.regional <text>`")
            return
        result = ""
        for ch in args[1].lower():
            result += _REGIONAL_MAP.get(ch, ch)
        await message.edit(result)

    register_command("Fun", "regional", "Convert text to regional indicator emojis")

    # 109. BRAILLE
    @app.on_message(filters.command("braille", prefixes=".") & filters.me)
    async def braille_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.braille <text>`")
            return
        result = ""
        for ch in args[1].lower():
            result += _BRAILLE_MAP.get(ch, ch)
        await message.edit(f"⠿ {result}")

    register_command("Fun", "braille", "Convert text to braille characters")

    # 110. MORSE
    @app.on_message(filters.command("morse", prefixes=".") & filters.me)
    async def morse_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.morse <text>`")
            return
        result = []
        for ch in args[1].upper():
            if ch in _MORSE:
                result.append(_MORSE[ch])
            else:
                result.append(ch)
        await message.edit(f"📡 {'   '.join(result)}")

    register_command("Fun", "morse", "Convert text to Morse code")

    # 111. BINARY
    @app.on_message(filters.command("binary", prefixes=".") & filters.me)
    async def binary_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.binary <text>`")
            return
        result = " ".join(format(ord(ch), '08b') for ch in args[1])
        await message.edit(f"💻 {result}")

    register_command("Fun", "binary", "Convert text to binary")

    # 112. FANCY
    @app.on_message(filters.command("fancy", prefixes=".") & filters.me)
    async def fancy_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.fancy <text>`")
            return
        result = ""
        for ch in args[1].lower():
            if ch in _FANCY_MAP:
                result += _FANCY_MAP[ch]
            else:
                result += ch
        await message.edit(f"✨ {result}")

    register_command("Fun", "fancy", "Convert text to fancy Unicode")

    # 113. SMALL
    @app.on_message(filters.command("small", prefixes=".") & filters.me)
    async def small_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.small <text>`")
            return
        result = ""
        for ch in args[1].lower():
            if ch in _SMALL_MAP:
                result += _SMALL_MAP[ch]
            else:
                result += ch
        await message.edit(result)

    register_command("Fun", "small", "Convert text to superscript small")

    # 114. DOUBLETEXT
    @app.on_message(filters.command("doubletext", prefixes=".") & filters.me)
    async def doubletext_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.doubletext <text>`")
            return
        result = ""
        for ch in args[1]:
            result += ch + ch
        await message.edit(result)

    register_command("Fun", "doubletext", "Double each character in text")

    # 115. BOX
    @app.on_message(filters.command("box", prefixes=".") & filters.me)
    async def box_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.box <text>`")
            return
        text = args[1].strip()
        width = max(len(text) + 4, 6)
        top = "╔" + "═" * width + "╗"
        mid = f"║  {text}  ║"
        pad = width - len(text) - 4
        if pad > 0:
            mid = f"║  {text}{' ' * pad}  ║"
        bot = "╚" + "═" * width + "╝"
        await message.edit(f"```\n{top}\n{mid}\n{bot}\n```")

    register_command("Fun", "box", "Put text in a box")

    # 116. STARWRAP
    @app.on_message(filters.command("starwrap", prefixes=".") & filters.me)
    async def starwrap_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.starwrap <text>`")
            return
        text = args[1].strip()
        await message.edit(f"✨ {text} ✨")

    register_command("Fun", "starwrap", "Wrap text with stars")

    # 117. DOTWRAP
    @app.on_message(filters.command("dotwrap", prefixes=".") & filters.me)
    async def dotwrap_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.dotwrap <text>`")
            return
        text = args[1].strip()
        await message.edit(f"• {text} •")

    register_command("Fun", "dotwrap", "Wrap text with dots")

    # 118. ZALGO
    @app.on_message(filters.command("zalgo", prefixes=".") & filters.me)
    async def zalgo_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.zalgo <text>`")
            return
        result = ""
        for ch in args[1]:
            result += ch
            if ch.isalpha():
                for _ in range(random.randint(1, 3)):
                    result += random.choice(_ZALGO_ABOVE)
                for _ in range(random.randint(1, 2)):
                    result += random.choice(_ZALGO_BELOW)
        await message.edit(result)

    register_command("Fun", "zalgo", "Z̸̧a̵l̶g̷o̶-ify text")

    # 119. EXPAND
    @app.on_message(filters.command("expand", prefixes=".") & filters.me)
    async def expand_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.expand <text>`")
            return
        result = ""
        for i, ch in enumerate(args[1]):
            if ch.isalpha():
                result += ch.upper() if i == 0 or not args[1][i-1].isalpha() else ch.lower()
                result += " " * min(i, 8)
            else:
                result += ch
        await message.edit(result)

    register_command("Fun", "expand", "E x p a n d text with spaces")

    # 120. SHRINK
    @app.on_message(filters.command("shrink", prefixes=".") & filters.me)
    async def shrink_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.shrink <text>`")
            return
        # Remove vowels and extra spaces to shrink text
        vowels = "aeiouAEIOU"
        result = "".join(ch for ch in args[1] if ch not in vowels or ch == ' ')
        result = " ".join(result.split())  # collapse multiple spaces
        if not result.strip():
            result = args[1]  # fallback if everything was a vowel
        await message.edit(f"🔬 {result}")

    register_command("Fun", "shrink", "Shrink text by removing vowels")

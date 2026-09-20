"""
KyrenUB - Naughty Plugin
=========================
83 commands for roasts, flirting, ratings, generators, and interactive fun.
Categories: Roasts(20), Flirt(15), Ratings(16), Generators(15), Interactive(17)
"""


def register(app):
    from pyrogram import filters
    from plugins import register_command
    import random
    import hashlib

    # ═══════════════════════════════════════════════════════════════
    #  SHARED HELPERS
    # ═══════════════════════════════════════════════════════════════

    def _get_target_name(client, message):
        """Get target user's first name from reply or arg."""
        if message.reply_to_message:
            u = message.reply_to_message.from_user
            return u.first_name if u else "Someone"
        return "You"

    def _deterministic_score(name, key, salt=""):
        """Hash-based deterministic 0-100 score."""
        h = hashlib.sha256(f"{name}{key}{salt}".encode()).hexdigest()
        return int(h[:8], 16) % 101

    def _progress_bar(pct, length=20):
        """Return a text progress bar."""
        filled = int(length * pct / 100)
        return "█" * filled + "░" * (length - filled)

    # ═══════════════════════════════════════════════════════════════
    #  ROASTS DATA (20 commands)
    # ═══════════════════════════════════════════════════════════════

    _ROASTS = [
        "You're like a cloud. When you disappear, it's a beautiful day.",
        "I'd agree with you but then we'd both be wrong.",
        "You're not the dumbest person on the planet, but you better hope they don't die.",
        "I'd explain it to you, but I left my crayons at home.",
        "You bring everyone so much joy when you leave the room.",
        "Somewhere out there, a village is missing its idiot.",
        "You're proof that evolution can go in reverse.",
        "Your brain is like a stadium — huge and completely empty.",
        "If ignorance is bliss, you must be the happiest person alive.",
        "You're the reason the gene pool needs a lifeguard.",
        "I'd call you a tool, but that would be an insult to tools.",
        "You're about as useful as a screen door on a submarine.",
        "I'm not saying you're stupid, I'm just saying you have bad luck thinking.",
        "You're the human equivalent of a participation trophy.",
        "I'd roast you, but my mom said not to burn trash.",
        "You have the perfect face for radio.",
        "If you were any slower, you'd be going backwards.",
        "Your personality is like a dial-up connection — slow and nobody wants it.",
        "I'd tell you to go outside, but you'd probably get lost.",
        "You're like a broken pencil — completely pointless.",
        "I've seen more personality in a cup of tap water.",
        "You're not lazy, you're just on energy-saving mode. Permanently.",
        "If you were a spice, you'd be flour.",
        "You're the reason instructions come with warnings.",
        "I'd challenge you to a battle of wits, but I see you're unarmed.",
        "Your opinion is like a penny — not worth picking up.",
        "You're like a software update — nobody wants you and you always show up at the worst time.",
        "I'm jealous of people who don't know you.",
        "You're the punchline to a joke nobody told.",
        "If brains were dynamite, you wouldn't have enough to blow your nose.",
        "You're as useful as an ashtray on a motorcycle.",
        "I'd tell you how I really feel, but I don't think your confidence could handle it.",
        "You're like a flat tire — annoying and completely deflating.",
    ]

    _BURNS = [
        "You look like something I'd draw with my left hand.",
        "I'm not saying you're ugly, but Halloween is your time to shine.",
        "You're so dense, light bends around you.",
        "I've seen better faces on a clock, and at least they have two hands.",
        "You're the reason autocorrect was invented.",
        "Your face could make an onion cry.",
        "I'd call you a joke, but at least jokes are funny.",
        "If you were any flatter, you'd be a 2D character.",
        "Your fashion sense is like a typo — everyone notices but nobody says anything.",
        "You have the charisma of a damp sock.",
        "I've seen better personalities on a mannequin.",
        "You're the reason people move to a different checkout line.",
        "If ugly was a crime, you'd get the death penalty.",
        "You're like a VPN — slow, unwanted, and always buffering.",
        "Your reflection apologizes to the mirror.",
        "I'd tell you to take a hike, but even nature doesn't deserve that.",
        "You're the person who puts the 'fun' in funeral.",
        "Your style is like a participation medal — barely there.",
        "I've seen better-looking things in a lost-and-found box.",
        "You're like a pop-up ad — nobody wants you around and you're impossible to close.",
        "If looks could kill, you'd be a mild headache.",
    ]

    _SAVAGES = [
        "You're not just a disappointment, you're the whole parade.",
        "I'd unsult you, but nature already did a better job.",
        "You're the reason shampoo has instructions.",
        "Your existence is a loading screen that never finishes.",
        "I'd tell you to have a good day, but you'd mess that up too.",
        "You're a real-life example of why some animals eat their young.",
        "If stupid was a sport, you'd be in the Hall of Fame.",
        "You're not the sharpest tool in the shed — you're not even in the shed.",
        "I'd say you're underwhelming, but that would be overwhelming for you.",
        "You're proof that not every egg deserves to hatch.",
        "Your birth certificate is an apology letter from the hospital.",
        "You're the reason the warning label exists.",
        "If you were a hot dog, you'd be the bun nobody wants.",
        "You're the reason your parents always say 'we can always try again.'",
        "I'd give you a nasty look, but you already have one.",
        "You're like a spoiler — nobody asked for you and you ruin everything.",
    ]

    _INSULTS = [
        "Your face is just fine. It's your personality that needs a makeover.",
        "You're like a marshmallow — soft, squishy, and nobody takes you seriously.",
        "I'd insult you, but I don't want to make your life harder than it already is.",
        "You have the personality of a speed bump.",
        "If I wanted to hear from you, I'd shake my piggy bank.",
        "You're as pleasant as a toothache.",
        "I'd tell you to go play in traffic, but I don't want to be responsible for the accidents.",
        "Your sense of style is like a GPS with no signal — completely lost.",
        "You're the reason your teacher considered early retirement.",
        "You're as charming as a colonoscopy.",
        "Your personality is like a blank coloring book — empty and not fun.",
        "I'd call you basic, but that would be an upgrade.",
        "You're like a mosquito — annoying, unwanted, and you always show up.",
        "If mediocrity was an Olympic sport, you'd be on the podium.",
        "You're as useful as a chocolate teapot.",
        "I'd ask for your opinion, but I'd rather not waste the silence.",
        "Your presence is like a pop quiz — nobody wants it and it ruins the day.",
        "You're the reason the 'mute' button was invented.",
        "I'd say you're a waste of space, but even space doesn't want you.",
        "You're like a rerun of a bad show — nobody asked for you and you're still here.",
        "If awkward was currency, you'd be a billionaire.",
    ]

    _DESTROYS = [
        "I didn't know they stacked stupidity that high.",
        "You're not even worth the calories it takes to type this.",
        "Your entire existence is a 404 error.",
        "I'd say you're irrelevant, but irrelevant things at least have context.",
        "You make a rubber chicken look dignified.",
        "You're the reason 'idiot-proofing' exists — and it still doesn't work on you.",
        "Your intelligence is like a candle in a hurricane — nonexistent.",
        "I've seen more personality in a bowl of oatmeal.",
        "You're the kind of person who brings a knife to a nerf fight and still loses.",
        "If I threw a rock at you, the rock would apologize for hitting something so sad.",
        "Your existence is a bug report that never got fixed.",
        "You're a walking advertisement for staying in school.",
        "I'd call you a clown, but clowns are paid to be funny.",
        "You're the reason your ancestors invented facepalming.",
        "Your personality is like a default setting — boring and everyone's seen it before.",
    ]

    _DEMOLISHES = [
        "You're the kind of person who reads the terms and conditions and still clicks 'decline' by accident.",
        "I'd say you fell from the ugly tree, but you clearly hit every branch on the way up.",
        "You're like a participation award — technically you exist, but nobody cares.",
        "If dumb was dirt, you'd be the Grand Canyon.",
        "Your brain cells are like an endangered species — critically low and declining.",
        "You're the reason AI thinks humans are a lost cause.",
        "I'd call you a waste of oxygen, but even oxygen doesn't want to be near you.",
        "You're the error message of the human race.",
        "Your personality is a 403 Forbidden — nobody's allowed in and nobody wants to be.",
        "I'd tell you to get a life, but the queue is too long.",
        "You're the reason they put 'Do Not Eat' on silica gel packets.",
        "If you were a stock, you'd be in freefall with no floor in sight.",
        "Your confidence is a glitch — it has no basis in reality.",
        "You're a demo version of a person — limited features and nobody buys the full thing.",
        "I'd say you hit rock bottom, but you brought a shovel.",
    ]

    _WRECKS = [
        "You got wrecked harder than a phone screen on concrete.",
        "That's a wreck so bad even the tow truck drove past.",
        "Wrecked. Like a shopping cart in a parking lot.",
        "You've been wrecked like a sandcastle at high tide.",
        "Total wreck. Like a car after a crash test.",
        "Wrecked so hard your ancestors felt it.",
        "That wreck was louder than your morning alarm.",
        "Wrecked like a piñata at a birthday party.",
        "You're wrecked like a typo in a dictionary.",
        "Wrecked so thoroughly they'll study this in schools.",
        "Wrecked. Call a construction crew, there's nothing left.",
    ]

    _TRASHES = [
        "You belong in the recycling bin — nobody wants you twice.",
        "You're the trash that even raccoons reject.",
        "Trash day was yesterday, how are you still here?",
        "You're the kind of trash that makes the landfill look better.",
        "Even the garbage disposal says 'no thanks.'",
        "You're not even premium trash — you're the clearance bin.",
        "The dumpster called — it wants its dignity back.",
        "You're the coffee grounds of personalities — used up and discarded.",
        "Even the compost pile rejected you for being too toxic.",
        "You're the junk mail of the human race.",
        "The trash can has higher standards than you think.",
    ]

    _ROASTMES = [
        "I asked for a roast and even the oven said 'too easy.'",
        "Roasting myself is like shooting fish in a barrel — if the fish were already dead.",
        "I'm the kind of person who trips on flat surfaces.",
        "I put the 'pro' in procrastination.",
        "My life is a blooper reel that never made the final cut.",
        "I'm the reason they invented the 'undo' button.",
        "Even my shadow leaves me when things get dark.",
        "I'm a limited edition — limited talent, limited appeal.",
        "I'm like a Wi-Fi signal — weak and always dropping.",
        "I'd roast myself but my life already did that for free.",
        "My bank account roasts me harder than anyone ever could.",
    ]

    _SELFBURNS = [
        "I'd set myself on fire, but I'm already getting burned by my own life choices.",
        "My reflection looks at me and says 'I can do better.'",
        "I'm the reason my own alarm clock hits snooze.",
        "Even my own shadow tries to walk away from me.",
        "I'm like a broken clock — only right twice a day, and that's generous.",
        "My confidence called — it's filing for bankruptcy.",
        "I'm my own worst critic, and honestly, I'm too kind.",
        "I'd challenge myself to a duel, but I'd lose.",
        "My own phone autocorrects my name to 'disappointment.'",
        "I looked in the mirror and the mirror cracked — from pity.",
        "Even my GPS says 'rerouting' when I try to find myself.",
    ]

    _ETHERS = [
        "You just got ethered — dissolved into nothing.",
        "That ether hit harder than a chemistry exam.",
        "Ethered so fast you didn't even see it coming.",
        "You've been ethered like a ghost in the machine.",
        "That ether was so pure it belongs in a lab.",
        "Ethered — poof, gone, like you never existed.",
        "You got ethered and the periodic table felt it.",
        "Ethered so hard you changed states of matter.",
        "That ether left nothing but vapors.",
        "You've been ethered — reduced to your base elements.",
        "Ethered. Your molecular structure has been dismantled.",
    ]

    _CLAPBACKS = [
        "I'd clap back, but my hands are too busy covering my ears from your nonsense.",
        "That wasn't even worth a clap back — more like a slow blink.",
        "Clap back delivered. You may now resume being irrelevant.",
        "I clap back so hard the audience gives a standing ovation.",
        "That clap back echoed through the chat.",
        "Clap back so swift you didn't even see my hands move.",
        "Consider yourself clapped back into your lane.",
        "That clap back was louder than your entire argument.",
        "Clap back complete. Please pick up your dignity on the way out.",
        "My clap back just set off a seismic event.",
        "Clap back delivered — no returns accepted.",
    ]

    _COMEBACKS = [
        "I'd make a comeback, but you're not worth the rehearsal.",
        "My comeback was so good it came with an encore.",
        "That comeback was sharper than a brand new pencil.",
        "I don't need a comeback — your argument did that for me.",
        "Comeback delivered. Track your package at 'nowhere.'",
        "My comeback is so legendary it has its own fan club.",
        "That comeback was faster than your internet connection.",
        "I've got comebacks on speed dial, and you just got the premium package.",
        "Comeback so clean it has its own hygiene certificate.",
        "That comeback was so smooth it needed its own soundtrack.",
        "Comeback complete. You may now sit down.",
    ]

    _DISS = [
        "That diss was so cold it gave the freezer frostbite.",
        "Dissed and dismissed — don't let the door hit you.",
        "You just got dissed like a bad restaurant review.",
        "That diss was cleaner than your browser history.",
        "Dissed so hard your WiFi disconnected out of sympathy.",
        "Consider yourself dissed. Tell your friends — oh wait.",
        "That diss was sharper than a samurai sword.",
        "Dissed. Your HP is now at zero.",
        "You got dissed so hard the dictionary added your name under 'owned.'",
        "That diss was so precise it came with coordinates.",
        "Dissed and delivered. No refund policy.",
    ]

    _SHADES = [
        "I don't throw shade — I provide complimentary dimming.",
        "That shade was so thick you need sunglasses indoors.",
        "Throwing shade like it's a solar eclipse.",
        "That shade was so cold it made winter jealous.",
        "I serve shade like it's happy hour — and it's always happy hour.",
        "That shade had its own UV index.",
        "Throwing shade so elegant it has a designer label.",
        "That shade was so refined it came with a wine pairing.",
        "My shade has more coverage than your insurance plan.",
        "Throwing shade so deep it has its own ecosystem.",
        "That shade was so subtle you probably missed it — like your potential.",
    ]

    _THROWSHADES = [
        "Throwing shade so hard the sun filed a complaint.",
        "That shade was so dark it created its own time zone.",
        "I throw shade like a eclipse — everyone notices.",
        "Throwing shade with the precision of a sniper.",
        "That shade came with its own SPF warning.",
        "I throw shade so professionally it's on my resume.",
        "Throwing shade like a tree in autumn — everywhere.",
        "That shade was so cold it needed a winter coat.",
        "I throw shade so well I should teach a masterclass.",
        "Throwing shade with the elegance of a sunset.",
        "That shade was so deep it reached the Earth's core.",
    ]

    _CALLOUTS = [
        "Callout complete. Your nonsense has been documented.",
        "I'm calling you out like a bingo number — and you just lost.",
        "That callout was so loud it echoed across time zones.",
        "Consider yourself called out. Your move.",
        "Callout delivered with the precision of a surgeon.",
        "That callout was so public it's trending.",
        "Calling you out like a referee — you're fouled out.",
        "That callout was so thorough it came with citations.",
        "Callout so clean it has its own insurance policy.",
        "I'm calling you out — and the echo is deafening.",
        "That callout was so clinical it needs a medical license.",
    ]

    _EXPOSES = [
        "Exposed like a bad Wi-Fi password — everyone can see right through.",
        "That exposure was so bright it needs sunglasses.",
        "Exposed. Your secrets are now public domain.",
        "That expose was more dramatic than a season finale.",
        "Consider yourself exposed like an unpatched vulnerability.",
        "Exposed like a tourist at the beach.",
        "That exposure was so complete it came with a report.",
        "Exposed — your cover has been blown to smithereens.",
        "That expose was so thorough it's admissible in court.",
        "Exposed like a fake designer bag at a flea market.",
        "That exposure was brighter than a supernova.",
    ]

    _RATIOS = [
        "Ratio + L + no one asked + stay mad.",
        "The ratio is so bad it needs its own zip code.",
        "Ratio'd. Your take was so bad it went negative.",
        "That ratio is wider than the Grand Canyon.",
        "Ratio + fell off + didn't ask + cope.",
        "You got ratio'd harder than a math textbook.",
        "The ratio speaks for itself — and it's saying 'yikes.'",
        "Ratio'd so hard your comment is now a cautionary tale.",
        "That ratio is so lopsided it changed the Earth's tilt.",
        "Ratio + touch grass + stay silent next time.",
        "You've been ratio'd. The numbers don't lie.",
    ]

    _REPLYWITHS = [
        "No. Just... no.",
        "I'm going to pretend I didn't see that.",
        "Did you actually just say that out loud?",
        "That's a bold strategy, Cotton. Let's see if it pays off.",
        "I'm not mad, I'm just disappointed.",
        "Sir, this is a Wendy's.",
        "And I took that personally.",
        "Well, that escalated quickly.",
        "There's a lot to unpack there, but I'm not a therapist.",
        "I have several questions, but I'm afraid of the answers.",
        "That's enough internet for today.",
    ]

    # ═══════════════════════════════════════════════════════════════
    #  ROASTS COMMANDS (20)
    # ═══════════════════════════════════════════════════════════════

    # 1. ROAST
    @app.on_message(filters.command("roast", prefixes=".") & filters.me)
    async def roast_cmd(client, message):
        name = _get_target_name(client, message)
        roasts = random.sample(_ROASTS, min(3, len(_ROASTS)))
        text = f"🔥 **Roasting {name}!**\n\n"
        for i, r in enumerate(roasts, 1):
            text += f"{i}. {r}\n"
        await message.edit(text)

    register_command("Naughty", "roast", "Roast someone with multiple burns", [])

    # 2. BURN
    @app.on_message(filters.command("burn", prefixes=".") & filters.me)
    async def burn_cmd(client, message):
        name = _get_target_name(client, message)
        burns = random.sample(_BURNS, min(3, len(_BURNS)))
        text = f"🔥 **Burning {name}!**\n\n"
        for i, b in enumerate(burns, 1):
            text += f"{i}. {b}\n"
        await message.edit(text)

    register_command("Naughty", "burn", "Deliver scorching burns", [])

    # 3. SAVAGE
    @app.on_message(filters.command("savage", prefixes=".") & filters.me)
    async def savage_cmd(client, message):
        name = _get_target_name(client, message)
        savages = random.sample(_SAVAGES, min(2, len(_SAVAGES)))
        text = f"💀 **Savage mode on {name}!**\n\n"
        for i, s in enumerate(savages, 1):
            text += f"{i}. {s}\n"
        await message.edit(text)

    register_command("Naughty", "savage", "Go savage on someone", [])

    # 4. INSULT
    @app.on_message(filters.command("insult", prefixes=".") & filters.me)
    async def insult_cmd(client, message):
        name = _get_target_name(client, message)
        insults = random.sample(_INSULTS, min(3, len(_INSULTS)))
        text = f"😤 **Insulting {name}!**\n\n"
        for i, ins in enumerate(insults, 1):
            text += f"{i}. {ins}\n"
        await message.edit(text)

    register_command("Naughty", "insult", "Throw creative insults", [])

    # 5. DESTROY
    @app.on_message(filters.command("destroy", prefixes=".") & filters.me)
    async def destroy_cmd(client, message):
        name = _get_target_name(client, message)
        destroys = random.sample(_DESTROYS, min(2, len(_DESTROYS)))
        text = f"💥 **Destroying {name}!**\n\n"
        for i, d in enumerate(destroys, 1):
            text += f"{i}. {d}\n"
        await message.edit(text)

    register_command("Naughty", "destroy", "Destroy someone's confidence", [])

    # 6. DEMOLISH
    @app.on_message(filters.command("demolish", prefixes=".") & filters.me)
    async def demolish_cmd(client, message):
        name = _get_target_name(client, message)
        demos = random.sample(_DEMOLISHES, min(2, len(_DEMOLISHES)))
        text = f"🏗 **Demolishing {name}!**\n\n"
        for i, d in enumerate(demos, 1):
            text += f"{i}. {d}\n"
        await message.edit(text)

    register_command("Naughty", "demolish", "Demolish someone completely", [])

    # 7. WRECK
    @app.on_message(filters.command("wreck", prefixes=".") & filters.me)
    async def wreck_cmd(client, message):
        name = _get_target_name(client, message)
        text = f"🏎 **Wrecked {name}!**\n\n{random.choice(_WRECKS)}"
        await message.edit(text)

    register_command("Naughty", "wreck", "Wreck someone", [])

    # 8. TRASH
    @app.on_message(filters.command("trash", prefixes=".") & filters.me)
    async def trash_cmd(client, message):
        name = _get_target_name(client, message)
        text = f"🗑 **Trashing {name}!**\n\n{random.choice(_TRASHES)}"
        await message.edit(text)

    register_command("Naughty", "trash", "Send someone to the trash", [])

    # 9. ROASTME
    @app.on_message(filters.command("roastme", prefixes=".") & filters.me)
    async def roastme_cmd(client, message):
        text = f"🤳 **Self-roast incoming!**\n\n{random.choice(_ROASTMES)}"
        await message.edit(text)

    register_command("Naughty", "roastme", "Roast yourself", [])

    # 10. SELFBURN
    @app.on_message(filters.command("selfburn", prefixes=".") & filters.me)
    async def selfburn_cmd(client, message):
        text = f"🔥 **Self-burn!**\n\n{random.choice(_SELFBURNS)}"
        await message.edit(text)

    register_command("Naughty", "selfburn", "Burn yourself", [])

    # 11. ETHER
    @app.on_message(filters.command("ether", prefixes=".") & filters.me)
    async def ether_cmd(client, message):
        name = _get_target_name(client, message)
        text = f"🧪 **Ethering {name}!**\n\n{random.choice(_ETHERS)}"
        await message.edit(text)

    register_command("Naughty", "ether", "Dissolve someone like ether", [])

    # 12. CLAPBACK
    @app.on_message(filters.command("clapback", prefixes=".") & filters.me)
    async def clapback_cmd(client, message):
        name = _get_target_name(client, message)
        text = f"👏 **Clapping back at {name}!**\n\n{random.choice(_CLAPBACKS)}"
        await message.edit(text)

    register_command("Naughty", "clapback", "Deliver a clapback", [])

    # 13. COMEBACK
    @app.on_message(filters.command("comeback", prefixes=".") & filters.me)
    async def comeback_cmd(client, message):
        name = _get_target_name(client, message)
        text = f"💬 **Comeback for {name}!**\n\n{random.choice(_COMEBACKS)}"
        await message.edit(text)

    register_command("Naughty", "comeback", "Serve a comeback", [])

    # 14. DIS
    @app.on_message(filters.command("dis", prefixes=".") & filters.me)
    async def dis_cmd(client, message):
        name = _get_target_name(client, message)
        text = f"🎤 **Dissing {name}!**\n\n{random.choice(_DISS)}"
        await message.edit(text)

    register_command("Naughty", "dis", "Drop a diss", [])

    # 15. SHADE
    @app.on_message(filters.command("shade", prefixes=".") & filters.me)
    async def shade_cmd(client, message):
        name = _get_target_name(client, message)
        text = f"🌤 **Throwing shade at {name}!**\n\n{random.choice(_SHADES)}"
        await message.edit(text)

    register_command("Naughty", "shade", "Throw shade", [])

    # 16. THROWSHADE
    @app.on_message(filters.command("throwshade", prefixes=".") & filters.me)
    async def throwshade_cmd(client, message):
        name = _get_target_name(client, message)
        text = f"🕶 **Throwing shade at {name}!**\n\n{random.choice(_THROWSHADES)}"
        await message.edit(text)

    register_command("Naughty", "throwshade", "Throw extra shade", [])

    # 17. CALLOUT
    @app.on_message(filters.command("callout", prefixes=".") & filters.me)
    async def callout_cmd(client, message):
        name = _get_target_name(client, message)
        text = f"📢 **Calling out {name}!**\n\n{random.choice(_CALLOUTS)}"
        await message.edit(text)

    register_command("Naughty", "callout", "Call someone out", [])

    # 18. EXPOSE
    @app.on_message(filters.command("expose", prefixes=".") & filters.me)
    async def expose_cmd(client, message):
        name = _get_target_name(client, message)
        text = f"🔎 **Exposing {name}!**\n\n{random.choice(_EXPOSES)}"
        await message.edit(text)

    register_command("Naughty", "expose", "Expose someone", [])

    # 19. RATIO
    @app.on_message(filters.command("ratio", prefixes=".") & filters.me)
    async def ratio_cmd(client, message):
        name = _get_target_name(client, message)
        text = f"📉 **Ratio'd {name}!**\n\n{random.choice(_RATIOS)}"
        await message.edit(text)

    register_command("Naughty", "ratio", "Ratio someone", [])

    # 20. REPLYWITH
    @app.on_message(filters.command("replywith", prefixes=".") & filters.me)
    async def replywith_cmd(client, message):
        text = f"💬 **Quick reply:**\n\n{random.choice(_REPLYWITHS)}"
        await message.edit(text)

    register_command("Naughty", "replywith", "Get a witty reply suggestion", [])

    # ═══════════════════════════════════════════════════════════════
    #  FLIRT DATA (15 commands)
    # ═══════════════════════════════════════════════════════════════

    _FLIRTS = [
        "Are you a magician? Because whenever I look at you, everyone else disappears.",
        "Do you have a map? Because I just got lost in your eyes.",
        "Is your name Google? Because you've got everything I've been searching for.",
        "If you were a vegetable, you'd be a cute-cumber.",
        "Are you a parking ticket? Because you've got FINE written all over you.",
        "Do you believe in love at first sight, or should I walk by again?",
        "Are you a campfire? Because you're hot and I want s'more.",
        "Is your dad a baker? Because you're a cutie pie.",
        "Are you a bank loan? Because you've got my interest.",
        "If you were a fruit, you'd be a fine-apple.",
        "Are you a dictionary? Because you add meaning to my life.",
        "Is your name Wi-Fi? Because I'm feeling a connection.",
        "Are you a snowstorm? Because you're making my heart race.",
        "Do you have a Band-Aid? Because I just scraped my knee falling for you.",
        "If beauty were time, you'd be an eternity.",
        "Are you an alien? Because you just abducted my heart.",
        "Is your name Dunkin? Because I donut want to spend another day without you.",
        "Are you a cat? Because you're purr-fect.",
        "Do you have a pencil? Because I want to erase your past and write our future.",
        "If you were a triangle, you'd be acute one.",
        "Are you a volcano? Because I lava you.",
        "Is your dad an artist? Because you're a masterpiece.",
        "Are you a shooting star? Because my wish just came true.",
        "If you were a burger at McDonald's, you'd be the McGorgeous.",
        "Are you a light switch? Because you turn me on... to the idea of getting to know you better.",
        "Is your aura made of gold? Because you radiate warmth.",
        "Are you a sunset? Because you make everything beautiful.",
        "Do you have a compass? Because I keep finding my way to you.",
        "If you were a song, you'd be the one on repeat.",
        "Are you a dream? Because I don't want to wake up.",
        "Is your heart a lock? Because I'd love to find the key.",
        "You must be made of cheese, because you're looking gouda tonight.",
    ]

    _PICKUPLINES = [
        "Are you French? Because Eiffel for you.",
        "If you were a booger, I'd pick you first.",
        "Are you a 45-degree angle? Because you're acute-y.",
        "Do you like raisins? How do you feel about a date?",
        "Are you my appendix? Because I don't understand how you work but this feeling in my stomach makes me want to take you out.",
        "If you were a burger at McDonald's, you'd be the McGorgeous.",
        "Are you a carbon sample? Because I want to date you.",
        "Do you have a sunburn, or are you always this hot?",
        "Is your dad a boxer? Because you're a knockout!",
        "Are you a time traveler? Because I see you in my future.",
        "If I could rearrange the alphabet, I'd put U and I together.",
        "Are you made of copper and tellurium? Because you're Cu-Te.",
        "Did you invent the airplane? Because you seem Wright for me.",
        "Is your name Ariel? Because we mermaid for each other.",
        "Are you a camera? Because every time I look at you, I smile.",
        "If you were a triangle, you'd be acute one.",
        "Are you a piece of art? Because I'd frame you.",
        "Do you play soccer? Because you're a keeper!",
        "Are you a campfire? Because you're hot and I want s'more.",
        "Is it hot in here, or is it just you?",
        "Are you a tower? Because Eiffel for you.",
        "If you were a vegetable, you'd be a cute-cumber.",
        "Can I follow you? Because my mom told me to follow my dreams.",
        "Are you a banana? Because I find you a-peeling.",
        "If you were a library book, I'd check you out.",
        "Do you have a name, or can I call you mine?",
        "Are you a unicorn? Because you're one of a kind.",
        "Is your name Candy? Because you're sweet.",
        "Are you a star? Because your beauty lights up the night.",
        "Did it hurt when you fell from the vending machine? Because you look like a snack.",
        "If beauty were a crime, you'd be serving a life sentence.",
        "You must be a broom, because you just swept me off my feet.",
    ]

    _CHEESY = [
        "Are you a cheese? Because you're looking gouda tonight.",
        "You must be made of swiss cheese, because you've got me full of holes... in my heart.",
        "Are you brie? Because you're the big cheese of my dreams.",
        "Is your name Cheddar? Because you're sharp and I'm craving you.",
        "You must be cream cheese, because you're spreading joy everywhere.",
        "Are you mozzarella? Because you've stringed me along and I'm loving it.",
        "You're like parmesan — you make everything better.",
        "Are you a cheese platter? Because I want to spend hours with you.",
        "You must be goat cheese, because you're fancy and I'm impressed.",
        "Are you a grilled cheese? Because you're warm and comforting.",
        "You're like mac and cheese — the ultimate comfort.",
        "Are you feta? Because you've crumbled my defenses.",
        "You must be gorgonzola, because you're bold and unforgettable.",
        "Are you nacho cheese? Because you're NACHO average person.",
        "You're like a cheese wheel — round, complete, and I want the whole thing.",
        "Are you a charcuterie board? Because you've got everything I want.",
        "You must be fondue, because you've melted my heart.",
        "Are you ricotta? Because I can't believe how sweet you are.",
        "You're like halloumi — you can take the heat and still be amazing.",
        "Are you a cheese factory? Because you're producing pure happiness.",
        "You must be mascarpone, because you make everything sweeter.",
    ]

    _SMOOTH = [
        "I'm not a photographer, but I can picture us together.",
        "I must be a snowflake, because I've fallen for you.",
        "Do you have a name, or can I call you mine?",
        "You must be tired, because you've been running through my mind all day.",
        "Is it hot in here, or is that just you?",
        "I'd offer you a cigarette, but you're already smoking.",
        "Your hand looks heavy — can I hold it for you?",
        "I'm not a genie, but I can make your dreams come true.",
        "Are you the moon? Because even when it's dark, you light up my world.",
        "I'm no mathematician, but I'm pretty good with numbers. Want me to give you mine?",
        "If you were a tear, I'd never cry for fear of losing you.",
        "Are you a sunset? Because I can't stop staring.",
        "I must be in a museum, because you're a work of art.",
        "Are you the ocean? Because I'm lost at sea.",
        "I'm not a weatherman, but you can expect more than a few inches tonight... of snow, obviously.",
        "You must be the square root of -1, because you can't be real.",
    ]

    _CHARM = [
        "You have the kind of energy that makes the whole room brighter.",
        "I was having a terrible day until you showed up.",
        "There's something about you that makes everything feel possible.",
        "Your smile should come with a warning label — it's dangerously captivating.",
        "I don't believe in perfection, but you're pretty close.",
        "You're the kind of person who makes 'ordinary' feel extraordinary.",
        "If charm were a currency, you'd be a billionaire.",
        "Your presence is like a warm cup of coffee on a cold morning.",
        "You've got that rare combination of beauty and wit.",
        "I'd say you're out of my league, but I think you created a whole new one.",
        "You're the reason the word 'charisma' was invented.",
        "If I had a flower for every time you made me smile, I'd have an endless garden.",
        "Your vibe is immaculate.",
        "You're proof that good things come in amazing packages.",
        "I'm not easily impressed, but here I am.",
    ]

    _ROMANTIC = [
        "If I had to choose between breathing and loving you, I'd use my last breath to tell you I love you.",
        "You're not just my person — you're my favorite hello and my hardest goodbye.",
        "In a room full of art, I'd still stare at you.",
        "My night has become a sunny dawn because of you.",
        "You're the reason I believe in love at first sight.",
        "Every love story is beautiful, but ours is my favorite.",
        "I could conquer the world with just one hand, as long as you're holding the other.",
        "You don't just make my heart skip a beat — you make it do a whole drum solo.",
        "If I could reach up and hold a star for every time you've made me smile, the entire sky would be in my hands.",
        "You're the poem I never knew how to write, and this life is the story I've always wanted to tell.",
        "When I look at you, I can feel my heart racing and my worries fading.",
        "You're my favorite notification.",
        "I love you not only for what you are, but for what I become when I'm with you.",
        "You're the missing piece I never knew I needed.",
        "If love were a language, you'd be the only word I'd ever need.",
    ]

    _SUAVE = [
        "I don't always flirt, but when I do, it's with you.",
        "You must be a secret agent, because you've stolen my heart without leaving a trace.",
        "I'd cook you dinner, but I'd rather take you somewhere you deserve.",
        "Are you a fine wine? Because you only get better with time.",
        "I don't need a map — your eyes already show me the way.",
        "You must be a masterpiece, because I can't look away.",
        "They say timing is everything. Mine must be perfect because I found you.",
        "I don't believe in luck, but meeting you makes me reconsider.",
        "You're like a rare book — I want to spend hours getting to know every page.",
        "I'd write you a love song, but no melody does you justice.",
        "You don't need a filter — you're already picture perfect.",
        "I'm not trying to impress you, I'm just being myself. The impressive part is you still noticed.",
        "You must be gravity, because I'm drawn to you.",
        "I'm not smooth — you're just stunning enough to make me try.",
        "You make confidence look effortless.",
    ]

    _CRINGE = [
        "Are you a trash can? Because I want to take you out.",
        "Is your name homework? Because I'm not doing you but I should be.",
        "Are you a door? Because I'm banging on you... to come inside and chat politely.",
        "Do you like me? Circle yes or no.",
        "Are you my appendix? Because I don't understand you but I feel like I need you.",
        "If you were a fruit, you'd be a fine-apple. Wait, I already used that one.",
        "Did you fart? Because you blew me away.",
        "Are you a beaver? Because daaaaam.",
        "Are you a vampire? Because you looked a little pale... until I showed up.",
        "I'm not a doctor, but I can prescribe you a dose of me.",
        "Are you a WiFi signal? Because I'm feeling a connection... and it's really weak.",
        "Is your name Earl Grey? Because you're a tea-riffic sight.",
        "Are you a skeleton? Because I can see right through to your heart.",
        "Do you have a mirror in your pocket? Because I can see myself in your pants... pocket, looking for my keys.",
        "If you were a chicken, you'd be impeccable.",
        "Are you from Tennessee? Because you're the only ten I see.",
    ]

    _VALENTINES = [
        "Roses are red, violets are blue, I'd rather be texting than doing anything else — especially with you.",
        "You're the chocolate in my heart-shaped box.",
        "If Cupid had good aim, he'd hit you — because you're the perfect target for love.",
        "You're my Valentine, and I'm not even mad about the candy tax.",
        "Be mine — or at least be the person who laughs at my jokes.",
        "I'd give you my heart, but it's already running on your fuel.",
        "Happy Valentine's Day to the person who makes every day feel like February 14th.",
        "You're sweeter than a box of conversation hearts.",
        "I don't need a Valentine — I need YOU.",
        "You're the only person I'd share my last chocolate with.",
    ]

    _DMS = [
        "Hey, I was just thinking about you and figured I'd say hi. So... hi. 👋",
        "I saw something today that reminded me of you — it was really nice.",
        "Random thought: you're awesome, and I felt like you should know.",
        "Quick question: how do you manage to be that cool? Asking for a friend.",
        "I'm not great at starting conversations, but I'm great at wanting to talk to you.",
        "Hey! No pressure, just wanted to drop in and make you smile.",
        "So I was going to play it cool, but then I remembered I don't know how.",
        "If you could have dinner with anyone, would you pick me? No pressure.",
        "I have a confession: I've been wanting to message you for a while.",
        "You. Me. A conversation. What do you say?",
    ]

    _WINGMANS = [
        "My friend thinks you're pretty great. I think so too, but that's not the point.",
        "I'm here on behalf of someone who's too nervous to say this: they think you're amazing.",
        "Look, I'm just the wingman. The real star of the show is over there being cool.",
        "Can I be honest? My friend hasn't stopped talking about you all day.",
        "My friend asked me to come over and say hi. So... hi from them. And also me.",
        "I'm the opening act. The main event is my friend, who thinks you're awesome.",
        "Consider me your friendly neighborhood wingperson. My friend thinks you're fantastic.",
        "I've been authorized to inform you that my friend is 100% worth your time.",
        "My friend is too shy to say it, but they think you're the best person in this room.",
        "Wingman report: my friend is interested. I vouch for them. They're great.",
    ]

    _FLIRTBACKS = [
        "Oh, you're flirting? Challenge accepted. 💫",
        "Is that the best you've got? Because I've got more where that came from.",
        "Flirting with me? Bold move. I respect it.",
        "Well well well, look who's trying to make me blush.",
        "Two can play at this game, and I play to win.",
        "That was smooth. Let me see if I can match that energy.",
        "Flirting detected. Counter-flirt initiated.",
        "Oh, it's flirting o'clock? I didn't get the memo, but I'm dressed for the occasion.",
        "I see your flirt and raise you one genuine compliment.",
        "If you're trying to make me smile, mission accomplished.",
    ]

    _COMPLIMENT2S = [
        "You have the kind of confidence that doesn't need to announce itself.",
        "Your laugh could power a small city.",
        "You're proof that good vibes are contagious.",
        "Your personality is your best accessory, and you wear it well.",
        "You're the type of person who makes strangers feel like friends.",
        "I admire how you stay true to yourself.",
        "Your enthusiasm is absolutely infectious.",
        "You've got main character energy and it shows.",
        "There's something about your vibe that just makes everything better.",
        "You give the best advice, even when you don't realize it.",
        "Your creativity is inspiring.",
        "You have a rare gift for making people feel seen.",
        "Your kindness is your superpower.",
        "You're the definition of 'good people.'",
        "Everything you do, you do with style.",
    ]

    _WHISPERS = [
        "Hey... I just wanted to say you're pretty amazing. 🤫",
        "Don't tell anyone, but I think you're the coolest person here.",
        "Just a little secret: you make this chat worth being in.",
        "Whisper whisper... you're awesome. Pass it on.",
        "Between you and me, you're the highlight of my day.",
        "Pssst... I think you're great, but let's keep that between us.",
        "Quietly dropping by to say you're wonderful. No big deal.",
        "Secret message: you've got something special. Don't let anyone tell you otherwise.",
        "Lowkey, you're the best. Highkey, I want everyone to know.",
        "Whispered compliment incoming: you're incredible, and I mean it.",
    ]

    _CONFESSES = [
        "I have a confession: I think about our conversations way more than I should.",
        "Confession time: you make me nervous in the best way possible.",
        "I'll confess — I've re-read our messages more than once.",
        "Here's my confession: I get genuinely happy when you come online.",
        "Confession: I've been wanting to tell you something nice for a while.",
        "I confess — your vibe is unmatched and I'm a little jealous.",
        "Real confession: I admire you more than I let on.",
        "Confession: I saved your last message because it made me smile.",
        "Here goes: I think you're genuinely one of a kind.",
        "Confession: I wrote like five different messages before sending this one.",
    ]

    # ═══════════════════════════════════════════════════════════════
    #  FLIRT COMMANDS (15)
    # ═══════════════════════════════════════════════════════════════

    # 21. FLIRT
    @app.on_message(filters.command("flirt", prefixes=".") & filters.me)
    async def flirt_cmd(client, message):
        name = _get_target_name(client, message)
        lines = random.sample(_FLIRTS, min(3, len(_FLIRTS)))
        text = f"😍 **Flirting with {name}!**\n\n"
        for i, l in enumerate(lines, 1):
            text += f"{i}. {l}\n"
        await message.edit(text)

    register_command("Naughty", "flirt", "Flirt with someone using smooth lines", [])

    # 22. PICKUP / PICKUPLINE
    @app.on_message(filters.command(["pickup", "pickupline"], prefixes=".") & filters.me)
    async def pickup_cmd(client, message):
        name = _get_target_name(client, message)
        lines = random.sample(_PICKUPLINES, min(3, len(_PICKUPLINES)))
        text = f"💌 **Pickup lines for {name}!**\n\n"
        for i, l in enumerate(lines, 1):
            text += f"{i}. {l}\n"
        await message.edit(text)

    register_command("Naughty", "pickup", "Deliver cheesy pickup lines", ["pickupline"])

    # 23. CHEESY
    @app.on_message(filters.command("cheesy", prefixes=".") & filters.me)
    async def cheesy_cmd(client, message):
        name = _get_target_name(client, message)
        lines = random.sample(_CHEESY, min(2, len(_CHEESY)))
        text = f"🧀 **Cheesy lines for {name}!**\n\n"
        for i, l in enumerate(lines, 1):
            text += f"{i}. {l}\n"
        await message.edit(text)

    register_command("Naughty", "cheesy", "Extra cheesy pickup lines", [])

    # 24. SMOOTH
    @app.on_message(filters.command("smooth", prefixes=".") & filters.me)
    async def smooth_cmd(client, message):
        name = _get_target_name(client, message)
        lines = random.sample(_SMOOTH, min(2, len(_SMOOTH)))
        text = f"😎 **Smooth lines for {name}!**\n\n"
        for i, l in enumerate(lines, 1):
            text += f"{i}. {l}\n"
        await message.edit(text)

    register_command("Naughty", "smooth", "Smooth and suave lines", [])

    # 25. CHARM
    @app.on_message(filters.command("charm", prefixes=".") & filters.me)
    async def charm_cmd(client, message):
        name = _get_target_name(client, message)
        lines = random.sample(_CHARM, min(2, len(_CHARM)))
        text = f"✨ **Charming {name}!**\n\n"
        for i, l in enumerate(lines, 1):
            text += f"{i}. {l}\n"
        await message.edit(text)

    register_command("Naughty", "charm", "Charm someone with compliments", [])

    # 26. ROMANTIC
    @app.on_message(filters.command("romantic", prefixes=".") & filters.me)
    async def romantic_cmd(client, message):
        name = _get_target_name(client, message)
        lines = random.sample(_ROMANTIC, min(2, len(_ROMANTIC)))
        text = f"🌹 **Being romantic with {name}!**\n\n"
        for i, l in enumerate(lines, 1):
            text += f"{i}. {l}\n"
        await message.edit(text)

    register_command("Naughty", "romantic", "Romantic lines and quotes", [])

    # 27. SUAVE
    @app.on_message(filters.command("suave", prefixes=".") & filters.me)
    async def suave_cmd(client, message):
        name = _get_target_name(client, message)
        lines = random.sample(_SUAVE, min(2, len(_SUAVE)))
        text = f"🎩 **Suave mode for {name}!**\n\n"
        for i, l in enumerate(lines, 1):
            text += f"{i}. {l}\n"
        await message.edit(text)

    register_command("Naughty", "suave", "Suave and sophisticated lines", [])

    # 28. CRINGE / CREEPY
    @app.on_message(filters.command(["cringe", "creepy"], prefixes=".") & filters.me)
    async def cringe_cmd(client, message):
        name = _get_target_name(client, message)
        lines = random.sample(_CRINGE, min(2, len(_CRINGE)))
        text = f"😬 **Cringe lines for {name}!**\n\n"
        for i, l in enumerate(lines, 1):
            text += f"{i}. {l}\n"
        await message.edit(text)

    register_command("Naughty", "cringe", "Cringe-worthy pickup lines", ["creepy"])

    # 29. VALENTINE
    @app.on_message(filters.command("valentine", prefixes=".") & filters.me)
    async def valentine_cmd(client, message):
        name = _get_target_name(client, message)
        text = f"💝 **Valentine's message for {name}!**\n\n{random.choice(_VALENTINES)}"
        await message.edit(text)

    register_command("Naughty", "valentine", "Valentine's day messages", [])

    # 30. DM
    @app.on_message(filters.command("dm", prefixes=".") & filters.me)
    async def dm_cmd(client, message):
        name = _get_target_name(client, message)
        text = f"📩 **DM opener for {name}!**\n\n{random.choice(_DMS)}"
        await message.edit(text)

    register_command("Naughty", "dm", "Suggest a DM opener", [])

    # 31. WINGMAN
    @app.on_message(filters.command("wingman", prefixes=".") & filters.me)
    async def wingman_cmd(client, message):
        name = _get_target_name(client, message)
        text = f"🪽 **Wingman for {name}!**\n\n{random.choice(_WINGMANS)}"
        await message.edit(text)

    register_command("Naughty", "wingman", "Wingman lines to help someone out", [])

    # 32. FLIRTBACK
    @app.on_message(filters.command("flirtback", prefixes=".") & filters.me)
    async def flirtback_cmd(client, message):
        name = _get_target_name(client, message)
        text = f"😏 **Flirting back at {name}!**\n\n{random.choice(_FLIRTBACKS)}"
        await message.edit(text)

    register_command("Naughty", "flirtback", "Counter-flirt with style", [])

    # 33. COMPLIMENT2
    @app.on_message(filters.command("compliment2", prefixes=".") & filters.me)
    async def compliment2_cmd(client, message):
        name = _get_target_name(client, message)
        lines = random.sample(_COMPLIMENT2S, min(2, len(_COMPLIMENT2S)))
        text = f"💖 **Compliments for {name}!**\n\n"
        for i, l in enumerate(lines, 1):
            text += f"{i}. {l}\n"
        await message.edit(text)

    register_command("Naughty", "compliment2", "Extra heartfelt compliments", [])

    # 34. WHISPER
    @app.on_message(filters.command("whisper", prefixes=".") & filters.me)
    async def whisper_cmd(client, message):
        name = _get_target_name(client, message)
        text = f"🤫 *whispering to {name}*\n\n{random.choice(_WHISPERS)}"
        await message.edit(text)

    register_command("Naughty", "whisper", "Whisper something sweet", [])

    # 35. CONFESS
    @app.on_message(filters.command("confess", prefixes=".") & filters.me)
    async def confess_cmd(client, message):
        name = _get_target_name(client, message)
        text = f"🫣 **Confession for {name}!**\n\n{random.choice(_CONFESSES)}"
        await message.edit(text)

    register_command("Naughty", "confess", "Make a sweet confession", [])

    # ═══════════════════════════════════════════════════════════════
    #  RATINGS DATA & COMMANDS (16 commands)
    # ═══════════════════════════════════════════════════════════════

    _RATING_CONFIG = {
        "ship": {"emoji": "❤️", "label": "Ship", "bar": True},
        "rate": {"emoji": "⭐", "label": "Rate", "bar": False},
        "hot": {"emoji": "🔥", "label": "Hot", "bar": False},
        "sexy": {"emoji": "💋", "label": "Sexy", "bar": False},
        "smash": {"emoji": "💥", "label": "Smash", "bar": False},
        "wifey": {"emoji": "💍", "label": "Wifey Material", "bar": False},
        "hubby": {"emoji": "🤵", "label": "Hubby Material", "bar": False},
        "redflag": {"emoji": "🚩", "label": "Red Flag", "bar": False},
        "greenflag": {"emoji": "✅", "label": "Green Flag", "bar": False},
        "toxicity": {"emoji": "☠️", "label": "Toxicity", "bar": False},
        "clingy": {"emoji": "🤗", "label": "Clingy", "bar": False},
        "loyal": {"emoji": "🤝", "label": "Loyalty", "bar": False},
        "freaky": {"emoji": "😏", "label": "Freaky", "bar": False},
        "innocent": {"emoji": "😇", "label": "Innocence", "bar": False},
        "dangerous": {"emoji": "⚡", "label": "Dangerous", "bar": False},
        "partner": {"emoji": "💑", "label": "Partner Material", "bar": False},
    }

    def _rating_text(name, key, config, extra_salt=""):
        score = _deterministic_score(name, key, extra_salt)
        emoji = config["emoji"]
        label = config["label"]
        if config.get("bar"):
            bar = _progress_bar(score)
            return f"{emoji} **{label}: {name}**\n\n[{bar}] **{score}%**"
        else:
            bar = _progress_bar(score)
            return f"{emoji} **{label}: {name}**\n\n[{bar}] **{score}%**"

    # 36. SHIP
    @app.on_message(filters.command("ship", prefixes=".") & filters.me)
    async def ship_cmd(client, message):
        name1 = _get_target_name(client, message)
        if message.reply_to_message:
            u2 = message.reply_to_message.from_user
            name2 = u2.first_name if u2 else "Someone"
        else:
            args = message.text.split(None, 2)
            name2 = args[2] if len(args) > 2 else args[1] if len(args) > 1 else "Yourself"
        combined = f"{name1}+{name2}"
        score = _deterministic_score(combined, "ship")
        bar = _progress_bar(score)
        hearts = "❤️" * (score // 20 + 1)
        text = (
            f"❤️ **Ship: {name1} + {name2}**\n\n"
            f"[{bar}] **{score}%**\n"
            f"{hearts}\n\n"
        )
        if score >= 80:
            text += "💍 **MATCH MADE IN HEAVEN!**"
        elif score >= 60:
            text += "💕 **Great chemistry!**"
        elif score >= 40:
            text += "🤔 **Could work... maybe?**"
        elif score >= 20:
            text += "😬 **It's complicated...**"
        else:
            text += "💔 **Not meant to be.**"
        await message.edit(text)

    register_command("Naughty", "ship", "Ship two people with progress bar", [])

    # 37. RATE
    @app.on_message(filters.command("rate", prefixes=".") & filters.me)
    async def rate_cmd(client, message):
        name = _get_target_name(client, message)
        cfg = _RATING_CONFIG["rate"]
        text = _rating_text(name, "rate", cfg)
        await message.edit(text)

    register_command("Naughty", "rate", "Rate someone 0-100%", [])

    # 38. HOT
    @app.on_message(filters.command("hot", prefixes=".") & filters.me)
    async def hot_cmd(client, message):
        name = _get_target_name(client, message)
        cfg = _RATING_CONFIG["hot"]
        text = _rating_text(name, "hot", cfg)
        await message.edit(text)

    register_command("Naughty", "hot", "How hot is someone 0-100%", [])

    # 39. SEXY
    @app.on_message(filters.command("sexy", prefixes=".") & filters.me)
    async def sexy_cmd(client, message):
        name = _get_target_name(client, message)
        cfg = _RATING_CONFIG["sexy"]
        text = _rating_text(name, "sexy", cfg)
        await message.edit(text)

    register_command("Naughty", "sexy", "Sexy rating 0-100%", [])

    # 40. SMASH
    @app.on_message(filters.command("smash", prefixes=".") & filters.me)
    async def smash_cmd(client, message):
        name = _get_target_name(client, message)
        score = _deterministic_score(name, "smash")
        text = f"💥 **Smash or Pass: {name}**\n\n{_progress_bar(score)} **{score}%**"
        if score >= 70:
            text += "\n\n✅ **SMASH!**"
        elif score >= 40:
            text += "\n\n🤔 **Hmm, maybe...**"
        else:
            text += "\n\n❌ **Pass.**"
        await message.edit(text)

    register_command("Naughty", "smash", "Smash or pass rating", [])

    # 41. WIFEY
    @app.on_message(filters.command("wifey", prefixes=".") & filters.me)
    async def wifey_cmd(client, message):
        name = _get_target_name(client, message)
        cfg = _RATING_CONFIG["wifey"]
        text = _rating_text(name, "wifey", cfg)
        await message.edit(text)

    register_command("Naughty", "wifey", "Wifey material rating", [])

    # 42. HUBBY
    @app.on_message(filters.command("hubby", prefixes=".") & filters.me)
    async def hubby_cmd(client, message):
        name = _get_target_name(client, message)
        cfg = _RATING_CONFIG["hubby"]
        text = _rating_text(name, "hubby", cfg)
        await message.edit(text)

    register_command("Naughty", "hubby", "Hubby material rating", [])

    # 43. REDFLAG
    @app.on_message(filters.command("redflag", prefixes=".") & filters.me)
    async def redflag_cmd(client, message):
        name = _get_target_name(client, message)
        score = _deterministic_score(name, "redflag")
        flags = "🚩" * (score // 15 + 1)
        text = f"🚩 **Red Flag Check: {name}**\n\n{_progress_bar(score)} **{score}%**\n{flags}"
        if score >= 80:
            text += "\n\n🚨 **DANGER ZONE! Run!**"
        elif score >= 50:
            text += "\n\n⚠️ **Proceed with caution.**"
        else:
            text += "\n\n✅ **Looks safe... for now.**"
        await message.edit(text)

    register_command("Naughty", "redflag", "Red flag check 0-100%", [])

    # 44. GREENFLAG
    @app.on_message(filters.command("greenflag", prefixes=".") & filters.me)
    async def greenflag_cmd(client, message):
        name = _get_target_name(client, message)
        cfg = _RATING_CONFIG["greenflag"]
        score = _deterministic_score(name, "greenflag")
        text = f"✅ **Green Flag Check: {name}**\n\n{_progress_bar(score)} **{score}%**"
        if score >= 80:
            text += "\n\n🌿 **Absolute green flag!**"
        elif score >= 50:
            text += "\n\n👍 **Mostly green flags.**"
        else:
            text += "\n\n🤔 **Some green, some... not.**"
        await message.edit(text)

    register_command("Naughty", "greenflag", "Green flag check 0-100%", [])

    # 45. TOXICITY
    @app.on_message(filters.command("toxicity", prefixes=".") & filters.me)
    async def toxicity_cmd(client, message):
        name = _get_target_name(client, message)
        cfg = _RATING_CONFIG["toxicity"]
        score = _deterministic_score(name, "toxicity")
        text = f"☠️ **Toxicity: {name}**\n\n{_progress_bar(score)} **{score}%**"
        if score >= 80:
            text += "\n\n🧪 **Hazardous material!**"
        elif score >= 50:
            text += "\n\n⚠️ **Mildly toxic.**"
        else:
            text += "\n\n🍃 **Pretty wholesome!**"
        await message.edit(text)

    register_command("Naughty", "toxicity", "Toxicity level 0-100%", [])

    # 46. CLINGY
    @app.on_message(filters.command("clingy", prefixes=".") & filters.me)
    async def clingy_cmd(client, message):
        name = _get_target_name(client, message)
        cfg = _RATING_CONFIG["clingy"]
        text = _rating_text(name, "clingy", cfg)
        await message.edit(text)

    register_command("Naughty", "clingy", "Clingy rating 0-100%", [])

    # 47. LOYAL
    @app.on_message(filters.command("loyal", prefixes=".") & filters.me)
    async def loyal_cmd(client, message):
        name = _get_target_name(client, message)
        cfg = _RATING_CONFIG["loyal"]
        text = _rating_text(name, "loyal", cfg)
        await message.edit(text)

    register_command("Naughty", "loyal", "Loyalty rating 0-100%", [])

    # 48. FREAKY
    @app.on_message(filters.command("freaky", prefixes=".") & filters.me)
    async def freaky_cmd(client, message):
        name = _get_target_name(client, message)
        cfg = _RATING_CONFIG["freaky"]
        text = _rating_text(name, "freaky", cfg)
        await message.edit(text)

    register_command("Naughty", "freaky", "Freaky rating 0-100%", [])

    # 49. INNOCENT
    @app.on_message(filters.command("innocent", prefixes=".") & filters.me)
    async def innocent_cmd(client, message):
        name = _get_target_name(client, message)
        cfg = _RATING_CONFIG["innocent"]
        text = _rating_text(name, "innocent", cfg)
        await message.edit(text)

    register_command("Naughty", "innocent", "Innocence rating 0-100%", [])

    # 50. DANGEROUS
    @app.on_message(filters.command("dangerous", prefixes=".") & filters.me)
    async def dangerous_cmd(client, message):
        name = _get_target_name(client, message)
        cfg = _RATING_CONFIG["dangerous"]
        text = _rating_text(name, "dangerous", cfg)
        await message.edit(text)

    register_command("Naughty", "dangerous", "Dangerous rating 0-100%", [])

    # 51. PARTNER
    @app.on_message(filters.command("partner", prefixes=".") & filters.me)
    async def partner_cmd(client, message):
        name = _get_target_name(client, message)
        cfg = _RATING_CONFIG["partner"]
        text = _rating_text(name, "partner", cfg)
        await message.edit(text)

    register_command("Naughty", "partner", "Partner material rating 0-100%", [])

    # ═══════════════════════════════════════════════════════════════
    #  GENERATORS DATA (15 commands)
    # ═══════════════════════════════════════════════════════════════

    _EXCUSES = [
        "My grandmother's parrot had an existential crisis and I had to talk it down.",
        "I got stuck in a philosophical debate with my reflection.",
        "A raccoon stole my shoes and I had to negotiate for them.",
        "My neighbor's cat scheduled a surprise intervention for me.",
        "I was temporarily trapped in a Netflix documentary about cheese.",
        "The universe aligned in a way that specifically prevented me from attending.",
        "My houseplant looked sad so I had to stay and comfort it.",
        "I got caught in a time loop but only the boring part.",
        "My WiFi router and I had a disagreement about commitment.",
        "A squirrel declared war on my mailbox and I had to defend it.",
        "I was busy teaching my goldfish about democracy.",
        "My refrigerator was making a sound that demanded my full attention.",
        "I got lost in my own neighborhood — the streets changed, I swear.",
        "My blanket was too comfortable and I don't make the rules of physics.",
        "I was preparing for the apocalypse. It hasn't happened yet, so you're welcome.",
        "A bee followed me and I had to lead it away from civilization.",
        "My phone autocorrected my alarm to 'charm' and honestly it was quite charming.",
    ]

    _ALIBIS = [
        "I was at the library studying the migratory patterns of pigeons.",
        "I was volunteering at the 'Socks Without Partners' charity.",
        "I was in a board meeting — a surfboard meeting at the beach.",
        "I was teaching my houseplants about photosynthesis.",
        "I was busy documenting the secret life of my neighbor's garden gnome.",
        "I was at a very important appointment with my couch.",
        "I was conducting research on how many snacks fit in one sitting.",
        "I was at a seminar on 'How to Apologize for Not Showing Up.'",
        "I was reorganizing my fridge by color coordination.",
        "I was in deep meditation about whether a hotdog is a sandwich.",
        "I was busy planning my acceptance speech for an award I haven't won.",
        "I was investigating a mysterious noise that turned out to be my stomach.",
        "I was at an emergency meeting of the Procrastinators Club — it was postponed.",
        "I was testing how long I can stare at a wall before getting bored.",
        "I was cataloging my collection of slightly different shades of beige.",
        "I was in a staring contest with my cat. I lost.",
    ]

    _CONFESSIONS = [
        "I once liked my own post from a fake account just to get started.",
        "I pretend to understand cryptocurrency at parties.",
        "I've rehearsed conversations in the shower that will never happen.",
        "I sometimes wave back at people who weren't waving at me.",
        "I've Googled words I should definitely know by now.",
        "I laugh at my own jokes before I even finish telling them.",
        "I've canceled plans to stay home and do absolutely nothing.",
        "I sometimes pretend to text to avoid talking to people.",
        "I've eaten food that fell on the floor and told no one.",
        "I judge people by their phone case.",
        "I've practiced my Oscar acceptance speech in the mirror.",
        "I've sent myself a message just to test if my notifications work.",
        "I sometimes rehearse arguments I might have in the future.",
        "I've pretended to be on a call to avoid small talk.",
        "I've reread my old messages and cringed at my own grammar.",
        "I've taken a selfie, deleted it, and then retaken the exact same one.",
    ]

    _RUMORS = [
        "I heard they were secretly raised by dolphins for the first five years.",
        "Rumor has it they can communicate with houseplants telepathically.",
        "Word on the street is they're the real reason WiFi goes down.",
        "Apparently, they were almost cast as the main character in a major movie.",
        "Sources say they have an undefeated record in competitive napping.",
        "I heard they once convinced a pigeon to carry a message. The pigeon refused.",
        "Rumor has it their aura is visible from space.",
        "Apparently they're the secret third member of every famous duo.",
        "Word is they can fold a fitted sheet perfectly on the first try.",
        "Sources claim they've never lost a staring contest with a cat.",
        "I heard they were the inspiration for a famous emoji.",
        "Rumor has it they can parallel park on the first try. Every time.",
        "Word on the street is they have a PhD in snacking.",
        "Apparently they taught a goldfish to do tricks. The fish was unimpressed.",
        "I heard they can make instant ramen taste like a 5-star meal.",
    ]

    _SECRETS = [
        "They secretly believe the dress is blue and black. Always.",
        "Their browser history is 90% 'how to basic' tutorials.",
        "They have a secret playlist that's just whale sounds and rain.",
        "They've never actually seen The Office but laugh at the references.",
        "Their phone wallpaper is a picture of a sandwich they once loved.",
        "They practice smiling in the mirror before social events.",
        "They have a detailed ranking of every cheese they've ever tried.",
        "Their secret talent is predicting when the microwave will hit zero.",
        "They've written a 50-page document on why pineapple belongs on pizza.",
        "They keep a log of every weird dream they've ever had.",
        "They can recite the entire menu of their favorite restaurant from memory.",
        "They have a secret fear of overly enthusiastic mascots.",
        "Their hidden skill is making the perfect cup of tea on the first try.",
        "They've memorized the WiFi passwords of every place they've visited.",
        "They keep a spreadsheet of their best comebacks for future use.",
    ]

    _REVIEWS = [
        "⭐⭐⭐⭐⭐ Amazing! Would interact again. Customer service was top-notch.",
        "⭐⭐⭐ Decent human being. Lost one star for bad timing. Another for excessive puns.",
        "⭐⭐⭐⭐⭐ Five stars! A stunning contribution to the conversation.",
        "⭐ One star. Would not recommend. Caused an awkward silence that lasted 47 seconds.",
        "⭐⭐⭐⭐ Solid 4/5. Reliable, but needs more chaos in their life.",
        "⭐⭐ Two stars. The vibes were confusing and the energy was mid.",
        "⭐⭐⭐⭐⭐ Masterpiece! A cinematic experience in human form.",
        "⭐⭐⭐ Mid. Not bad, not great. The vanilla ice cream of personalities.",
        "⭐⭐⭐⭐⭐ Absolutely legendary! The main character energy is off the charts.",
        "⭐⭐ Needs improvement. The plot was predictable and the pacing was off.",
        "⭐⭐⭐⭐ Very good! A delightful experience with minor plot holes.",
        "⭐⭐⭐⭐⭐ Standing ovation! An instant classic.",
        "⭐⭐ Would not watch again. The storyline was confusing and the ending was rushed.",
        "⭐⭐⭐⭐ Certified fresh! A refreshing take on being a person.",
        "⭐⭐⭐ It was okay. Like a Tuesday. Not memorable, not terrible.",
    ]

    _YELPS = [
        "🌟🌟🌟🌟🌟 'The vibes here are immaculate. Will definitely return.' — Verified Human",
        "🌟🌟 'Found a hair in my conversation. Not literally, but the energy was off.' — Karen K.",
        "🌟🌟🌟🌟 'Solid experience. Would recommend to a friend, maybe.' — Chill C.",
        "🌟 'Zero stars if I could. The whole interaction felt like a loading screen.' — Disappointed D.",
        "🌟🌟🌟 'It was fine. Like gas station sushi — it exists.' — Average A.",
        "🌟🌟🌟🌟🌟 'Life-changing! I'm a different person now.' — Dramatic D.",
        "🌟🌟 'The ambiance was giving waiting room at the dentist.' — Skeptical S.",
        "🌟🌟🌟🌟 'Surprisingly delightful! Like finding money in your old jeans.' — Lucky L.",
        "🌟 'I've had better interactions with my GPS.' — Lost L.",
        "🌟🌟🌟 'Decent. Like a 6/10 on the personality scale.' — Numeric N.",
    ]

    _REPORTS = [
        "📋 **Official Report**\nSubject: [Name]\nViolation: Excessive awesomeness\nSeverity: Critical\nAction: Mandatory high-five",
        "📋 **Official Report**\nSubject: [Name]\nViolation: Being too funny\nSeverity: High\nAction: Must dad-joke rehab",
        "📋 **Official Report**\nSubject: [Name]\nViolation: Unauthorized good vibes\nSeverity: Moderate\nAction: Issued warning",
        "📋 **Official Report**\nSubject: [Name]\nViolation: Suspicious levels of charm\nSeverity: Critical\nAction: Under investigation",
        "📋 **Official Report**\nSubject: [Name]\nViolation: Lacking chill\nSeverity: Extreme\nAction: Chill injections required",
        "📋 **Official Report**\nSubject: [Name]\nViolation: Being a menace (complimentary)\nSeverity: High\nAction: Monitored for greatness",
        "📋 **Official Report**\nSubject: [Name]\nViolation: Illegal amounts of style\nSeverity: Critical\nAction: Fashion police notified",
        "📋 **Official Report**\nSubject: [Name]\nViolation: Excessive sass\nSeverity: Moderate\nAction: Sass reduction program",
        "📋 **Official Report**\nSubject: [Name]\nViolation: Unregistered rizz\nSeverity: High\nAction: Must register at local rizz office",
        "📋 **Official Report**\nSubject: [Name]\nViolation: Being suspiciously wholesome\nSeverity: Low\nAction: No action, just admiration",
    ]

    _WARRANTS = [
        "🔍 **WARRANT ISSUED**\nFor: [Name]\nCharge: Armed and dangerous with comebacks\nBail: 1,000,000 likes\nStatus: ACTIVE",
        "🔍 **WARRANT ISSUED**\nFor: [Name]\nCharge: Grand theft attention\nBail: 500 compliments\nStatus: ACTIVE",
        "🔍 **WARRANT ISSUED**\nFor: [Name]\nCharge: Felony-level sarcasm\nBail: 3 sincere apologies\nStatus: ACTIVE",
        "🔍 **WARRANT ISSUED**\nFor: [Name]\nCharge: Emotional damages (from being too cool)\nBail: A high-five\nStatus: ACTIVE",
        "🔍 **WARRANT ISSUED**\nFor: [Name]\nCharge: Conspiracy to be amazing\nBail: Unlimited respect\nStatus: ACTIVE",
        "🔍 **WARRANT ISSUED**\nFor: [Name]\nCharge: Possession of excessive rizz\nBail: Humility classes\nStatus: ACTIVE",
        "🔍 **WARRANT ISSUED**\nFor: [Name]\nCharge: Operating a personality without a license\nBail: Chill pills\nStatus: ACTIVE",
        "🔍 **WARRANT ISSUED**\nFor: [Name]\nCharge: First-degree fun-having\nBail: Mandatory nap time\nStatus: ACTIVE",
        "🔍 **WARRANT ISSUED**\nFor: [Name]\nCharge: Disorderly conduct (being too loud with the vibes)\nBail: Volume control\nStatus: ACTIVE",
        "🔍 **WARRANT ISSUED**\nFor: [Name]\nCharge: Resisting the urge to be normal\nBail: Acceptance speech\nStatus: ACTIVE",
    ]

    _INDICTMENTS = [
        "⚖️ **INDICTMENT**\n[Name] is hereby charged with:\n• Count 1: Conspiracy to steal hearts\n• Count 2: Operating without sufficient chill\n• Count 3: Excessive use of charm\nMaximum penalty: Lifetime of being awesome",
        "⚖️ **INDICTMENT**\n[Name] is hereby charged with:\n• Count 1: First-degree sass\n• Count 2: Aggravated humor\n• Count 3: Possession of an unregistered personality\nMaximum penalty: Standing ovation",
        "⚖️ **INDICTMENT**\n[Name] is hereby charged with:\n• Count 1: Illegal distribution of good vibes\n• Count 2: Fraudulent levels of confidence\n• Count 3: Public disturbance (being too entertaining)\nMaximum penalty: Key to the city",
        "⚖️ **INDICTMENT**\n[Name] is hereby charged with:\n• Count 1: Reckless abandonment of boring conversations\n• Count 2: Operating a sense of humor above legal limits\n• Count 3: Embezzlement of everyone's attention\nMaximum penalty: Award ceremony",
        "⚖️ **INDICTMENT**\n[Name] is hereby charged with:\n• Count 1: Unauthorized style deployment\n• Count 2: Criminal levels of wit\n• Count 3: Aggravated awesomeness in a public setting\nMaximum penalty: VIP membership everywhere",
        "⚖️ **INDICTMENT**\n[Name] is hereby charged with:\n• Count 1: Grand theft spotlight\n• Count 2: Corrupting the youth with good energy\n• Count 3: Conspiracy to make people smile\nMaximum penalty: Nobel Prize nomination",
        "⚖️ **INDICTMENT**\n[Name] is hereby charged with:\n• Count 1: Violation of the boring-person act\n• Count 2: Exceeding maximum rizz limits\n• Count 3: Destruction of awkward silences\nMaximum penalty: Friendship bracelet",
        "⚖️ **INDICTMENT**\n[Name] is hereby charged with:\n• Count 1: Unlawful possession of charisma\n• Count 2: Distributing unlicensed compliments\n• Count 3: Organized good-vibing\nMaximum penalty: Group hug",
        "⚖️ **INDICTMENT**\n[Name] is hereby charged with:\n• Count 1: Inciting a laugh riot\n• Count 2: Being funny without a permit\n• Count 3: Conspiracy to brighten days\nMaximum penalty: Comedy special",
        "⚖️ **INDICTMENT**\n[Name] is hereby charged with:\n• Count 1: First-degree coolness\n• Count 2: Aggravated swagger\n• Count 3: Resisting the urge to be basic\nMaximum penalty: Hall of fame induction",
    ]

    _DIAGNOSES = [
        "🩺 **Medical Report**\nPatient: [Name]\nDiagnosis: Chronic sassiness (incurable but manageable)\nPrognosis: Will continue being iconic",
        "🩺 **Medical Report**\nPatient: [Name]\nDiagnosis: Acute fun-having syndrome\nPrognosis: No cure available, must live with it",
        "🩺 **Medical Report**\nPatient: [Name]\nDiagnosis: Severe case of main character energy\nPrognosis: Terminal. Patient will always be the star.",
        "🩺 **Medical Report**\nPatient: [Name]\nDiagnosis: Rizz deficiency — just kidding, levels are off the charts\nPrognosis: Dangerously charming",
        "🩺 **Medical Report**\nPatient: [Name]\nDiagnosis: Overactive humor gland\nPrognosis: Will make people laugh uncontrollably",
        "🩺 **Medical Report**\nPatient: [Name]\nDiagnosis: Exceptional vibes syndrome\nPrognosis: Contagious. Others will catch good energy.",
        "🩺 **Medical Report**\nPatient: [Name]\nDiagnosis: Chronic overachievement\nPrognosis: Refuses to be mediocre",
        "🩺 **Medical Report**\nPatient: [Name]\nDiagnosis: Acute loyalty imbalance (gives too much)\nPrognosis: Will remain a great friend",
        "🩺 **Medical Report**\nPatient: [Name]\nDiagnosis: Mild-to-severe awesomeness\nPrognosis: Incurable. Society is better for it.",
        "🩺 **Medical Report**\nPatient: [Name]\nDiagnosis: Terminal coolness\nPrognosis: Patient has accepted their fate with style",
        "🩺 **Medical Report**\nPatient: [Name]\nDiagnosis: Hyperactive creativity disorder\nPrognosis: Will keep coming up with amazing ideas",
        "🩺 **Medical Report**\nPatient: [Name]\nDiagnosis: Excessive empathy levels\nPrognosis: Will continue being too nice for their own good",
        "🩺 **Medical Report**\nPatient: [Name]\nDiagnosis: Chronic meme brain\nPrognosis: Will reference memes in every conversation",
        "🩺 **Medical Report**\nPatient: [Name]\nDiagnosis: Unbreakable spirit syndrome\nPrognosis: Cannot be stopped. Proceed with admiration.",
        "🩺 **Medical Report**\nPatient: [Name]\nDiagnosis: Infectious laughter disease\nPrognosis: Everyone around them will catch the giggles",
    ]

    _PERSONALITY_TYPES = [
        "🎭 **The Chaos Agent** — Brings disorder to every plan in the most entertaining way possible.",
        "🎭 **The Golden Retriever** — Pure, wholesome, and always excited to see you.",
        "🎭 **The Cat** — Independent, mysterious, and judges you silently.",
        "🎭 **The Professor** — Has an unnecessary amount of knowledge and shares it freely.",
        "🎭 **The Stand-Up Comic** — Turns every situation into material.",
        "🎭 **The Zen Master** — Unbothered, moisturized, happy, in their lane.",
        "🎭 **The Tornado** — Arrives suddenly, changes everything, leaves confusion.",
        "🎭 **The Care Bear** — Cares too much, gives the best hugs, worries about everyone.",
        "🎭 **The CEO of Vibes** — Controls the energy of every room they enter.",
        "🎭 **The Cryptid** — Rarely seen but when they appear, it's legendary.",
    ]

    _COMPATIBILITIES = [
        "🧬 **Compatibility Report**\nBased on completely scientific methods:\n\n☀️ Best match: Someone who shares your chaos\n🌙 Worst match: Anyone who takes themselves too seriously\n💫 Secret match: The person you least expect",
        "🧬 **Compatibility Report**\nBased on the stars and vibes:\n\n☀️ Best match: Fellow main character energy\n🌙 Worst match: NPC energy\n💫 Secret match: Your polar opposite",
        "🧬 **Compatibility Report**\nBased on ancient wisdom:\n\n☀️ Best match: Someone who laughs at your worst jokes\n🌙 Worst match: Someone who doesn't laugh at your best jokes\n💫 Secret match: The one who gets your weird references",
        "🧬 **Compatibility Report**\nBased on energy fields:\n\n☀️ Best match: Equal levels of unhinged\n🌙 Worst match: Too much chill\n💫 Secret match: The one who matches your freak",
        "🧬 **Compatibility Report**\nBased on zero research:\n\n☀️ Best match: Foodie with great taste\n🌙 Worst match: Someone who says 'I'm fine' and isn't\n💫 Secret match: The person who sends memes at 3am",
        "🧬 **Compatibility Report**\nBased on cosmic alignment:\n\n☀️ Best match: Someone who brings snacks\n🌙 Worst match: The 'let's talk about it' type\n💫 Secret match: Fellow night owl",
        "🧬 **Compatibility Report**\nBased on personality algorithms:\n\n☀️ Best match: The 'yes, and' type\n🌙 Worst match: The 'actually' type\n💫 Secret match: Someone who finishes your sentences",
        "🧬 **Compatibility Report**\nBased on tea leaves:\n\n☀️ Best match: Fellow chaotic good\n🌙 Worst match: Lawful boring\n💫 Secret match: The one who knows your coffee order",
        "🧬 **Compatibility Report**\nBased on the ancient art of vibes:\n\n☀️ Best match: Dog person (trust the process)\n🌙 Worst match: 'No drama' people (they ARE the drama)\n💫 Secret match: The one you argue with for fun",
        "🧬 **Compatibility Report**\nBased on nothing but intuition:\n\n☀️ Best match: Your comfort person\n🌙 Worst match: Anyone who doesn't like music\n💫 Secret match: The one who knows your playlist password",
    ]

    _LOVELETTERS = [
        "💌 **Dear [Name],**\nIf I could send you a bouquet of newly sharpened pencils, I would. You make every day feel like the first day of school — exciting, nervous, and full of possibility. Yours truly, Someone Who Notices.",
        "💌 **Dear [Name],**\nYou're the song I can't get out of my head, and I don't want to. You turn ordinary moments into memories I replay on loop. With affection, Your Number One Fan.",
        "💌 **Dear [Name],**\nI was going to write a love poem, but all my metaphors led back to you. So here's the truth: you make the world less annoying. Warmly, A Hopeless Romantic.",
        "💌 **Dear [Name],**\nIf loving you was a job, I'd be employee of the month every month. You're the reason I check my phone. Sincerely, Smitten.",
        "💌 **Dear [Name],**\nYou had me at 'hello' — or honestly, at 'sup.' Either way, I'm a fan. Fondly, Someone Who Thinks You're Great.",
        "💌 **Dear [Name],**\nI'd walk 500 miles, and I'd walk 500 more, just to be the person who delivers your coffee. With warmth, Your Local Admirer.",
        "💌 **Dear [Name],**\nYou're the plot twist I never saw coming, and the happily-ever-after I didn't know I needed. Yours, The Protagonist.",
        "💌 **Dear [Name],**\nIf you were a vegetable, you'd be a cute-cumber. If you were a text, you'd be the one I re-read at 2am. Adoringly, Sleepless.",
        "💌 **Dear [Name],**\nI don't know how to flirt, but I do know how to mean it when I say you're amazing. Honestly, Your Secret Admirer.",
        "💌 **Dear [Name],**\nRoses are red, violets are blue, this letter is cheesy, but it's all for you. XOXO, The Cheese.",
    ]

    # ═══════════════════════════════════════════════════════════════
    #  GENERATORS COMMANDS (15)
    # ═══════════════════════════════════════════════════════════════

    # 52. EXCUSE
    @app.on_message(filters.command("excuse", prefixes=".") & filters.me)
    async def excuse_cmd(client, message):
        text = f"🤷 **Excuse Generator**\n\n{random.choice(_EXCUSES)}"
        await message.edit(text)

    register_command("Naughty", "excuse", "Generate a creative excuse", [])

    # 53. ALIBI
    @app.on_message(filters.command("alibi", prefixes=".") & filters.me)
    async def alibi_cmd(client, message):
        text = f"🕵️ **Alibi Generator**\n\n{random.choice(_ALIBIS)}"
        await message.edit(text)

    register_command("Naughty", "alibi", "Generate a believable alibi", [])

    # 54. CONFESSION (generator)
    @app.on_message(filters.command("confession", prefixes=".") & filters.me)
    async def confession_gen_cmd(client, message):
        text = f"🫣 **Confession Generator**\n\n{random.choice(_CONFESSIONS)}"
        await message.edit(text)

    register_command("Naughty", "confession", "Generate a funny confession", [])

    # 55. RUMOR
    @app.on_message(filters.command("rumor", prefixes=".") & filters.me)
    async def rumor_cmd(client, message):
        name = _get_target_name(client, message)
        rumor = random.choice(_RUMORS)
        text = f"🤫 **Rumor about {name}**\n\n{rumor}"
        await message.edit(text)

    register_command("Naughty", "rumor", "Generate a wild rumor about someone", [])

    # 56. SECRET
    @app.on_message(filters.command("secret", prefixes=".") & filters.me)
    async def secret_cmd(client, message):
        name = _get_target_name(client, message)
        secret = random.choice(_SECRETS)
        text = f"🤐 **Secret about {name}**\n\n{secret}"
        await message.edit(text)

    register_command("Naughty", "secret", "Reveal a 'secret' about someone", [])

    # 57. DOSSIER
    @app.on_message(filters.command("dossier", prefixes=".") & filters.me)
    async def dossier_cmd(client, message):
        name = _get_target_name(client, message)
        chaos = _deterministic_score(name, "chaos")
        charm = _deterministic_score(name, "charm")
        threat = _deterministic_score(name, "threat")
        humor = _deterministic_score(name, "humor")
        text = (
            f"📁 **CLASSIFIED DOSSIER**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"👤 Subject: **{name}**\n"
            f"🌀 Chaos Level: `{chaos}%`\n"
            f"✨ Charm Level: `{charm}%`\n"
            f"⚠️ Threat Level: `{threat}%`\n"
            f"😂 Humor Level: `{humor}%`\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🔒 Classification: **{'TOP SECRET' if threat > 70 else 'CLASSIFIED' if threat > 40 else 'PUBLIC'}**"
        )
        await message.edit(text)

    register_command("Naughty", "dossier", "Generate a classified dossier", [])

    # 58. REVIEW
    @app.on_message(filters.command("review", prefixes=".") & filters.me)
    async def review_cmd(client, message):
        name = _get_target_name(client, message)
        review = random.choice(_REVIEWS)
        text = f"📝 **Review of {name}**\n\n{review}"
        await message.edit(text)

    register_command("Naughty", "review", "Write a humorous review of someone", [])

    # 59. YELP
    @app.on_message(filters.command("yelp", prefixes=".") & filters.me)
    async def yelp_cmd(client, message):
        name = _get_target_name(client, message)
        review = random.choice(_YELPS)
        text = f"📱 **Yelp Review: {name}**\n\n{review}"
        await message.edit(text)

    register_command("Naughty", "yelp", "Yelp-style review of someone", [])

    # 60. REPORT
    @app.on_message(filters.command("report", prefixes=".") & filters.me)
    async def report_cmd(client, message):
        name = _get_target_name(client, message)
        report = random.choice(_REPORTS).replace("[Name]", name)
        await message.edit(report)

    register_command("Naughty", "report", "Generate an official report", [])

    # 61. WARRANT
    @app.on_message(filters.command("warrant", prefixes=".") & filters.me)
    async def warrant_cmd(client, message):
        name = _get_target_name(client, message)
        warrant = random.choice(_WARRANTS).replace("[Name]", name)
        await message.edit(warrant)

    register_command("Naughty", "warrant", "Issue a warrant for someone", [])

    # 62. INDICTMENT
    @app.on_message(filters.command("indictment", prefixes=".") & filters.me)
    async def indictment_cmd(client, message):
        name = _get_target_name(client, message)
        indictment = random.choice(_INDICTMENTS).replace("[Name]", name)
        await message.edit(indictment)

    register_command("Naughty", "indictment", "Draft an indictment for someone", [])

    # 63. DIAGNOSIS
    @app.on_message(filters.command("diagnosis", prefixes=".") & filters.me)
    async def diagnosis_cmd(client, message):
        name = _get_target_name(client, message)
        diag = random.choice(_DIAGNOSES).replace("[Name]", name)
        await message.edit(diag)

    register_command("Naughty", "diagnosis", "Diagnose someone humorously", [])

    # 64. PERSONALITYTYPE
    @app.on_message(filters.command("personalitytype", prefixes=".") & filters.me)
    async def personalitytype_cmd(client, message):
        name = _get_target_name(client, message)
        ptype = random.choice(_PERSONALITY_TYPES)
        text = f"🧪 **Personality Analysis: {name}**\n\n{ptype}"
        await message.edit(text)

    register_command("Naughty", "personalitytype", "Reveal someone's personality type", [])

    # 65. COMPATIBILITY
    @app.on_message(filters.command("compatibility", prefixes=".") & filters.me)
    async def compatibility_cmd(client, message):
        compat = random.choice(_COMPATIBILITIES)
        await message.edit(compat)

    register_command("Naughty", "compatibility", "Check compatibility report", [])

    # 66. LOVELETTER
    @app.on_message(filters.command("loveletter", prefixes=".") & filters.me)
    async def loveletter_cmd(client, message):
        name = _get_target_name(client, message)
        letter = random.choice(_LOVELETTERS).replace("[Name]", name)
        await message.edit(letter)

    register_command("Naughty", "loveletter", "Generate a love letter", [])

    # ═══════════════════════════════════════════════════════════════
    #  INTERACTIVE DATA & COMMANDS (17 commands)
    # ═══════════════════════════════════════════════════════════════

    _INTERACTIONS = {
        "spank": {
            "emoji": "👋", "action": "spanks",
            "texts": [
                "Get over my knee!", "Naughty naughty!", "That'll teach you!",
                "Surprise spanking incoming!", "Deserved that one!",
                "The spank of justice!", "Spank initialized!",
                "Critical spank deployed!", "Tactical spanking maneuver!",
                "You've been served — a spanking!",
            ]
        },
        "slap": {
            "emoji": "🤚", "action": "slaps",
            "texts": [
                "Get a taste of this!", "Slap attack!", "Right across the face!",
                "Consider yourself slapped!", "The hand of justice!",
                "Slap reflex activated!", "Quick draw slap!",
                "The five-finger discount!", "High-speed slap delivered!",
                "Slap certified and delivered!",
            ]
        },
        "punch": {
            "emoji": "👊", "action": "punches",
            "texts": [
                "Knockout incoming!", "Right in the kisser!", "Fist of fury!",
                "Super punch activated!", "The one-inch punch!",
                "Punch card: all slots filled!", "Punching at full power!",
                "Critical hit! It's super effective!", "The People's Punch!",
                "Haymaker delivered!",
            ]
        },
        "kick2": {
            "emoji": "🦵", "action": "kicks",
            "texts": [
                "Roundhouse kick!", "Drop kick activated!", "Flying kick!",
                "The kick of destiny!", "Shaolin soccer style!",
                "Kick served fresh!", "Tactical kick maneuver!",
                "Spin kick combo!", "The forbidden kick technique!",
                "Kick launched successfully!",
            ]
        },
        "hug": {
            "emoji": "🤗", "action": "hugs",
            "texts": [
                "Come here, you!", "The warmest hug!", "Squeeze tight!",
                "Hug protocol initiated!", "Maximum comfort hug!",
                "The healing hug!", "Bear hug engaged!",
                "The kind of hug that fixes everything!", "Hug.exe running!",
                "A hug so warm it could melt ice!",
            ]
        },
        "kiss": {
            "emoji": "😘", "action": "kisses",
            "texts": [
                "Mwah!", "A gentle peck!", "Smooch delivered!",
                "Kiss attack!", "The sweetest kiss!",
                "Forehead kiss of protection!", "Kiss launched at target!",
                "A kiss so nice, they said it twice!", "Boop kiss combo!",
                "Air kiss with style!",
            ]
        },
        "pat": {
            "emoji": "👋", "action": "pats",
            "texts": [
                "Good job!", "There, there!", "Pats for comfort!",
                "You did great!", "A reassuring pat!",
                "Pat pat pat!", "The world needs more pats!",
                "Encouragement pat delivered!", "Motivational pat!",
                "You deserve this pat!",
            ]
        },
        "headpat": {
            "emoji": "🤚", "action": "headpats",
            "texts": [
                "Soft headpat!", "You're doing amazing, sweetie!",
                "Protect at all costs!", "Headpat of approval!",
                "Maximum headpat power!", "The supreme headpat!",
                "Headpat for good behavior!", "Quality headpats right here!",
                "Headpat.exe has stopped working (too wholesome)!",
                "Legendary headpat!",
            ]
        },
        "cuddle": {
            "emoji": "🥰", "action": "cuddles",
            "texts": [
                "Snuggle time!", "Maximum cuddle mode!",
                "The coziest cuddle!", "Blanket fort cuddle!",
                "Cuddle puddle achieved!", "Premium cuddle service!",
                "The kind of cuddle that cures sadness!",
                "Ultra cuddle combo!", "Safety cuddle deployed!",
                "Cuddle: the ultimate comfort!",
            ]
        },
        "poke": {
            "emoji": "👉", "action": "pokes",
            "texts": [
                "Poke!", "Hey, notice me!", "Poke poke!",
                "Boop!", "Poke of curiosity!", "The interrogative poke!",
                "Poke and run!", "Strategic poke deployed!",
                "Poke for attention!", "Surprise poke!",
            ]
        },
        "bite": {
            "emoji": "🦷", "action": "bites",
            "texts": [
                "Nom nom!", "Vampire mode activated!",
                "A tiny nibble!", "The love bite!",
                "Bite sized affection!", "Snack detected, bite initiated!",
                "The friendliest bite!", "Cookie monster bite!",
                "Bite of friendship!", "Gentle nibble attack!",
            ]
        },
        "lick": {
            "emoji": "👅", "action": "licks",
            "texts": [
                "Lick!", "The puppy lick!", "Taste test complete!",
                "Random lick attack!", "Cactus mode — all licks!",
                "Quality check lick!", "The ice cream approach!",
                "Lick of curiosity!", "Did I just get licked?",
                "The friendship lick!",
            ]
        },
        "tickle": {
            "emoji": "🪶", "action": "tickles",
            "texts": [
                "Tickle fight!", "The ultimate tickle!",
                "Tickle monster incoming!", "Can't escape the tickle!",
                "Tickle attack launched!", "Surprise tickle!",
                "The feather of doom!", "Giggle inducer deployed!",
                "Tickle protocol engaged!", "Maximum tickle intensity!",
            ]
        },
        "highfive": {
            "emoji": "🙌", "action": "high-fives",
            "texts": [
                "Up top!", "The legendary high-five!",
                "High-five excellence!", "That satisfying clap!",
                "Premium high-five delivered!", "The People's High-Five!",
                "High-five of destiny!", "Epic high-five!",
                "High-five for being awesome!", "The perfect high-five!",
            ]
        },
        "fistbump": {
            "emoji": "👊", "action": "fist-bumps",
            "texts": [
                "Bro moment!", "The ultimate fist bump!",
                "Fist bump of brotherhood!", "Respect!",
                "The cool fist bump!", "Fist bump activated!",
                "Maximum respect fist bump!", "The bro-fist!",
                "Fist bump of legends!", "Professional fist bump!",
            ]
        },
        "nom": {
            "emoji": "🍪", "action": "noms on",
            "texts": [
                "Nom nom nom!", "Snack acquired!",
                "Delicious!", "The cutest nom!",
                "Nom of approval!", "Tiny nom attack!",
                "Adorable nom delivered!", "Nom.exe running!",
                "Nomming intensifies!", "The friendliest nom!",
            ]
        },
        "glomp": {
            "emoji": "🤭", "action": "glomps",
            "texts": [
                "Surprise tackle hug!", "The running glomp!",
                "Glomp attack from nowhere!", "Full body tackle hug!",
                "Maximum velocity glomp!", "The anime glomp!",
                "Glomp of pure excitement!", "Supersonic glomp!",
                "The tackle-glomp combo!", "Glomp initiated with love!",
            ]
        },
    }

    # Generate all 17 interactive commands
    for _iname, _idata in _INTERACTIONS.items():
        # Create handler dynamically
        def _make_handler(data):
            async def _handler(client, message):
                name = _get_target_name(client, message)
                emoji = data["emoji"]
                action = data["action"]
                flavor = random.choice(data["texts"])
                me = await client.get_me()
                my_name = me.first_name
                text = f"{emoji} **{my_name} {action} {name}!**\n\n_{flavor}_"
                await message.edit(text)
            return _handler

        handler = _make_handler(_idata)
        # Register with app
        app.on_message(filters.command(_iname, prefixes=".") & filters.me)(handler)

        # Register command info
        help_text = f"{_idata['action'].capitalize()} someone with flavor text"
        register_command("Naughty", _iname, help_text, [])

    # Command number mapping for interactive:
    # 67. spank
    # 68. slap
    # 69. punch
    # 70. kick2
    # 71. hug
    # 72. kiss
    # 73. pat
    # 74. headpat
    # 75. cuddle
    # 76. poke
    # 77. bite
    # 78. lick
    # 79. tickle
    # 80. highfive
    # 81. fistbump
    # 82. nom
    # 83. glomp

import asyncio
import urllib.request as url
import json
import fuzzysearch as fs
import random as rand
import re
from nextcord.ext import commands
from configparser import ConfigParser as cp

config = cp()
config.read("litbot_config.ini")
discord_API = config["Discord"]["discord_API"]

bot = commands.Bot(command_prefix='!', case_insensitive = True)



class Quotes(commands.Cog):
    quotes = []
    
    def __init__(self, bot):
        self.bot = bot
        self.quotes = self.get_quotes()

    def get_quotes(self):
        file = open("quotes.txt", 'r', encoding = "utf8")
        current_quote = []
        quotes = []
        for line in file:
            if line == '\n' or line == "":
                quotes.append(" ".join(current_quote))
                current_quote = []
            
            else:
                line = line.replace('\n', "")
                current_quote.append(line)
        quotes.append(" ".join(current_quote))
        file.close()
        return quotes

    @commands.command()
    async def quote(self, ctx, *args):
        try:
            if len(args) == 0:
                entry = rand.choice(self.quotes)
                
                await ctx.send(entry)
                return
            else:
                string = " ".join(args)
                
                matches = []
                mindists = []
                candidates = []
                for i in range(len(self.quotes)):
                    quote = fs.find_near_matches(string, self.quotes[i], max_l_dist = 1)
                    if quote != []:
                        dists = []
                        
                        
                        
                        for j in range(len(quote)):
                            dists.append(quote[j]. dist)
                        dist = min(dists)
                        mindists.append(dist)
                        match = len(quote)
                        matches.append(match)
                        criteria = [dist, match, i]
                        
                        candidates.append(criteria)
                        
                
                mindist = min(mindists)
                
                
                
                advancers = [x for x in candidates if x[0] <= mindist]
                win_matches = [x[1] for x in advancers]
                maxmatch = max(win_matches)
                winners = [x for x in advancers if x[1] >= maxmatch]
            





                
                send = self.quotes[winners[0][2]]
                await ctx.send(send)
                return
        except Exception as e:
            print(e)
            await ctx.send("Sorry, I can't find any quotes like that in my library :/")

    @commands.command()
    async def addquote(self, ctx, quote):
        affirmitaves = ["yes", "ye", "y", "yeah", "yeah!", "yes!", "sure", "sure!"]
        author = ctx.author
        await ctx.send("Just to confirm, you would like to add (" + quote + ") to my quotes library?")
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        if len(quote) == 0:
            await ctx.send("You didn't quote anything!")
            return
        
        try:
         msg = await bot.wait_for("message", check=check, timeout=30) # 30 seconds to reply
         if msg.content in affirmitaves:
            file = open("quotes.txt", 'a', encoding = "utf8")
            file.write('\n')
            file.write(quote)
            file.close()    
            self.quotes = self.get_quotes()
            await ctx.send("Quote added successfully :)")
            return
         else:
             await ctx.send("I won't add it, then!")
             return
        except asyncio.TimeoutError:
            await ctx.send(f"You left me hanging! :( {author.mention}")
            return
     
class Dictionary(commands.Cog):
    dictAPI = config["Merriam-Webster"]["dictAPI"]
    thesAPI = config["Merriam-Webster"]["thesAPI"]
    obscure_sorrows_dict = {"adomania":  "n. the sense that the future is arriving ahead of schedule, that all those years with fantastical names like '2013' are bursting from their hypothetical cages into the arena of the present, furiously bucking the grip of your expectations while you lean and slip in your saddle, one hand reaching for reins, the other waving up high like a schoolkid who finally knows the answer to the question.", "adronitis":  "n. frustration with how long it takes to get to know someone—spending the first few weeks chatting in their psychological entryway, with each subsequent conversation like entering a different anteroom, each a little closer to the center of the house—wishing instead that you could start there and work your way out, exchanging your deepest secrets first, before easing into casualness, until you've built up enough mystery over the years to ask them where they're from, and what they do for a living.", "agnosthesia":  "n. the state of not knowing how you really feel about something, which forces you to sift through clues hidden in your behavior, as if you were some other person—noticing a twist of acid in your voice, an obscene amount of effort put into something trifling, or an inexplicable weight on your shoulders that makes it difficult to get out of bed.", "aimonomia":  "n. fear that learning the name of something—a bird, a constellation, an attractive stranger—will somehow ruin it, transforming a lucky discovery into a conceptual husk pinned in a glass case, which leaves one less mystery to flutter around your head, trying to get in.", "Altschmerz":  "n. weariness with the same old issues that you’ve always had—the same boring flaws and anxieties you’ve been gnawing on for years, which leaves them soggy and tasteless and inert, with nothing interesting left to think about, nothing left to do but spit them out and wander off to the backyard, ready to dig up some fresher pain you might have buried long ago.", "ambedo":  '''n. a kind of melancholic trance in which you become completely absorbed in vivid sensory details—raindrops skittering down a window, tall trees leaning in the wind, 
clouds of cream swirling in your coffee—which leads to a dawning awareness of the haunting fragility of life, a mood whose only known cure is the vuvuzela.''', "ameneurosis":  '''n. the half-forlorn, half-escapist ache 
of a train whistle calling in the distance at night.''', "anchorage":  "n. the desire to hold on to time as it passes, like trying to keep your grip on a rock in the middle of a river, feeling the weight of the current against your chest while your elders float on downstream, calling over the roar of the rapids, 'Just let go—it's okay—let go.'", "anecdoche":  "n. a conversation in which everyone is talking but nobody is listening, simply overlaying disconnected words like a game of Scrabble, with each player borrowing bits of other anecdotes as a way to increase their own score, until we all run out of things to say.", "antematter":  "n. the dream versions of things in your life, which appear totally foreign but are still somehow yours—your anteschool, your antefriends, your antehome— all part of a parallel world whose gravitational pull raises your life's emotional stakes, increasing the chances you'll end up betting everything you have.", "anthrodynia":  "n. a state of exhaustion with how shitty people can be to each other, typically causing a countervailing sense of affection for things that are sincere but not judgmental, are unabashedly joyful, or just are.", "apomakrysmenophobia":  "n. fear that your connections with people are ultimately shallow, that although your relationships feel congenial at the time, an audit of your life would produce an emotional safety deposit box of low-interest holdings and uninvested windfall profits, which will indicate you were never really at risk of joy, sacrifice or loss.",  "backmasking":  "n. the instinctive tendency to see someone as you knew them in their youth, a burned-in image of grass-stained knees, graffitied backpacks or handfuls of birthday cake superimposed on an adult with a degree, an illusion formed when someone opens the door to your emotional darkroom while the memory is still 'developing.'",  "the bends": '''n. frustration that you're not 
enjoying an experience as much as you should, even something you've worked for years to attain, which prompts you to plug in various thought combinations to try for anything more than static emotional blankness, 
as if your heart had been accidentally demagnetized by a surge of expectations.''', "catoptric tristesse": "n. the sadness that you'll never really know what other people think of you, whether good, bad or if at all—that although we reflect on each other with the sharpness of a mirror, the true picture of how we're coming off somehow reaches us softened and distorted, as if each mirror was preoccupied with twisting around, desperately trying to look itself in the eye.", "chrysalism":  "n. the amniotic tranquility of being indoors during a thunderstorm, listening to waves of rain pattering against the roof like an argument upstairs, whose muffled words are unintelligible but whose crackling release of built-up tension you understand perfectly.", "contact high-five" : "n. an innocuous touch by someone just doing their job—a barber, yoga instructor or friendly waitress—that you enjoy more than you’d like to admit, a feeling of connection so stupefyingly simple that it cheapens the power of the written word, so that by the year 2025, aspiring novelists would be better off just giving people a hug.", "la cuna": "n. a twinge of sadness that there's no frontier left, that as the last explorer trudged with his armies toward a blank spot on the map, he didn't suddenly remember his daughter's upcoming piano recital and turn for home, leaving a new continent unexplored so we could set its mists and mountains aside as a strategic reserve of mystery, if only to answer more of our children's questions with 'Nobody knows! Out there, anything is possible.'", "daguerreologue":  "n. an imaginary interview with an old photo of yourself, an enigmatic figure who still lives in the grainy and color-warped house you grew up in, who may well spend a lot of their day wondering where you are and what you’re doing now, like an old grandma whose kids live far away and don’t call much 'anymore.",  "dead reckoning" :"n. to find yourself bothered by someone's death more than you would have expected, as if you assumed they would always be part of the landscape, like a lighthouse you could pass by for years until the night it suddenly goes dark, leaving you with one less landmark to navigate by—still able to find your bearings, but feeling all that much more adrift.", "deep cut": "n. an emotion you haven’t felt in years that you might have forgotten about completely if your emotional playlist hadn't been left on shuffle—a feeling whose opening riff tugs on all your other neurons like a dog on a leash waiting for you to open the door.", "degrassé":  '''adj. 
entranced and unsettled by the vastness of the universe, experienced in a jolt of recognition that the night sky is not just a wallpaper but a deeply foreign ocean whose currents are steadily carrying off all other castaways, who share our predicament but are already well out of earshot—worlds and stars who would've been lost entirely except for the scrap of light they were able to fling out into the dark, a message in a bottle that's only just now washing up in the Earth's atmosphere, an invitation to a party that already ended a million years ago.''', "dialecstatic":  "adj. hearing a person with a thick accent pronounce a certain phrase—the Texan “cooler,” the South African “bastard,” the Kiwi “thirty years ago”—and wanting them to repeat it over and over until the vowels pool in the air and congeal into a linguistic taffy you could break apart and give as presents.", "dream fever": "n. the intense heat on the skin of a sleeping person, a radioactive byproduct of an idle mind humming with secret delusions which then vaporize when plunged into the cooling bath of reality, thus preventing a meltdown that could endanger those close by, who tolerate the risk because it gives them energy.", "hanker sore": "adj. finding a person so attractive it actually kinda pisses you off.", "heartworm":  "n. a relationship or friendship that you can't get out of your head, which you thought had faded long ago but is still somehow alive and unfinished, like an abandoned campsite whose smoldering embers still have the power to start a forest fire.", "hiybbprqag":  "n. the feeling that everything original has already been done, that the experiment of human culture long ago filled its petri dish and now just feeds on itself, endlessly crossbreeding old clichés into a radioactive ooze of sadness.", "scabulous":  '''adj. proud of a scar on your body, which is an autograph signed to you by a world grateful for 
your continued willingness to play with her, even when you don't feel like it.''', "semaphorism":  '''n. a conversational hint that you have something personal to say on the subject but don't go any further—an emphatic 
nod, a half-told anecdote, an enigmatic 'I know the feeling'—which you place into conversations like those little flags that warn diggers of something buried underground: maybe a cable that secretly powers your house, maybe a fiber-optic link to some foreign country.''' ,"silience":  "n. the kind of unnoticed excellence that carries on around you every day, unremarkably—the hidden talents of friends and coworkers, the fleeting solos of subway buskers, the slapdash eloquence of anonymous users, the unseen portfolios of aspiring artists—which would be renowned as masterpieces if only they’d been appraised by the cartel of popular taste, who assume that brilliance is a rare and precious quality, accidentally overlooking buried jewels that may not be flawless but are still somehow perfect.", "slipcast":  "n. the default expression that your face automatically reverts to when idle— amused, melancholic, pissed off—which occurs when a strong emotion gets buried and forgotten in the psychological laundry of everyday life, leaving you wearing an unintentional vibe of pink or blue or gray, or in rare cases, a tie-dye of sheer madness.", "sonder":  "n. the realization that each random passerby is living a life as vivid and complex as your own—populated with their own ambitions, friends, routines, worries and inherited craziness—an epic story that continues invisibly around you like an anthill sprawling deep underground, with elaborate passageways to thousands of other lives that you’ll never know existed, in which you might appear only once, as an extra sipping coffee in the background, as a blur of traffic passing on the highway, as a lighted window at dusk.", "swish fulfillment" :"n. the feeling of delicate luck after casually tossing something across the room and hitting your target so crisply and perfectly that you feel no desire to even attempt another shot, which is a more compelling argument for the concept of monogamous love than anything sung to a guitar.", "the tilt shift": "n. a phenomenon in which your lived experience seems oddly inconsequential once you put it down on paper, which turns an epic tragicomedy into a sequence of figures on a model train set, assembled in their tiny classrooms and workplaces, wandering along their own cautious and well-trodden paths— peaceable, generic and out of focus.", "trumspringa":  "n. the temptation to step off your career track and become a shepherd in the mountains, following your flock between pastures with a sheepdog and a rifle, watching storms at dusk from the doorway of a small cabin, just the kind of hypnotic diversion that allows your thoughts to make a break for it and wander back to their cubicles in the city.", "vellichor":  "n. the strange wistfulness of used bookstores, which are somehow infused with the passage of time—filled with thousands of old books you’ll never have time to read, each of which is itself locked in its own era, bound and dated and papered over like an old room the author abandoned years ago, a hidden annex littered with thoughts left just as they were on the day they were captured.", "vemödalen":  "n. the frustration of photographing something amazing when thousands of identical photos already exist—the same sunset, the same waterfall, the same curve of a hip, the same closeup of an eye—which can turn a unique subject into something hollow and pulpy and cheap, like a mass-produced piece of furniture you happen to have assembled yourself.", "waldosia":  "n. [Brit. wallesia] a condition characterized by scanning faces in a crowd looking for a specific person who would have no reason to be there, which is your brain's way of checking to see whether they're still in your life, subconsciously patting its emotional pockets before it leaves for the day.", "wytai":  "n. a feature of modern society that suddenly strikes you as absurd and grotesque—from zoos and milk-drinking to organ transplants, life insurance, and fiction—part of the faint background noise of absurdity that reverberates from the moment our ancestors first crawled out of the slime but could not for the life of them remember what they got up to do.", "xeno":  "n. the smallest measurable unit of human connection, typically exchanged between passing strangers—a flirtatious glance, a sympathetic nod, a shared laugh about some odd coincidence—moments that are fleeting and random but still contain powerful emotional nutrients that can alleviate the symptoms of feeling alone.", "Zielschmerz":  "n. the exhilarating dread of finally pursuing a lifelong dream, which requires you to put your true abilities out there to be tested on the open savannah, no longer protected inside the terrarium of hopes and delusions that you created in kindergarten and kept sealed as long as you could, only to break in case of 'emergency'"}
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name = "def")
    async def define(self, ctx, word):
        if str(word) in self.obscure_sorrows_dict:
            await ctx.send(self.obscure_sorrows_dict[str(word)])
            return
        call = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/" + word + "?key=" + self.dictAPI 
        word = url.urlopen(call)
        body = word.read()
        body = json.loads(body)
        message= []
        try:
            for i in range(len(body)):
            
                    defin = body[i]["shortdef"]
                    definit = defin[0]
                    definit.replace("[", "")
                    definit.replace("]", "")
                    message.append(str(i+1) + ". " + definit)
        

            await ctx.send('\n'.join(message))
        except Exception as e:
            print("Error: " + str(e))
            await ctx.send("Sorry, that word is currently not in my dictionary!")

    @commands.command()
    async def ent(self, ctx, word):
        call = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/" + word + "?key=" + self.dictAPI 
        word = url.urlopen(call)
        body = word.read()
        body = json.loads(body)
        message = []
        for i in range(len(body)):
            if "et" in body[i].keys():
                string = body[i]["et"][0][1]
                string = re.sub("\{.*?\}", "", string)
                message.append(string + '\n' + '\n')
        send = "".join(message)
        await ctx.send(send)
        return

    
    @commands.command()
    async def syns(self, ctx, word):
        author = ctx.author
        call = "https://www.dictionaryapi.com/api/v3/references/thesaurus/json/" + word + "?key=" + self.thesAPI 
        word = url.urlopen(call)
        body = word.read()
        body = json.loads(body)
        message = []
        
        if len(body) != 1:
            message.append("I found more than one possible definition in the thesaurus. Which did you mean?")
            for i in range(len(body)):
                    message.append((str(i+1) + ". " + str(body[i]["meta"]["id"]) + ": " + str(body[i]["shortdef"])))
            await ctx.send('\n'.join(message).replace("[","").replace("]",""))
            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel
            try:
                msg = await bot.wait_for("message", check=check, timeout=30) # 30 seconds to reply
                try:
                    choice = int(msg.content)
                    if choice-1 < 0 or choice-1 > len(body):
                        raise IndexError("Choice is not in the list")
                    message = []
                    message.append(str(body[choice-1]["meta"]["id"])+ ": " + str(body[choice-1]["shortdef"]) + '\n' + str(body[choice-1]["meta"]["syns"][0][0]))
                    for i in range(1, len(body[choice-1]["meta"]["syns"])):
                        message.append(body[choice-1]["meta"]["syns"][0][i])
                    await ctx.send(', '.join(message).replace("[","").replace("]",""))
                    return


                except Exception as e:
                    print(body)
                    print("Error: " + str(e))
                    await ctx.send("Sorry, I couldn't find what you were looking for!")
                    return
            except asyncio.TimeoutError:
                await ctx.send(f"You left me hanging! :( {author.mention}")
                return
        message.append(str(body[0]["meta"]["id"])+ ": " + str(body[0]["shortdef"]) + '\n' + str(body[0]["meta"]["syns"][0][0]))
        for i in range(1, len(body[0]["meta"]["syns"])):
            message.append(body[0]["meta"]["syns"][0][i])
        await ctx.send(','.join(message).replace("[","").replace("]",""))
        return
    @commands.command()
    async def sorrows(self, ctx, amount = len(obscure_sorrows_dict)):
            sorrows = list(self.obscure_sorrows_dict.keys())
            trunc_sorrows = sorrows[:amount]
            await ctx.send(", ".join(trunc_sorrows))
            return

class Maintenance(commands.Cog):
    

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name = "naptime")
    @commands.is_owner()
    async def shutdown(self, ctx):
       
        await ctx.send(">:(")
        await bot.close()
        print("Goodnight!")
        return

class WOTD():
    word = ""
    definition = ""
    pronunciation = ""
    entymology = ""
    context = ""
    def wotd():
        request = url.urlopen("https://www.merriam-webster.com/word-of-the-day/")
        data = json.loads(request)
        return

class Rosulae_Material(commands.Cog):
    poems_channel_ID = config["Discord"]["poems_channel_ID"]

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def poem(self, ctx, *args):
        await ctx.send("One moment, please!")
        titles = open("rosulae_poems/rosulae_poem_titles.txt", "r+")
        content = open("rosulae_poems/rosulae_poems.txt", "a")
        links = open("rosulae_poems/rosulae_poem_links.txt", "a")
        title_pattern = r"(\*\*)(\w|\W|\s)+(\*\*)"
        search = " ".join(args)
        channel = self.bot.get_channel(self.poems_channel_ID)
        messages = await ctx.channel.history(limit = 9999).flatten()
        title = ""
        
        for msg in messages:
            print("Working...")
            if search.lower() in msg.content.lower() and "**" in msg.content and msg.author != self.bot.user:
                title = re.search(title_pattern, msg.content)
                if title.group(0) not in titles.read():
                    titles.write(title.group(0) + '\n')
                    content.write(msg.content + '\n')
                    links.write(msg.jump_url + '\n')
                await ctx.send(title.group(0) + ": " + msg.jump_url)
      
        titles.close()
        content.close()
        links.close()                    

                
        print("Done!")
        return




bot.add_cog(Quotes(bot))
bot.add_cog(Dictionary(bot))
bot.add_cog(Maintenance(bot))
bot.add_cog(Rosulae_Material(bot))

bot.run(discord_API)





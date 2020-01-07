# -*- coding: utf-8 -*-
from discord.ext import commands
from pyquery import PyQuery
import urllib.request
from urllib.error import HTTPError
import os
import random
from fuzzywuzzy import fuzz
import markovify
import discord
from .permissions import mod, creator


def Search(input, address):
    # Load the HTML from destination
    input = input.lower()
    fp = urllib.request.urlopen(str(address))
    mybytes = fp.read()
    mystr = mybytes.decode("utf8")
    fp.close()
    pq = PyQuery(mystr)

    # Due to parts of the table contents being in a tags inside td tags rather than directly under td, we need to
    # find all matching results from both to get all the results
    table = (pq("td"))
    allTables = []
    output = ""

    # Iterate over every item found, removing all linebreaks from individual items, and adding a line breaks to the
    # end of each of the items for better formatting
    for item in table:
        formattedItem = ""
        entry = pq(item).closest("tr")
        for stat in entry:
            formattedItem += pq(stat).text().replace("\n", " ")
        formattedItem += "\n"
        allTables.append(formattedItem)

    # Due to the way we find the table entries, we get many duplicates. uncleanOutput holds the output with the
    # duplicates
    uncleanOutput = ""

    for item in allTables:
        if fuzz.partial_ratio(item.lower(), input) > 82:
            uncleanOutput += item

    # Here we remove the duplicates
    seen = set()
    for line in uncleanOutput.splitlines():
        if line not in seen:
            seen.add(line)
            output += line + "\n"

    return output


def GetWikiCharacters():
    charpages = {}
    # Setting up variables for the addresses to be crawled
    address = "https://shadownet.run"
    # next page links dont give the domain in them
    addressmod = "/index.php?title=Category:Player_Characters"

    # while loop because we have an unknown amount of pages on mediawiki
    while True:
        # Load the HTML from destination
        fp = urllib.request.urlopen(str(address + addressmod))
        mybytes = fp.read()
        mystr = mybytes.decode("utf8")
        fp.close()
        pq = PyQuery(mystr)

        # Find all divs
        divs = (pq("div"))

        for div in divs:
            # filter out all that dont have the correct class
            if pq(div).has_class("mw-category-group"):
                # find all character links
                charlist = pq(div)("ul")("li")("a")

                # add all the link titles and hrefs to a dictionary
                for char in charlist:
                    charpages[char.attrib['title']] = char.attrib['href']

        # find all links that have the content "next page"
        linklist = pq("a:Contains('next page')")

        # if the list of links is empty, we are on the last page, and can break
        if linklist.length == 0:
            break
        # otherwise change the addressmod variable to the modifier in the next page link
        else:
            addressmod = linklist[0].attrib['href']

    return charpages


class Shadownet(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(brief="[Number of characters to be generated. Max 25, Default 1]")
    async def chargen(self, ctx, amt: int = 1):

        async with ctx.channel.typing():

            # checking if the amount requested goes over the limit
            limit = 25
            if amt > limit:
                amt = limit

            # loading the model
            with open("chargen.json", 'r') as input:
                model = markovify.Text.from_json(input.read())

            output = "```\n"

            # Generating the requested amount of characters. While loop is used due to having to rerun iteration in the
            # case of a failed generation.
            i = 0
            while i < amt:
                sentence = str(model.make_sentence()) + "\n"
                if sentence != "None\n" or sentence in output:
                    output += sentence
                    i = i + 1

            output += "```"
            input.close()
            await ctx.send(output)

    @chargen.error
    async def chargen_eh(self, ctx: commands.Context, err: Exception):
        await ctx.send("Oh dear, something went wrong here")

    @commands.command(brief="[Character Name]")
    async def character(self, ctx, input: str = None):
        """Displays a shadownet characters wiki page"""
        async with ctx.channel.typing():

            # get all the characters and their wiki pages
            charlinks = GetWikiCharacters()

            highestscore = 0
            highestname = ""

            # get all the keys in the character list
            for char in list(charlinks.keys()):
                # run fuzzysearch for input against the keys
                charscore = fuzz.partial_ratio(char.lower(), input.lower())

                # check if current character scores better than so far highest score
                if charscore > highestscore:
                    # storing the character name and their score
                    highestname = char
                    highestscore = charscore

            # Thank you to https://stackoverflow.com/a/18269491 for this
            try:
                url = f"http://www.shadownet.run{charlinks[highestname]}"
                fp = urllib.request.urlopen(url)
                mybytes = fp.read()
                mystr = mybytes.decode("utf8")
                fp.close()
                pq = PyQuery(mystr)
                output = ""

                # Checking if the character was made with the old or the new character form
                if pq('table.infobox'):
                    # Finding the character infobox
                    infobox = pq('table.infobox > tbody > tr')
                    output = highestname + "\n"
                    # Checking if the character has an image linked
                    try:
                        output += "http://www.shadownet.run" + pq(infobox).find('img').eq(0).attr('src') + "\n"
                    except TypeError:
                        pass
                    output += "```css\n"
                    # Iterate over every item in the box to get the name and value
                    for item in infobox:
                        name = pq(item).find('th').eq(0).text()
                        value = pq(item).find('td').eq(0).text()
                        # If neither of the values are empty, add it to the output
                        if name != "" and value != "":
                            output += "%s: %s\n" % (name, value)

                    output += "```"
                # There are different kinds of infoboxes for characters, this is to deal with them.
                elif pq('div.mw-parser-output'):
                    infobox = pq('div.mw-parser-output').find("table").eq(0)
                    infobox = infobox("tbody > tr")

                    # Everything from here is pretty much a repeat of the other case
                    try:
                        output += "http://www.shadownet.run" + pq(infobox).find('img').eq(0).attr('src') + "\n"
                    except TypeError:
                        pass
                    output += "```css\n"
                    for item in infobox:
                        name = pq(item).find('th').eq(0).text()
                        value = pq(item).find('td').eq(0).text()

                        if name != "" and value != "":
                            output += "%s: %s\n" % (name, value)
                    output += "```"

                    if output == "```css\n```":
                        output = "Character does not have an infobox on the wiki :c"

                else:
                    output = "Im sorry, I have no idea how to display this character. It has probably been created using " \
                             "one of the unsupported forms :c"
            except HTTPError:
                output = "Character not found! 💔"

            await ctx.send(output)

    @character.error
    async def character_eh(self, ctx: commands.Context, err: Exception):
        await ctx.send("You didn't specify a character to look for :c")

    @commands.command()
    async def goodnight(self, ctx):
        """Gives you a random sleepy bunny :3"""
        path = "Resources/Bunny/"
        # Get all the images in the Bunny folder. This means I can just add images there and it will work
        img_list = os.listdir(path)
        # Pick a random one
        img = random.choice(img_list)
        # Post it
        bunny = open(path + img, "rb")
        await ctx.send(file=discord.File(path + img))
        bunny.close()

    @commands.command(brief="[Mode] [Search Term]")
    async def search(self, ctx: commands.Context, mode: str = "help", *, input: str = None):
        """Find stats for Shadowrun 5E"""

        async with ctx.channel.typing():
            output = ""

            # This variable holds the names of the different search modes, and the pages where the mode should search from
            modes = {
                "adept": "http://adragon202.no-ip.org/Shadowrun/index.php/SR5:Adept_Powers_List",
                "armor": "http://adragon202.no-ip.org/Shadowrun/index.php/SR5:Gear_Lists:Armor/Clothing",
                "electronic": "http://adragon202.no-ip.org/Shadowrun/index.php/SR5:Gear_Lists:Electronics",
                "magiGear": "http://adragon202.no-ip.org/Shadowrun/index.php/SR5:Gear_Lists:Magical_Equipment",
                "medical": "http://adragon202.no-ip.org/Shadowrun/index.php/SR5:Gear_Lists:Medical",
                "mentor": "http://adragon202.no-ip.org/Shadowrun/index.php/SR5:Mentor_Spirits_List",
                "misc": "http://adragon202.no-ip.org/Shadowrun/index.php/SR5:Gear_Lists:Others",
                "security": "http://adragon202.no-ip.org/Shadowrun/index.php/SR5:Gear_Lists:Security",
                "spell": "http://adragon202.no-ip.org/Shadowrun/index.php/SR5:Spell_List",
                "spirit": "http://adragon202.no-ip.org/Shadowrun/index.php/SR5:Spirit_List",
                "sprite": "http://adragon202.no-ip.org/Shadowrun/index.php/SR5:Matrix:Sprites",
                "tradition": "http://adragon202.no-ip.org/Shadowrun/index.php/SR5:Magic:Traditions",
                "vehicle": "http://adragon202.no-ip.org/Shadowrun/index.php/SR5:Gear_Lists:Vehicles%5CDrones",
                "vehicleMod": "http://adragon202.no-ip.org/Shadowrun/index.php/SR5:Vehicle_Mods_Lists",
                "ware": "http://adragon202.no-ip.org/Shadowrun/index.php/SR5:Gear_Lists:Cyberware",
                "weapon": "http://adragon202.no-ip.org/Shadowrun/index.php/SR5:Gear_Lists:Weapons"
            }

            # Help message
            if mode.lower() == "help":
                output = "To use the search command, please first designate a mode, and then search term. The modes are " \
                         "as follows:```css\nglobal\n" + '\n'.join(modes) + '``` Global mode searches from every mode ' \
                                                                            'listed. However I do not recommend using it, ' \
                                                                            'as it is considerably slower than the other ' \
                                                                            'modes, and especially with more broad search ' \
                                                                            'terms like "Ares" might not be able to ' \
                                                                            'resolve, as the output would exceed Discords ' \
                                                                            '2,000 character limit. Note that the search ' \
                                                                            'term is case sensitive. PLEASE NOTE, THIS IS ' \
                                                                            'NOT A RULES SOURCE, ONLY USE FOR QUICK ' \
                                                                            'REFERENCE. '

            # Global search mode. This just runs the search for every mode individually before posting the results
            elif mode.lower() == "global":
                output = "```css\n"
                for section in modes:
                    output += Search(input, modes[section])
                output += "```"

            # Normal search the mode simply specifies the address to search from
            else:
                output = "```css\n"
                output += Search(input, modes[mode])
                output += "```"

            if output == "```css\n```":
                output = "Sorry, I couldn't find anything :c"

            await ctx.send(output)

    @search.error
    async def search_eh(self, ctx: commands.Context, err: Exception):
        await ctx.send(
            f"I cant do that :c Please use &search help to figure out what went wrong")

    # Just post a picture, because catalyst
    @commands.command()
    async def because(self, ctx: commands.Context):
        """Catalyst"""
        await ctx.send(file=discord.File("Resources/Other/catalyst.jpg"))

    # Cookie recipe!
    @commands.command()
    async def cookie(self, ctx: commands.Context):
        """Cookies!"""
        await ctx.send("```What you need:\n"
                       "• 2½ cups all-purpose ﬂour\n"
                       "• 1 teaspoon baking soda\n"
                       "• 2 teaspoons cream of tartar\n"
                       "• ½ teaspoon ground cinnamon\n"
                       "• ½ teaspoon sea salt\n"
                       "• 1 cup unsalted butter, sliced\n"
                       "• 1¼ cup dark brown sugar\n"
                       "• ½ cup granulated sugar\n"
                       "• 1 large egg\n"
                       "• 1 egg yolk\n"
                       "• 1 tablespoon vanilla extract\n"
                       "• 1 tablespoon plain Greek yogurt\n"
                       "• 1 cup caramel squares, cut into quarters\n"
                       "• ¼ cup granulated sugar\n"
                       "• 2 teaspoons ground cinnamon\n"
                       "• Coarse sea salt for sprinkling\n"
                       "How to make them:\n"
                       "They are cookies, its not that hard, jeez```")

    @commands.command()
    async def pie(self, ctx: commands.Context):
        """ITS A PIE!"""
        await ctx.send("https://imgur.com/gallery/ZKh8C")

    # So.... This command has been such a pain in the ass that I just cant anymore. I might return to it someday.

    # @commands.command(brief="[Your Timezone] [Your Time] [Target Timezone]]")
    # async def time(self, ctx: commands.Context, ogtimezone: str = "UTC", ogtime: str = "1970/1/1:00:00",
    #                totimezone: str = "UTC"):
    #     await self.client.reply("Sorry, this command is currently WIP :c")
    #     return
    #     # noinspection PyUnreachableCode
    #     """Timezone helper. to display the help page, don't give any arguments"""
    #
    #     # HUGE thanks to Ruby#0437 in discord for fixing my code, and implementing the UTC to GMT conversion
    #
    #     ogtimezone, totimezone = totimezone, ogtimezone
    #     fmt = '%Y/%m/%d:%H:%M'
    #
    #     if ctx.message.content == "&time" or ogtimezone.lower() == "help":
    #         await self.client.reply("```You can use this command in 2 different ways:\n"
    #                                 "You can either use a format of &time [Your Timezone] [Your Time Like Dis HH:MM] "
    #                                 "[Target Timezone], and I will treat it as a time on the current day\n\n"
    #                                 "You can also specify a day, like this: &time [Your Timezone] [Your Time "
    #                                 "YYYY/MM/DD:HH/MM] [Target Timezone], and that way I'll give you an accurate day "
    #                                 "aswell (✿◠‿◠)```")
    #         return
    #
    #     # convert UTC to GMT offset for compatibility with tzinfo
    #     if re.match('^[UTC]', ogtimezone, re.IGNORECASE):
    #         ogtimezone = 'GMT' + ogtimezone[3:]
    #     if re.match('^[UTC]', totimezone, re.IGNORECASE):
    #         totimezone = 'GMT' + totimezone[3:]
    #
    #     # Find the name of the timezone in the list of timezones that pytz has
    #     for tz in pytz.all_timezones:
    #         if ogtimezone.lower() in tz.lower():
    #             ogtimezone = tz
    #             break
    #
    #     # Then the same for the target timezone
    #     for tz in pytz.all_timezones:
    #         if totimezone.lower() in tz.lower():
    #             totimezone = tz
    #             break
    #
    #     ogtime = ogtime.replace(':', '/').split("/")
    #
    #     # converting timezones to pytz tzinfo
    #     ogtimezone_tzinfo = pytz.timezone(ogtimezone)
    #     totimezone_tzinfo = pytz.timezone(totimezone)
    #
    #     # only providing time
    #     if len(ogtime) < 3:
    #
    #         indate = datetime.datetime.now(pytz.timezone(ogtimezone))
    #         intime = datetime.time(int(ogtime[0]), int(ogtime[1]))
    #         inputdate = datetime.datetime.combine(indate, intime)
    #
    #         ogtimelocalized = ogtimezone_tzinfo.localize(inputdate)
    #         output = "```css\n"
    #         output += ogtimezone_tzinfo.zone + "\n"
    #         output += ogtimelocalized.strftime(fmt) + "\n"
    #         output += totimezone_tzinfo.zone + "\n"
    #         output += ogtimelocalized.astimezone(totimezone_tzinfo).strftime(fmt) + "\n"
    #         output += "```"
    #     # providing date
    #     else:
    #         inputdate = datetime.datetime([int(x) for x in ogtime])
    #         ogtimelocalized = ogtimezone_tzinfo.localize(inputdate)
    #
    #         output = "```css\n"
    #         output += pytz.timezone(ogtimezone).zone + "\n"
    #         output += ogtimelocalized.strftime(fmt) + "\n"
    #         output += pytz.timezone(totimezone).zone + "\n"
    #         output += ogtimelocalized.astimezone(totimezone_tzinfo).strftime(fmt) + "\n"
    #         output += "```"
    #
    #     await self.client.reply(output)

    @commands.command(brief="[Item]")
    async def illegal(self, ctx: commands.Context, *, item: str = ""):
        """Checks for legality of the specified thing"""

        async with ctx.channel.typing():

            if item == "":
                await self.client.reply(
                    "You do need to specify what to look for ya dumb dumb. If you were looking just "
                    "for the wiki page, here ya go <https://shadownet.run/Illegal_Things>")
                return

            address = "https://shadownet.run/Illegal_Things"

            fp = urllib.request.urlopen(str(address))
            mybytes = fp.read()
            mystr = mybytes.decode("utf8")
            fp.close()
            pq = PyQuery(mystr)

            table = pq("li")
            output = ""

            for hit in table:
                if fuzz.partial_ratio(str(hit.text).lower(), item.lower()) > 82:
                    output = str(hit.text)
                    break

            if output is not "":
                path = "Resources/Illegal/"
                img_list = os.listdir(path)
                img = random.choice(img_list)
                illegal = open(path + img, "rb")
                await ctx.send(file=discord.File(path + img))
                await ctx.send(
                    f"{output} is banned, sorry :c. Here is a link to the page of illegal things <{address}>")
                illegal.close()

            else:
                await ctx.send(f"{item} is cool! Here is a link to the page of illegal things <{address}>")

    @illegal.error
    async def illegal_eh(self, ctx: commands.Context, err):
        await ctx.send("Ok, how? Something has gone terribly wrong here, please alert Aksu#1010")

    @commands.command()
    async def spook(self, ctx):
        """Get spooked"""
        await ctx.send("Doot Doot", file=discord.File("Resources/Other/doot.png"))

    @commands.command(brief="[Quote]")
    async def quote(self, ctx):
        """Context is for nerds"""
        quoteList = []
        with open('Resources/Other/quotes.txt', 'r') as quoteFile:
            for line in quoteFile:
                if line != "\n":
                    quoteList.append(line)

        await ctx.send(random.choice(quoteList))

    @quote.error
    async def quote_eh(self, ctx: commands.Context, err):
        await ctx.send("Something went wrong. This could be because there's no quotes, or the command might have "
                       "something wrong with it")

    @commands.command(brief="[Quote]")
    async def addquote(self, ctx, *, quote: str):
        """Add a quote"""
        if "\n" in quote:
            await ctx.send("No newlines allowed >:c")
            return
        with open('Resources/Other/quotes.txt', 'a') as quoteFile:
            quoteFile.write(f'\n{str(quote)}')

        await ctx.guild.get_member(114796980739244032).send(f'{ctx.author} added quote: {quote}')
        await ctx.send("Quote Added")

    @addquote.error
    async def addquote_eh(self, ctx: commands.Context, err):
        await ctx.send("Something went wrong.")

    @commands.command()
    async def hatcount(self, ctx):
        hatcount = len(ctx.author.roles) - 1  # Gets the number of roles the user has, and reduces it by 1 to account
        # for the everyone role
        output = f"<@{ctx.author.id}> you have {hatcount} hats."

        if hatcount <= 5:
            output += random.choice([" That's just a few. Its okay, we still love you.",
                                     " That's not that many, but that's fine. ^_^"])
        elif hatcount <= 10:
            output += random.choice([" Nice.",
                                     " That's a good amount of hats!",
                                     " Not bad."])
        elif hatcount <= 15:
            random.choice([" That's a bloody tower you got there.",
                           " Damn.",
                           " You are a big boy/girl now."])
        elif hatcount <= 20:
            random.choice([" Jesus.",
                           " How do you even fit in here?",
                           " Do you play TF2?"])

        await ctx.send(output)


def setup(client: commands.Bot):
    client.add_cog(Shadownet(client))

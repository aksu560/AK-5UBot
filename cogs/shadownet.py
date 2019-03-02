from discord.ext import commands
from pyquery import PyQuery
import urllib.request
from urllib.error import HTTPError
import os
import random
import pytz
import datetime
import math


def Search(input, address):
    # Load the HTML from desstination
    fp = urllib.request.urlopen(str(address))
    mybytes = fp.read()
    mystr = mybytes.decode("utf8")
    fp.close()
    pq = PyQuery(mystr)

    # Due to parts of the table contents being in a tags inside td tags rather than directly under td, we need to
    # find all matching results from both to get all the results
    links = pq(f"a:contains('{input}')").closest("td")
    table = (pq(f"td:contains('{input}')"))
    output = ""

    # Iterate over every item found, removing all linebreaks from individual results, and adding a line breaks to the
    # end of each of the results for better formatting
    for item in links or table:
        entry = pq(item).closest("tr")
        for stat in entry:
            output += pq(stat).text().replace("\n", " ")
        output += "\n"

    return output


class Shadownet(object):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(pass_context=True, brief="[Character Name]")
    async def character(self, ctx, char: str):
        """Displays a shadownet characters wiki page"""
        try:
            fp = urllib.request.urlopen(str(f"http://www.shadownet.run/{char}"))
            mybytes = fp.read()
            mystr = mybytes.decode("utf8")
            fp.close()
            pq = PyQuery(mystr)
            output = ""

            # Checking if the cahracter was made with the old or the new character form
            if pq('table.infobox'):
                # Finding the character infobox
                infobox = pq('table.infobox > tbody > tr')
                output = ""
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

            else:
                output = "Im sorry, I have no idea how to display this character. It has probably been created using " \
                         "one of the unsupported forms :c"
        except HTTPError:
            output = "Character not found! 💔"

        await self.client.reply(output)

    @character.error
    async def character_eh(self, err, ctx: commands.Context):
        await self.client.reply(f"You didn't specify a character to look for :c")

    @commands.command(pass_context=True)
    async def goodnight(self, ctx):
        """Gives you a random sleepy bunny :3"""
        path = "Resources/Bunny/"
        # Get all the images in the Bunny folder. This means I can just add images there and it will work
        img_list = os.listdir(path)
        # Pick a random one
        img = random.choice(img_list)
        # Post it
        bunny = open(path + img, "rb")
        await self.client.send_file(ctx.message.channel, path + img)
        bunny.close()

    @commands.command(pass_context=True, brief="[Mode] [Search Term]")
    async def search(self, ctx: commands.Context, mode: str = "help", *, input: str = None):
        """Find stats for Shadowrun 5E"""

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
                                                                        'term is case sensitive.'

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
            output = "Sorry, I couldnt find anything :c"
        await self.client.reply(output)

    @search.error
    async def search_eh(self, err, ctx: commands.Context):
        await self.client.reply(
            f"I cant do that :c Please use &search help to figure out what went wrong")

    # Just post a picture, because catalyst
    @commands.command(pass_context=True)
    async def because(self, ctx: commands.Context):
        """Catalyst"""
        await self.client.send_file(ctx.message.channel, "Resources/Other/catalyst.jpg")

    # Cookie recipe!
    @commands.command(pass_context=True)
    async def cookie(self, ctx: commands.Context):
        """Cookies!"""
        await self.client.reply("```What you need:\n"
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

    @commands.command(pass_context=True)
    async def pie(self, ctx: commands.Context):
        """ITS A PIE!"""
        await self.client.reply("https://imgur.com/gallery/ZKh8C")

    @commands.command(pass_context=True, brief="[Your Timezone] [YourTtime] [Target Timezone]]")
    async def time(self, ctx: commands.Context, ogtimezone: str = "UTC", ogtime: str = "1970/1/1:00:00",
                   totimezone: str = "UTC"):
        """Timezone helper. to display the help page, don't give any arguments"""
        fmt = '%Y/%m/%d:%H:%M'

        await self.client.reply("Sorry, this command is currently WIP :c")
        return

        if ctx.message.content == "&time" or ogtimezone.lower() == "help":

            await self.client.reply("```You can use this command in 2 different ways:\n"
                                    "You can either use a format of &time [Your Timezone] [Your Time Like Dis HH:MM] "
                                    "[Target Timezone], and I will treat it as a time on the current day\n\n"
                                    "You can also specify a day, like this: &time [Your Timezone] [Your Time "
                                    "YYYY/MM/DD:HH/MM] [Target Timezone], and that way I'll give you an accurate day "
                                    "aswell (✿◠‿◠)```")
            return

        # Find the name of the timezone in the list of timezones that pytz has
        for tz in pytz.all_timezones:
            if ogtimezone.lower() in tz.lower():
                ogtimezone = tz
                break

        # Then the same for the target timezone
        for tz in pytz.all_timezones:
            if totimezone.lower() in tz.lower():
                totimezone = tz
                break

        ogtime = ogtime.replace(':', '/').split("/")

        if len(ogtime) < 3:

            ogtimelocalized = pytz.timezone(ogtimezone).localize(
                datetime.datetime.combine(datetime.datetime.now(pytz.timezone(ogtimezone)), datetime.time(int(ogtime[0]), int(ogtime[1]))))
            output = "```css\n"
            output += pytz.timezone(ogtimezone).zone + "\n"
            output += ogtimelocalized.strftime(fmt) + "\n"
            output += pytz.timezone(totimezone).zone + "\n"
            output += ogtimelocalized.astimezone(pytz.timezone(totimezone)).strftime(fmt) + "\n"
            output += "```"

        else:
            ogtimelocalized = pytz.timezone(ogtimezone).localize(
                datetime.datetime(int(ogtime[0]), int(ogtime[1]), int(ogtime[2]), int(ogtime[3]), int(ogtime[4]), 0))

            output = "```css\n"
            output += pytz.timezone(ogtimezone).zone + "\n"
            output += ogtimelocalized.strftime(fmt) + "\n"
            output += pytz.timezone(totimezone).zone + "\n"
            output += ogtimelocalized.astimezone(pytz.timezone(totimezone)).strftime(fmt) + "\n"
            output += "```"

        await self.client.reply(output)


def setup(client: commands.Bot):
    client.add_cog(Shadownet(client))

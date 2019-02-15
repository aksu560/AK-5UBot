from discord.ext import commands
from pyquery import PyQuery
import urllib.request
from urllib.error import HTTPError
import os
import random


def Search(input, address):
    fp = urllib.request.urlopen(str(address))
    mybytes = fp.read()
    mystr = mybytes.decode("utf8")
    fp.close()
    pq = PyQuery(mystr)

    links = pq(f"a:contains('{input}')").closest("td")
    table = (pq(f"td:contains('{input}')"))
    output = ""
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

            if pq('table.infobox'):
                infobox = pq('table.infobox > tbody > tr')
                output = ""
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
            # There are different kinds of infoboxes for characters, this is to deal with them.
            elif pq('div.mw-parser-output'):
                infobox = pq('div.mw-parser-output').find("table").eq(0)
                infobox = infobox("tbody > tr")

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
        img_list = os.listdir(path)
        img = random.choice(img_list)
        bunny = open(path + img, "rb")
        await self.client.send_file(ctx.message.channel, path + img)
        bunny.close()

    @commands.command(pass_context=True, brief="[Mode] [Search Term]")
    async def search(self, ctx: commands.Context, mode: str = "help", *, input: str = None):
        """Find stats for Shadowrun 5E"""

        output = ""
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

        elif mode.lower() == "global":
            output = "```css\n"
            for section in modes:
                output += Search(input, modes[section])
            output += "```"

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

    @commands.command(pass_context=True)
    async def because(self, ctx: commands.Context):
        """Catalyst"""
        await self.client.send_file(ctx.message.channel, "Resources/Other/catalyst.jpg")

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
        await self.client.reply("https://imgur.com/gallery/ZKh8C")

def setup(client: commands.Bot):
    client.add_cog(Shadownet(client))

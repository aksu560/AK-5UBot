from discord.ext import commands
from pyquery import PyQuery
import urllib.request
from urllib.error import HTTPError
import os
import random


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

    @commands.command(pass_context=True)
    async def weapon(self, ctx, weapon):
        """Find weapon stats for Shadowrun 5E"""
        try:
            fp = urllib.request.urlopen(str(f"http://adragon202.no-ip.org/Shadowrun/index.php/SR5:Gear_Lists:Weapons"))
            mybytes = fp.read()
            mystr = mybytes.decode("utf8")
            fp.close()
            pq = PyQuery(mystr)

            infobox = pq(f"a:contains({weapon})").closest("tr").filter(lambda i: PyQuery("this").text().find(f"{weapon}"))
            foo = infobox[1]
            output = ""
            output += "```css\n"
            for item in infobox:
                data = pq(item).find('td').text()

                if data != "":
                    output += data + "\n"

            output += "```"
        except IndexError:
            output = "No weapons found! 💔"

        await self.client.reply(output)


def setup(client: commands.Bot):
    client.add_cog(Shadownet(client))

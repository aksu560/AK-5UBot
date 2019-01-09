from discord.ext import commands
import discord
from pyquery import PyQuery 
import urllib.request
from urllib.error import HTTPError


class Shadownet(object):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(pass_context=True, brief="[Wiki page]")
    async def character(self, ctx, page: str):
        """Displays a shadownet wiki page"""
        try:
            fp = urllib.request.urlopen(str(f"http://www.shadownet.run/{page}"))
            mybytes = fp.read()
            mystr = mybytes.decode("utf8")
            fp.close()
            pq = PyQuery(mystr)

            infobox = pq('table.infobox > tr')
            output = ""
            try:
                output += "http://www.shadownet.run" + pq(infobox).find('img').eq(0).attr('src')+"\n"
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


def setup(client: commands.Bot):
    client.add_cog(Shadownet(client))
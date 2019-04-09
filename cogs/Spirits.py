# -*- coding: utf-8 -*-
from discord.ext import commands
from .data import spirit


class Spirits(object):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(pass_context=True, brief="[Spirit type] [Force]")
    async def spirit(self, ctx, wanted: str = "", force: int = 6):
        """Get spirit stats"""

        if wanted == "":

            output = 'This is the spirit help command. Use it like so: &spirit [spirit type] [force]\n&spirit fire 6\n'
            output += 'Here is a list of all the spirits:\n'

            output += '```css\n'
            for item in spirit.spirit.index:
                output += item + "\n"
            output += '```'

        else:
            output = str(spirit.spirit.index[wanted.lower()](force))


        await self.client.reply(output)

    @spirit.error
    async def avorion_eh(self, err, ctx: commands.Context):
        await self.client.reply("Sorry, I didnt quite catch that :c")


def setup(client: commands.Bot):
    client.add_cog(Spirits(client))

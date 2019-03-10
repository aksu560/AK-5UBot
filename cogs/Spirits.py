from discord.ext import commands
from .data import spirit


class Spirits(object):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(pass_context=True, brief="[Spirit type] [Force]")
    async def spirit(self, ctx, wanted: str, force: int):
        """Get spirit stats"""

        output = str(spirit.spirit.index[wanted.lower()](force))
        await self.client.reply(output)


def setup(client: commands.Bot):
    client.add_cog(Spirits(client))

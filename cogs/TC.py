# -*- coding: utf-8 -*-
from discord.ext import commands
from .permissions import avorionperm
from requests import get
import importlib


class TC(object):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command()
    async def avorion(self, ctx):
        """Get avorion server IP"""
        importlib.reload(avorionperm)
        if avorionperm.isAvorion(ctx):
            ip = get('https://api.ipify.org').text
            await self.client.send_message(ctx.message.author, f"Server IP: {ip}")
        else:
            raise ValueError

    @avorion.error
    async def avorion_eh(self, ctx: commands.Context, err):
        await self.client.reply("Fug u")


def setup(client: commands.Bot):
    client.add_cog(TC(client))

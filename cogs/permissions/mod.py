from discord.ext import commands


def isMod(ctx: commands.Context):
    return ctx.message.author.guild_permissions.administrator


async def isModAsync(ctx: commands.Context):
    return ctx.message.author.guild_permissions.administrator

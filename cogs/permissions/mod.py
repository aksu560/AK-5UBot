from discord.ext import commands


def isMod(ctx: commands.Context):
    return ctx.message.author.guild_permissions.administrator or ctx.author.id == 114796980739244032


async def isModAsync(ctx: commands.Context):
    return ctx.message.author.guild_permissions.administrator or ctx.author.id == 114796980739244032

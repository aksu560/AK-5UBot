from discord.ext import commands
import configparser

config = configparser.ConfigParser()
config.read(r"cogs\permissions\authorized_users.ini")


def isCreator(ctx: commands.Context):
    return ctx.message.author.id == "114796980739244032"


async def isCreatorAsync(ctx: commands.Context):
    return ctx.message.author.id == "114796980739244032"

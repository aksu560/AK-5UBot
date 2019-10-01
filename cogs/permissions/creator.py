from discord.ext import commands
import configparser

# This is actually not needed. But Ill leave it here, because maybe at some point I can be assed to fix it
# TODO: Fix this to actually read the file
config = configparser.ConfigParser()
config.read(r"cogs\permissions\authorized_users.ini")


# Just checks if the command author's userID matches. This one is mine, replace this with your's if you are hosting
# this by yourself
def isCreator(ctx: commands.Context):
    return ctx.author.id == 114796980739244032


async def isCreatorAsync(ctx: commands.Context):
    return ctx.author.id == 114796980739244032

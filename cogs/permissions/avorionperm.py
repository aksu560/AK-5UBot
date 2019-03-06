from discord.ext import commands
import configparser
import os
import ast

# noinspection PyBroadException
try:
    avoAuth = configparser.ConfigParser()
    avoIni = open(os.getcwd() + "/avorion.ini")
    avoAuth.read_file(avoIni)
    avoUsers = ast.literal_eval(avoAuth.get("avorion", "users"))
    avoIni.close()
except Exception:
    avoUsers = []


def isAvorion(ctx: commands.Context):
    return ctx.message.author.id in avoUsers


async def isAvorionAsync(ctx: commands.Context):
    return ctx.message.author.id in avoUsers

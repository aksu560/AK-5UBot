from discord.ext import commands
import configparser
import os
import ast

# noinspection PyBroadException
try:
    avoAuth = configparser.ConfigParser()
    avoIni = open(os.getcwd() + "/avorion.ini")
    avoAuth.read_file(avoIni)
    avoIni.close()
    avoUsers = ast.literal_eval(avoAuth.get("avorion", "users"))
except Exception:
    avoUsers = []

try:
    creatorAuth = configparser.ConfigParser()
    creatorIni = open(os.getcwd() + "/cogs/permissions/authorized_users.ini")
    creatorAuth.read_file(avoIni)
    creatorIni.close()
    creator = ast.literal_eval(creatorAuth.get("avorion", "users"))
except Exception:
    creator = ""

avoUsers.append(creator)


def isAvorion(ctx: commands.Context):
    return int(ctx.message.author.id) in avoUsers


async def isAvorionAsync(ctx: commands.Context):
    return int(ctx.message.author.id) in avoUsers

from discord.ext import commands
import discord
from .permissions import avorionperm, creator
import os
import configparser
import ast


class TC(object):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(pass_context=True)
    @commands.check(avorionperm.isAvorionAsync)
    async def avorion(self, ctx):
        """Get avorion server IP"""
        ip = os.system('dig +short myip.opendns.com @resolver1.opendns.com')
        await self.client.send_message(ctx.message.author, ip)

    @avorion.error
    async def avorion_eh(self, err: Exception, ctx: commands.Context):
        print(err)
        self.client.reply("Fug u")

    @commands.command(pass_context=True)
    @commands.check(creator.isCreator)
    async def addAvorion(self, ctx, user: discord.Member):
        """Add someone to the Avorion group. All this does is let them use the command"""

        avoAuth = configparser.ConfigParser()

        # We open the file storing the authorized users
        # noinspection PyBroadException
        try:
            avoIni = open(os.getcwd() + "/avorion.ini")
            avoAuth.read_file(avoIni)

            avoUsers = ast.literal_eval(avoAuth.get("avorion", "users"))

        # if that fails, we just create the variable
        except Exception as e:
            print(e)
            avoUsers = []

        # If the user is not already in the file, we write them in it
        if user.id not in avoUsers:
            avoUsers.append(user.id)
            file = f'[avorion]\nusers={str(avoUsers)}'
            avoIni = open(os.getcwd() + "/avorion.ini", 'w', encoding='utf-8')
            avoIni.write(file)
            avoIni.close
            await self.client.add_reaction(ctx.message, '\U00002714')  # React with a black checkmark

        else:
            await self.client.add_reaction(ctx.message, '\U0000274c')  # React with a react with an X

        avoIni.close

    @addAvorion.error
    async def addAvorion_eh(self, c, ctx: commands.Context):
        await self.client.add_reaction(ctx.message, '\U00002753')  # React with a question mark

    @commands.command(pass_context=True)
    @commands.check(creator.isCreator or avorionperm.isAvorionAsync)
    async def removeAvorion(self, ctx, user: discord.Member):
        """Add some one to the Avorion group. All this does is let them use the command"""

        avoAuth = configparser.ConfigParser()

        # We open the file storing the authorized users
        # noinspection PyBroadException
        try:
            avoIni = open(os.getcwd() + "/avorion.ini")
            avoAuth.read_file(avoIni)

            avoUsers = ast.literal_eval(avoAuth.get("avorion", "users"))

        # if that fails, we just create the variable
        except Exception as e:
            print(e)
            avoUsers = []

        # If the user is in file, remove them
        if user.id in avoUsers:
            avoUsers.remove(user.id)
            file = f'[avorion]\nusers={str(avoUsers)}'
            avoIni = open(os.getcwd() + "/avorion.ini", 'w', encoding='utf-8')
            avoIni.write(file)
            avoIni.close
            await self.client.add_reaction(ctx.message, '\U00002714')  # React with a black checkmark

        else:
            await self.client.add_reaction(ctx.message, '\U0000274c')  # React with a react with an X

        avoIni.close

    @removeAvorion.error
    async def removeAvorion_eh(self, ctx: commands.Context):
        await self.client.add_reaction(ctx.message, '\U00002753')  # React with a question mark


def setup(client: commands.Bot):
    client.add_cog(TC(client))

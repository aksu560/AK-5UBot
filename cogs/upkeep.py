from discord.ext import commands
import discord
from .permissions import creator
import configparser
import praw
import os
import markovify
import ast


class Upkeep(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command()
    @commands.check(creator.isCreator)
    async def trainChargen(self, ctx):
        """Train the chargen commands markov chains on the chargen subreddits entries"""

        async with ctx.channel.typing():

            # Reading the required credentials from auth.ini
            redditAuth = configparser.ConfigParser()
            auth = open(os.getcwd() + "/auth.ini")
            redditAuth.read_file(auth)

            redditId = redditAuth.get("reddit", "id")
            redditSecret = redditAuth.get("reddit", "secret")
            redditUser = redditAuth.get("reddit", "user")

            # Creating the required Reddit object
            reddit = praw.Reddit(client_id=redditId, client_secret=redditSecret, user_agent=redditUser)

            # Iterating over every approved character in the /r/shadowchargen subreddit, and storing them in a variable
            characters = []
            for submission in reddit.subreddit('shadowchargen').new(limit=None):
                if submission.link_flair_text == "Approved":
                    characters.append(submission.title)
            output = f"```css\n{len(characters)} characters found\n"

            # Joining that data as a string, characters separated by newlines
            trainingData = "\n".join(characters)

            # noinspection PyBroadException
            # Creating the markov model, and saving it to a file
            try:
                model = markovify.NewlineText(trainingData, state_size=1)

                with open("chargen.json", "w") as file:
                    file.write(model.to_json())

                output += "Model trained\n"
            except Exception as e:
                output += "Model training failed!, check bot console for more information."
                print(e)

            output += "```"

            file.close()
            await ctx.send(output)

    @commands.command()
    @commands.check(creator.isCreator)
    async def reload(self, ctx):
        """Reload all the cogs"""
        reloadMessage = "Reloading cogs:```css\n"
        failedOne = False

        for cog in self.client.allCogs:
            try:
                self.client.unload_extension(cog)
                self.client.load_extension(cog)
                reloadMessage += f"{cog[4:]} - success\n"
            except Exception as err:
                failedOne = True
                reloadMessage += f"{cog[4:]} - failed\n"
                print(f"[reload] Failed to reload cog \"{cog}\" [{type(err).__name__}: {err}]")

        reloadMessage += "```"
        reloadMessage += "**Something's wrong!**" if failedOne == True else ""
        await ctx.send(reloadMessage)

    @commands.command()
    @commands.check(creator.isCreator)
    async def die(self, ctx):
        """Kill the bot"""
        await ctx.send("Time for me to die :<")
        exit()

    @commands.command(brief="[channel/user ID] [message]")
    @commands.check(creator.isCreator)
    async def messageTo(self, ctx, target: str, *, msg: str):
        """Send a custom message to any channel or user"""
        channel = self.client.get_channel(int(target))
        if channel is None:
            channel = await self.client.fetch_user(int(target))
        await channel.send(msg)

    @messageTo.error
    async def messageTo_eh(self, ctx: commands.Context, err: Exception):
        if isinstance(err, commands.MissingRequiredArgument):
            await ctx.send(f"{ctx.author.mention} you forgot something... Baka...")
        elif isinstance(err, commands.CommandInvokeError):
            await ctx.send(f"{ctx.author.mention} invalid channel/user ID... Baka...")

    @commands.command()
    @commands.check(creator.isCreator)
    async def sep(self, ctx):
        """Just sends some separating lines to the server console. Used for debugging"""
        print("-------")


def setup(client: commands.Bot):
    client.add_cog(Upkeep(client))

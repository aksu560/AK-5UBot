from discord.ext import commands
import discord
from .permissions import creator
import configparser
import praw
import os
import markovify


class Upkeep(object):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(pass_context=True)
    @commands.check(creator.isCreator)
    async def trainChargen(self, ctx):
        """Train the chargen commands markov chains on the chargen subreddits entries"""

        await self.client.send_typing(ctx.message.channel)

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
        await self.client.reply(output)

    @commands.command()
    @commands.check(creator.isCreator)
    async def reload(self):
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
        await self.client.say(reloadMessage)

    @commands.command()
    @commands.check(creator.isCreator)
    async def die(self):
        """Kill the bot"""
        await self.client.say("Time for me to die :<")
        exit()

    @commands.command(pass_context=True, brief="[\"playing\"/\"streaming\"/\"listening\"/\"watching\"] [what]")
    @commands.check(creator.isCreator)
    async def status(self, ctx: commands.Context, mode: str, *, what: str):
        """Change my status"""
        mode = ["playing", "streaming", "listening", "watching"].index(mode)
        game = discord.Game(name=what, url="https://www.twitch.tv/Helmerz", type=mode)
        await self.client.change_presence(game=game)
        await self.client.add_reaction(ctx.message, '\U00002714')  # React with a black checkmark

    @status.error
    async def status_eh(self, err: Exception, ctx: commands.Context):
        if isinstance(err, commands.MissingRequiredArgument):
            await self.client.say(f"{ctx.message.author.mention} you forgot something... Baka...")
        elif isinstance(err, commands.CommandInvokeError):
            await self.client.say(f"{ctx.message.author.mention} what the fuck is that mode?")

    @commands.command(brief="[channel/user ID] [message]")
    @commands.check(creator.isCreator)
    async def messageTo(self, target: str, *, msg: str):
        """Send a custom message to any channel or user"""
        channel = self.client.get_channel(target)
        if channel == None:
            channel = await self.client.get_user_info(target)
        await self.client.send_message(channel, msg)

    @messageTo.error
    async def messageTo_eh(self, err: Exception, ctx: commands.Context):
        if isinstance(err, commands.MissingRequiredArgument):
            await self.client.say(f"{ctx.message.author.mention} you forgot something... Baka...")
        elif isinstance(err, commands.CommandInvokeError):
            await self.client.say(f"{ctx.message.author.mention} invalid channel/user ID... Baka...")

    @commands.command()
    @commands.check(creator.isCreator)
    async def sep(self):
        """Just sends some separating lines to the server console. Used for debugging"""
        print("-------")


def setup(client: commands.Bot):
    client.add_cog(Upkeep(client))

# -*- coding: utf-8 -*-
from discord.ext import commands
from cogs.permissions import creator


class Help(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command()
    async def help(self, ctx: commands.Context):
        """Is a very helpful command"""
        commandsText = f"Here are all the commands, {ctx.message.author.mention}:```css\n"

        # Iterate through all commands
        for name, cmd in self.client.all_commands.items():
            # Ignore aliases
            if name != cmd.name:
                continue

            # Dont list Upkeep commands to people who aren't marked as the creator
            if cmd.cog_name in ["Upkeep", "Chat"] and not creator.isCreator(ctx):
                continue

            # Is the cog already stated in the list?
            if f".{cmd.cog_name}\n" not in commandsText:
                commandsText += f".{cmd.cog_name}\n"
            
            commandsText += f"    &{cmd.name} "
            commandsText += f"{cmd.brief} " if cmd.brief != None else ""
            commandsText += f"/* {cmd.help} */\n"

        # Cuts the output to multiple commands if the output would go over Discord's character limit
        if len(commandsText) > 2000:
            texts = []
            pos1 = commandsText.find('\n', 1700, 1900)
            texts.append(commandsText[:pos1] + "```")
            texts.append(f"```css\n{commandsText[pos1:]}```")
            for i in texts:
                await ctx.send(i)
        else:
            await ctx.send(commandsText + "```")


def setup(client: commands.Bot):
    client.add_cog(Help(client))

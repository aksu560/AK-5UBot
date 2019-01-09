from discord.ext import commands
import discord


class Help(object):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(pass_context=True)
    async def help(self, ctx: commands.Context):
        """Is a very helpful command"""
        commandsText = f"Here are all the commands, {ctx.message.author.mention}:```css\n"

        for name, cmd in self.client.commands.items():
            # Ignore aliases
            if name != cmd.name:
                continue
                
            if cmd.cog_name in ["Reload"] and not checks.isCreator(ctx):
                continue
                
            # Is the cog already stated in the list?
            if f".{cmd.cog_name}\n" not in commandsText:
                commandsText += f".{cmd.cog_name}\n"
            
            commandsText += f"    &{cmd.name} "
            commandsText += f"{cmd.brief} " if cmd.brief != None else ""
            commandsText += f"/* {cmd.help} */\n"

        if len(commandsText) > 2000:
            texts = []
            pos1 = commandsText.find('\n', 1700, 1900)
            texts.append(commandsText[:pos1] + "```")
            texts.append(f"```css\n{commandsText[pos1:]}```")
            for i in texts:
                await self.client.say(i)
        else:
            await self.client.say(commandsText + "```")


def setup(client: commands.Bot):
    client.add_cog(Help(client))
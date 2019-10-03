from discord.ext import commands
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer


class Chat(commands.Cog):
    bean = ChatBot(
        'Bean',
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        database='./database.sqlite3'
    )

    def __init__(self, client: commands.Bot):
        self.client = client
        self.trainer = ChatterBotCorpusTrainer(self.bean)
        client.getResponse = self.getResponse

    def getResponse(self, message: str):
        return self.bean.get_response(message)

    @commands.command()
    async def trainChatbot(self, ctx):
        await ctx.send("```\n"
                       "Training Chatbot, please wait"
                       "```")

        self.trainer.train(
            'chatterbot.corpus.english'
        )

        async for message in ctx.channel.history(limit=200):
            if message.author == self.client.user and message.content == "```\nTraining Chatbot, please wait```":
                await message.edit(content="```\n"
                                     "Chatbot Trained"
                                     "```")
                break


def setup(client: commands.Bot):
    client.add_cog(Chat(client))

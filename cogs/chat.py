from discord.ext import commands
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer


class Chat(commands.Cog):

    conversations = {}

    bean = ChatBot(
        'Bean',
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        database='./database.sqlite3'
    )

    def __init__(self, client: commands.Bot):
        self.client = client
        self.trainer = ChatterBotCorpusTrainer(self.bean)
        client.getResponse = self.getResponse  # this way we can access the command in main.py

    def getResponse(self, author_id, message: str):
        if author_id not in self.conversations:
            self.conversations[author_id] = ChatBot(
                                            'Bean',
                                            storage_adapter='chatterbot.storage.SQLStorageAdapter',
                                            database='./database.sqlite3'
            )
            print("New chatbot instance created for a conversation with " + str(author_id))

        return self.conversations[author_id].get_response(message)

    @commands.command()
    async def trainChatbot(self, ctx):
        """Train the chatbot on default english data"""
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

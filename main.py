from discord.ext import commands
import configparser
import logging
import os

# Setting up logging as per discord.py's documentation
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


client = commands.Bot(command_prefix="&")
client.remove_command("help")

# Read our config file (Hey, this 'global' parser works) -tero 2k18
# It didnt -aksu 2k19
client.cfgParser = configparser.ConfigParser()
auth = open(os.getcwd()+"/auth.ini")
client.cfgParser.read_file(auth)

clientKey = client.cfgParser.get("discord", "key")

# Listing all cogs to be loaded. If you are adding a module, add it to the list here
client.allCogs = [
    "cogs.shadownet",
    "cogs.help",
    "cogs.upkeep",
    "cogs.interactive",
    "cogs.TC",
    "cogs.Spirits",
]


@client.event
async def on_ready():
    print("==== Booting Up ====")

    print("Loading cogs...")    
    for cog in client.allCogs:
        try:
            client.load_extension(cog)
            print(f"Successfully loaded cog \"{cog}\"")
        except Exception as err:
            print(f"Failed to load cog \"{cog}\" [{type(err).__name__}: {err}]")

    print(f"-- Connected to {len(client.servers)} servers:")
    for server in client.servers:
        print(f":: {server.name}")

    print("==== Boot Success! ====")
    
# Run the bot with our API key
client.run(clientKey)
from discord.ext import commands
import discord
from io import BytesIO
from PIL import Image, ImageDraw, ImageOps
import aiohttp


# I stole most of this from my roommate https://github.com/TeroJokela/Discord-Bot/blob/master/cogs/picture.py

class Interactive(object):
    def __init__(self, client: commands.Bot):
        self.client = client

    def cookie(self, giverAvatar: BytesIO, receiverAvatar: BytesIO):
        giverAvatar = Image.open(giverAvatar).resize((117, 117)).convert('RGBA')
        receiverAvatar = Image.open(receiverAvatar).resize((117, 117)).convert('RGBA')
        cookieImage = Image.open("Resources/Other/cookie.png")
        baseImage = Image.new("RGB", cookieImage.size).convert('RGBA')
        baseImage.paste(giverAvatar, (107, 115))
        baseImage.paste(receiverAvatar, (260, 52))
        baseImage.paste(cookieImage, (0, 0), cookieImage)
        ret = BytesIO()
        baseImage.save(ret, "PNG")
        ret.seek(0) # Go back to the start of the stream
        return ret

    async def getAvatarBytes(self, user: discord.User):
        async with aiohttp.ClientSession() as session:
            avatarURL = user.avatar_url if user.avatar_url else user.default_avatar_url
            res = await session.get(avatarURL)
            return BytesIO(await res.read())

    @commands.command(pass_context=True, brief="[tag someone]")
    async def givecookie(self, ctx: commands.Context, toGive: discord.Member):
        """Give someone a cookie!"""
        await self.client.send_typing(ctx.message.channel)
        giverAvatarBytes = await self.getAvatarBytes(ctx.message.author)
        receiverAvatarBytes = await self.getAvatarBytes(toGive)

        image = await self.client.loop.run_in_executor(None, self.cookie, giverAvatarBytes, receiverAvatarBytes)

        embed = discord.Embed(description=f"{ctx.message.author.mention} Gave a cookie to {toGive.mention}!",
                              colour=0xFF69B4)
        embed.set_image(url="attachment://Keksi.png")
        # He's got some weird magic stuff here
        msgData = await self.client.http.send_file(ctx.message.channel.id, image, guild_id=ctx.message.server.id,
                                                   filename="Keksi.png", embed=embed.to_dict())
        self.client.connection._create_message(channel=ctx.message.channel, **msgData)

    # @hug.error
    # async def cookie_eh(self, err: Exception, ctx: commands.Context):
    #     await self.client.reply("Wha?")


def setup(client: commands.Bot):
    client.add_cog(Interactive(client))

import datetime

import discord
from discord.ext import commands

from core import basecog
from core.text import text
from core.config import config

boottime = datetime.datetime.now().replace(microsecond=0)

uhoh_ctr = 0


class Base(basecog.Basecog):
    """Basic bot commands."""

    def __init__(self, bot: commands.Bot):
        super().__init__(bot)

    @commands.command(description=text.get("base", "uhoh_desc"))
    async def uhoh(self, ctx):
        global uhoh_ctr

        await ctx.send(text.fill("base", "uh oh", cnt=uhoh_ctr))

    @commands.cooldown(rate=2, per=20.0, type=commands.BucketType.user)
    @commands.command(description=text.get("base", "uptime_desc"))
    async def uptime(self, ctx):
        now = datetime.datetime.now().replace(microsecond=0)
        delta = now - boottime

        embed = self.create_embed(author=ctx.message.author, title="Uptime")
        embed.add_field(name="Boot", value=str(boottime), inline=False)
        embed.add_field(name="Uptime", value=str(delta), inline=False)
        await ctx.send(embed=embed, delete_after=config.delay_embed)
        await self.deleteCommand(ctx)

    @commands.command(description=text.get("base", "ping_desc"))
    async def ping(self, ctx):
        await ctx.send("pong: **{:.2f} s**".format(self.bot.latency))

    @commands.command(hidden=True, description=text.get("base", "pong_desc"))
    async def pong(self, ctx):
        await ctx.send(text.get("base", "really"))

    @commands.command(hidden=True)
    async def guilds(self, ctx):
        message = "```"
        for guild in self.bot.guilds:
            message += f"{guild.name} ({guild.id}) members: {guild.member_count}\n"
        message += "```"
        await ctx.send(message)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def leave(self, ctx, id: int):
        guild = discord.utils.get(self.bot.guilds, id=id)
        if guild is not None:
            await guild.leave()
            await ctx.send("Stejně se mi tam nelíbilo :ok_hand:")
        else:
            await ctx.send("Takový server neznám")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        global uhoh_ctr

        if message.content == "PR":
            await message.channel.send("<https://github.com/Czechbol/Amadeus/pulls>")
        elif message.content == "🔧":
            await message.channel.send("<https://github.com/Czechbol/Amadeus/issues>")
        elif "uh oh" in message.content.lower() and not message.author.bot:
            await message.channel.send("uh oh")
            uhoh_ctr += 1

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        booster_role = discord.utils.get(self.getGuild().roles, id=config.booster_role)

        if booster_role in before.roles:
            before_booster = True
        else:
            before_booster = False

        if booster_role in after.roles:
            after_booster = True
        else:
            after_booster = False

        if not before_booster and not after_booster:
            return
        elif before_booster and after_booster:
            return
        elif not before_booster and after_booster:
            embed = discord.Embed(
                title=text.get("base", "new_server_booster"),
                color=config.color_boost,
                timestamp=datetime.datetime.now().replace(microsecond=0),
            )
        elif before_booster and not after_booster:
            embed = discord.Embed(
                title=text.get("base", "not_booster_anymore"),
                color=config.color_boost,
                timestamp=datetime.datetime.now().replace(microsecond=0),
            )
        embed.set_thumbnail(url=after.avatar_url)
        embed.add_field(name="User", value=f"{after.name}#{after.discriminator}")
        embed.set_footer(text=f"UserID: {after.id}")
        channel = discord.utils.get(self.getGuild().channels, id=config.boost_channel)
        await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Base(bot))

import json
import requests
from datetime import date

import discord
from discord.ext import commands

from core.config import config
from core.text import text
from core import basecog, utils
from config.messages import Messages as messages

class Librarian(basecog.Basecog):
    """Knowledge and information based commands"""
    def __init__(self, bot):
        super().__init__(bot)

    @commands.command(aliases=["svátek"])
    async def svatek(self, ctx):
        url = config.nameday_cz
        res = requests.get(url).json()
        names = []
        for i in res:
            names.append(i["name"])
        await ctx.send(text.fill("librarian", "nameday cz", name=', '.join(names)))

    @commands.command()
    async def meniny(self, ctx):
        url = config.nameday_sk
        res = requests.get(url).json()
        names = []
        for i in res:
            names.append(i["name"])
        await ctx.send(text.fill("librarian", "nameday sk", name=', '.join(names)))

    @commands.command(aliases=["tyden", "týden", "tyzden", "týždeň"])
    async def week(self, ctx: commands.Context):
        """See if the current week is odd or even"""
        starting_week = config.starting_week
        cal_week = date.today().isocalendar()[1]
        stud_week = cal_week - starting_week
        even, odd = "sudý", "lichý"
        cal_type  = even if  cal_week % 2 == 0 else odd
        stud_type = even if stud_week % 2 == 0 else odd

        embed = self._getEmbed(ctx)
        embed.add_field(name="Studijní", value="{} ({})".format(stud_type, stud_week))
        embed.add_field(name="Kalendářní", value="{} ({})".format(cal_type, cal_week))
        await ctx.send(embed=embed)
        await self.deleteCommand(ctx)


    @commands.command(aliases=['pocasi', 'pocasie'])
    async def weather(self, ctx, *args):
        token = config.weather_token
        city = "Brno"
        if(len(args) != 0):
            city = ' '.join(map(str, args))
        url = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&units=metric&lang=cz&appid=" + token
        res = requests.get(url).json()
        
        if(str(res["cod"]) == "200"):
            description = "Aktuální počasí v městě " + res["name"] + ", " + res["sys"]["country"]
            embed=discord.Embed(title="Počasí", description=description)
            image = "http://openweathermap.org/img/w/" + res["weather"][0]["icon"] + ".png"
            embed.set_thumbnail(url=image)
            weather = res["weather"][0]["main"] + " (" + res["weather"][0]["description"] + ")"
            temp = str(res["main"]["temp"]) + "°C"
            feels_temp = str(res["main"]["feels_like"]) + "°C"
            humidity = str(res["main"]["humidity"]) + "%"
            wind = str(res["wind"]["speed"]) + "m/s"
            clouds = str(res["clouds"]["all"]) + "%"
            visibility = str(res["visibility"] / 1000) + " km" if "visibility" in res else "bez dat"
            embed.add_field(name="Počasí", value=weather, inline=False)
            embed.add_field(name="Teplota", value=temp, inline=True)
            embed.add_field(name="Pocitová teplota", value=feels_temp, inline=True)
            embed.add_field(name="Vlhkost", value=humidity, inline=True)
            embed.add_field(name="Vítr", value=wind, inline=True)
            embed.add_field(name="Oblačnost", value=clouds, inline=True)
            embed.add_field(name="Viditelnost", value=visibility, inline=True)
            await ctx.send(embed=embed)
        elif(str(res["cod"]) == "404"):
            await ctx.send("Město nenalezeno")
        elif(str(res["cod"]) == "401"):
            await ctx.send("Rip token")
        else:
            await ctx.send("Město nenalezeno! " + emote.panic + " (" + res["message"] + ")")
        await self.deleteCommand(ctx)


def setup(bot):
    bot.add_cog(Librarian(bot))

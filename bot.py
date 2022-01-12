import os
from discord.ext import commands
from dotenv import load_dotenv
import requests
import keep_alive



bot = commands.Bot(command_prefix='!', case_insensitive = True)

#get summary data to use to create commands
summaryData = requests.get("https://api.covid19tracker.ca/summary").json()['data'][0]
del summaryData["latest_date"]

#create dictionary of commands as keys and the values as part of the keys for the api data
statAccessors = { c.split('_')[1] : c.split('_',1)[-1] for c in summaryData.keys() }

#command to get and return different stats accessed by alias to specificy which stat (ex. cases)
@bot.command(aliases=list(statAccessors.keys()), help = f'For Covid-19 stats call one of { list(statAccessors.keys())} with a location (Canada or the short form of a province)')
async def CovidStats(ctx, *, location="canada"):
    #get summarized data for canada or province specific data from the api
    if location.upper() == "CANADA":
        data = requests.get("https://api.covid19tracker.ca/summary").json()['data'][0]
    else:
        data = requests.get("https://api.covid19tracker.ca/summary/split").json()['data']
        found = False
        for provinceData in data:
            if location.upper() == provinceData["province"]:
                data = provinceData
                found = True
                break
        if not found:
            await ctx.send("Location not found, please specify a province by short form or Canada")
            return
    
    #message the user with the correct statistic
    stat = ctx.invoked_with.lower()
    if stat == "CovidStats":
        stat = "cases"
    await ctx.send(f'There have been {data["total_"+statAccessors[stat]]} {stat} in {location.upper()}, a change of {data["change_"+statAccessors[stat]]} {stat} since yesterday')

#keep bot alive using flask and repl.it
keep_alive()

#login to bot
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot.run(TOKEN)
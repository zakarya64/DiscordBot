import discord
from discord.ext import commands
import asyncio
import os
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import json
import random








# URL thing for COVID stats
my_url = "https://www.nytimes.com/interactive/2021/us/covid-cases.html"
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, "html.parser")










client = commands.Bot(command_prefix = "r! ")




# Starting the bot
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("Prefix is r! | Type r! help for more info"))
    print("Bot is ready.")




@client.command()
async def balance(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()


    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]


    em = discord.Embed(title=f"{ctx.author.name}'s balance", color=discord.Color.red())
    em.add_field(name="Wallet", value=wallet_amt)
    em.add_field(name="Bank balance", value=bank_amt)
    await ctx.send(embed=em)








@client.command()
async def beg(ctx):
    await open_account(ctx.author)


    user = ctx.author


    users = await get_bank_data()


    earnings = random.randrange(101)






    await ctx.send(f"Someone gave you {earnings} coins!")


    users[str(user.id)]["wallet"] += earnings


    with open("bank.json", "w") as f:
        json.dump(users,f)




async def open_account(user):


        users = await get_bank_data()






        if str(user.id) in users:
            return False
        else:
            users[str(user.id)] = {}
            users[str(user.id)]["wallet"] = 0
            users[str(user.id)]["bank"] = 0


        with open("bank.json","w") as f:
            json.dump(users,f)
        return True


async def get_bank_data():
    with open("bank.json", "r") as f:
        users = json.load(f)
    return users




# Command error
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid command, please type in the right command.")


# Gives ping
@client.command()
async def ping(ctx):
    await ctx.send(f"Not pong {round(client.latency * 1000)}ms.")




# Says hi
@client.command()
async def hi(ctx):
    await ctx.send("Hello there.")




# 8 ball message
@client.command(aliases=["8ball"])
async def eightball(ctx, *, question):
    eightballmessages = ["Yeah there's a good chance in that happening.",
                         "YES THAT WILL DEFINITELY HAPPEN!",
                         "DEAR GOD NO WHY WOULD YOU EVER THINK THAT!",
                         "Eh sorry I don't really see it happening.",
                         "There is some potential...",
                         "That could be happening in a way...",
                         "Very strong chance that it will happen."]
    await ctx.send(random.choice(eightballmessages))


# Reminder function 
@client.command()
async def reminder(ctx, time, task):
    def convert(time):
        words = ['s', 'm', 'h', 'd']


        time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600 * 24}


        unit = time[-1]


        if unit not in words:
            return -1
        try:
            val = int(time[:-1])
        except:
            return -2


        return val * time_dict[unit]


    converted_time = convert(time)




    if converted_time == -1:
        await ctx.send("Please type in the time correctly.")
        return


    if converted_time == -2:
        await ctx.send("Please type in an integer.")
        return












    await ctx.send(f"I'll remind you in {time}.")
    await asyncio.sleep(converted_time)
    await ctx.send(f"{ctx.author.mention}, I am reminding you for {task}.")








# DM's a user
@client.command()
async def dm(ctx, member:discord.Member):
    await ctx.send("What would you like to say?")
    def check(m):
        return m.author.id == ctx.author.id


    message = await client.wait_for("message", check=check)
    await ctx.send(f"Just messaged {member}.")


    await member.send(f"{ctx.author.mention} has a message for you:\n"
                      f"{message.content}")








# Tracks COVID stats in the US
@client.command()
async def covid(ctx):
    US = page_soup.find("td", {"class":"bignum cases show-mobile"})
    US2 = page_soup.find("td", {"class":"num cases svelte-6tbkhx"})
    US3 = page_soup.find("td", {"class":"num tests svelte-6tbkhx"})
    US4 = page_soup.find("td", {"class":"num hospitalized svelte-6tbkhx"})
    US5 = page_soup.find("td", {"class": "num deaths svelte-6tbkhx"})
    US6 = page_soup.find("td", {"class": "bignum"})
    US7 = page_soup.find("td", {"class": "num vax td-end"})
    embed = discord.Embed(
        title="United States Coronavirus Statistics",
        colour=discord.Colour.blue()


    )
    embed.set_footer(text="Contact Zakarya#6969 on Discord to request a country/region.")
    embed.add_field(name="7 day average cases", value=f"{US.text}", inline=False)
    embed.add_field(name="Total cases", value=f"{US2.text}", inline=False)
    embed.add_field(name="7 day average tests   ", value=f"{US3.text}", inline=False)
    embed.add_field(name="7 day average hospitalizations", value=f"{US4.text}", inline=False)
    embed.add_field(name="7 day average deaths", value=f"{US5.text}", inline=False)
    embed.add_field(name="Total deaths", value=f"{US6.text}", inline=False)
    embed.add_field(name="Percentage of fully vaccinated people", value=f"{US7.text}", inline=False)
    await ctx.send(embed=embed)
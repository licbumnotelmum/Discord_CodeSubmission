import discord
from discord.ext import commands
from toolkit import failsafe as fn


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="#", intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')



#trial to change to uppercase text
@bot.command()
async def upper(ctx, *, text:str):
    await ctx.send(text.upper())

#trial to find length
@bot.command()
async def count(ctx, *, text:str):
    await ctx.send(f"Length: {len(text)}")

#time to get user info
@bot.command()
async def info(ctx):
    author = ctx.author          # user object
    name = ctx.author.name       # username
    timestamp = ctx.message.created_at  # UTC datetime

    await ctx.send(f"Author: {author}\nName: {name}\nTime: {timestamp}")


@bot.command()
async def submit(ctx, *, text:str):
    segmnt=fn.segment(text)

    user = ctx.author.name                     #############author file naming convention
    timeStamp = ctx.message.created_at

    fn.failSafe(segmnt)        #trycatch impersonator
    
    qNum = segmnt[0]
    fFormat = segmnt[1]
    code = segmnt[2]

    if fn.isInSafeState(qNum,fFormat):
        fn.saveCode()
    else:
        await ctx.send("""wrong question number or wrong file format
Please enter correct question number OR
Please use file format of java or c
""")
    
#    await ctx.send(text) #edit needed




bot.run("MTQxNDg2OTE5NzcwMzYxNDQ2NQ.GlT71E.8LbHRgytxzSSYJkrqmkIBTKqYToTkE4Rb0IajU")

import discord
from discord.ext import commands
import functions as fn
import mysql.connector
from dotenv import load_dotenv
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="#", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')





#displayes user info
@bot.command(help="Displayes user info")
async def info(ctx):
    author = ctx.author               # user object
    name = ctx.author.name               # username
    timestamp = ctx.message.created_at  # UTC datetime
    await ctx.send(f"Author: {author}\nName: {name}\nTime: {timestamp}")

#submits the code to the folder and rewrites table of timestamp and teams
@bot.command(help="Submits of your code to our database")
async def s(ctx, *, text:str):
    await ctx.message.delete()
    user = ctx.author
    timeStamp = ctx.message.created_at
    # print()
    # print(user," at ",timeStamp.time(),sep=" ")
    # print(text)

    segments=fn.segment(text,2)

    if fn.isSafe(text):
        fileFormat={
            "j":".java",
            "c":".c",
            "+":".c++"
        }
        qId=segments[0]
        fForm=segments[1]
        code=segments[2]
        extention=fileFormat[fForm[0]]
        
        fn.saveCode(user, timeStamp, qId, extention, code)
        
        await ctx.send(f"Thank you\n{ctx.author.mention}A Code of {extention} for {qId} has bees saved")
    else:
        
        await ctx.send(f"{ctx.author.mention}\nerror on question number or file type")
        await ctx.send(f"check\n{segments[0]+" "+segments[1]}")

#describes on how to submit code
@bot.command(help="Describes how to submit a code")
async def helpSubmit(ctx):
    text='''
## If you want to submit you code type


 #submit <question_number> <file_Type>
 <rest of your plain code>


## example (Submiting a <code> for question number 5 in C++ lang)


 #submit q5 +
 <code>

__                                        __
__|  file    |   file_type |__
|  java  |           j          |
|  c++   |          +          |
__|  c        |          c          |__


There are few constrains if you encounter an error (follow the example for easier submition)
1. Theres a min limit of 20 charecters for your <code> to be accepted
2. Check if your question numeber is correct
3. Check if your file type is correct for the programing language (submiting an incorrect file type automatically leads to disqualification)

If you or team member has uploaded code for same question, your team's previous code attempt will be ***overwritten***.
Each team has only one code file generated for a question. 
You can answer any number of questions and use #submit as much as you want. But your ***last submit will be accepted as the final code*** for that question

Happy Coding
'''
    
    await ctx.send(text)

#displayes example on how to submit code
@bot.command(help="Displayes an example on how to enter the #s command")
async def example(ctx):
    text='''
    example for a c++ program
#s q4 +
#include<iostream>
using namespace std;
int main(){
 cout<<"HI";
}
'''
    await ctx.send(text)



#register new users
@bot.command(help="Join your team by entering your Team ID")    
async def joinTeam(ctx, *, text:str):
    author = ctx.author

    try:
        teamId = int(text)
    except:
        await ctx.message("please enter your TEAM_ID from the given list")
    role = discord.utils.get(ctx.guild.roles, name="admin")                     # change role to be displayed on team change
    conn,cursor=fn.invokeSql()

    query=f" select sum(Disc_ID in ('{author}')) from members;"
    cursor.execute(query)
    regstd=cursor.fetchall()[0][0]

    query=f"select teams.Team_Name from members , teams  where members.Team_Id=Teams.Team_ID and members.Disc_ID='{author}';"
    cursor.execute(query)
    teamName=cursor.fetchall()[0][0]

    if not(regstd):
        query=f"insert members values({teamId},'{author}')"
        await ctx.send(f"{ctx.author.mention} joined {teamName}")
        print(f"{author} joined {teamName}")
        cursor.execute(query)
        conn.commit()
    else:
        await ctx.send(f"you are alredy enrolled in a team {teamName}\nTo change your team please contact {role.mention}")        
    cursor.close()
    conn.close


# delets user from member table
# @bot.command()
# async def res(ctx):
#     author=ctx.author
#     conn,cursor=fn.invokeSql()
#     query=f"delete from members where Disc_ID='{author}'"
#     cursor.execute(query)
#     await ctx.send(f"removed user {ctx.author.mention}")
#     conn.commit()
#     cursor.close()

load_dotenv()
token=os.getenv("TOKEN")
bot.run(token)

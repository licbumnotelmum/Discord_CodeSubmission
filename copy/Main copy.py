import discord
from discord.ext import commands
import functions_copy as fn
from dotenv import load_dotenv
import os

class MyHelpCommand(commands.DefaultHelpCommand):
    def get_ending_note(self):
        return ("Use `!command` to run a command.\nEach command needs ! before them to run")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents,help_command=MyHelpCommand())

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_member_join(member):
    newUser = discord.utils.get(member.guild.text_channels, name='welcome')
    if newUser:
        await newUser.send(f"Welcome to the server, {member.mention}\nPlease Join your team using #joinTeam command")


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


 !s <question_number> <file_Type>
 <rest of your plain code>


## example (Submiting a <code> for question number 5 in C++ lang)


 #submit q5 +
 <code>

__                                        __
__|  file    |   file_type     |__
|  java  |           j            |
|  c++   |          +           |
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
@bot.command(help="Displayes an example on how to enter the !s command")
async def example(ctx):
    text='''
    example for a c++ program
!s q4 +
#include<iostream>
using namespace std;
int main(){
 cout<<"HI";
}
'''
    await ctx.send(text)

#register new users
@bot.command(help="Join your team by entering your Team ID after the command")    
async def joinTeam(ctx, *, text:str):
    author = ctx.author

    try:
        
        teamId = int(text)
    except:
        await ctx.message("please enter your TEAM_ID from the given list")
    role = discord.utils.get(ctx.guild.roles, name="Admin")                     # change role to be displayed on team change
    conn,cursor=fn.invokeSql()

    query=f" select sum(Disc_ID in ('{author}')) from members;"
    cursor.execute(query)
    regstd=cursor.fetchall()[0][0]
    
    query=f"select teams.Team_Name, members.Disc_ID from members , teams  where members.Team_Id=Teams.Team_ID and members.Disc_ID='{author}';"
    query=f"select Team_Name from teams  where Team_ID='{teamId}';"
    cursor.execute(query)
    try:
        teamName=cursor.fetchall()[0][0]
    except:
        print(teamName)

    print(regstd)
    if not(regstd):
        query=f"insert members values({teamId},'{author}')"
        await ctx.send(f"{ctx.author.mention} joined `{teamName}`")
        print(f"{author} joined {teamName}")
        cursor.execute(query)
        conn.commit()
    else:
        await ctx.send(f"you are alredy enrolled in a team `{teamName}`\nTo change your team please contact {role.mention}")        
    cursor.close()
    conn.close

@bot.command(help="used by admin to List all teams")
@commands.has_any_role("Admin","Moderators")
async def listTeams(ctx):
    conn,cursor=fn.invokeSql()

    query=f"select Team_ID,Team_Name from teams order by team_id;"
    cursor.execute(query)
    rows=cursor.fetchall()
    await ctx.send("# All the recent registered teams have been listed\n## join your team with their Team ID\nTeam ID\tTeam Name")
    for row in rows:
        await ctx.send(f"{row[0]}\t\t\t\t\t{row[1]}")

    cursor.close()
    conn.close()

# delets user from member table
@bot.command(help="used by Admin to remove users from teams")
@commands.has_role("Admin")
async def res(ctx,*, text:str):
    author=text
    conn,cursor=fn.invokeSql()
    query=f"delete from members where Disc_ID='{author}'"
    cursor.execute(query)
    await ctx.send(f"stranded {ctx.author.mention}")
    conn.commit()
    cursor.close()

load_dotenv()
token=os.getenv("TOKEN")
bot.run(token)

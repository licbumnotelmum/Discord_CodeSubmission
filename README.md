# Discord_CodeSubmission
## A bot that helped me automate the process of collecting the codes of different participants in a competation

## *To run the code:*
  step 1: create a `.env` file with certain values \n  
    TOKEN={Your Discord Bot Token}  
    HOST={host for MySqlDb}  
    DBUSER={MySqlDb user}  
    DBPASS={password for DBUSER}  
    DATABASE={Database Name}  
  Step 2:  
    (Keep In Mind the table fields except the Qn fields are to be kept as it is for the queries to perform)  
    configure `MySqlSetup.py` crTeamQ function and crTimeSt function to have Question fields according to your liking   
  step 3:  
    Run `MySqlSetup.py` and add teams  
  step 4:  
    Run `Main.py` (Go through the commands and role commands that have been premade)  
  Step 5:  
    (Admins or mods can display the Team_ID and Team_Name using the command !listTeams in discord)  
    make sure before submitting the code, The discord members have joined team by using the `!joinTeam <Team_Id>`  
    (make sure everyone has joined their teams, _no warning will be given_ if submission without team takes place)  
    the joinTeam command will bind the discord username to the their team there can be any number of members in a team.  
  step 6:  
    to submit the code in the same message after the line `!s qn ext`.  
    for detailed view and examples, type `!helpSubmit` and `!example` in discoed message  
      
## *Other functionalities*:  
  the bot also has !res <username> command that will unbind the discord user and their team from the database making them unable to submit the code.  
  !info command will display the username  
  
The bot usees my sql database to keep track of the time stamps of the questions submited by the teams.  
database uses 3 tables   
  table 1 (Members)  
    keeps track of discord users and the teams they reside as team ids  
  table 2 (Teams)  
    keeps track of teams with the team id and the question they attempt  
  table 3 (Time_Stamp)  
    keeps track of timestamp  
Teams table has aditional columns that store the file name of the the code. this file name entity is stored in the field of Qn which depicts the question number.  
Files are stored in a sub directory called `codeVault` this codevault stores every entry with the naming schele of TnQn.ext   
  Tn:  depicts the Team_ID in the database  
  Qn:  depicts the question id that the team has attempted to solve  
  ext: reffers to the fiile extenntion  
  

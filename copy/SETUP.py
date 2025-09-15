import mysql.connector
from dotenv import load_dotenv
import os

#select members.Disc_ID , teams.Team_Name from members , teams  where members.Team_Id=Teams.Team_ID;
    
def crMembers(cursor):
    table="Members"
    try:
        cursor.execute(f"CREATE TABLE {table} (Team_ID int ,Disc_ID varchar(50) unique);")
    except:
        print(table)

def crTeamQ(cursor):
    table="Teams"
    try:
      cursor.execute(f"""CREATE TABLE {table}(
                     Team_ID INT AUTO_INCREMENT primary key,
                     Team_Name varchar(50) UNIQUE,
                     Q1 varchar(20),
                     Q2 varchar(20),
                     Q3 varchar(20),
                     Q4 varchar(20),
                     Q5 varchar(20),
                     Q6 varchar(20),
                     Q7 varchar(20),
                     Q8 varchar(20),
                     Q9 varchar(20),
                     Q10 varchar(20),
                     Q11 varchar(20),
                     Q12 varchar(20),
                     Q13 varchar(20),
                     Q14 varchar(20),
                     Q15 varchar(20)
                     );""")
    except:
        print(table)
    
def crTimeSt(cursor):
    table="Time_Stamp"
    try:
      cursor.execute(f"""CREATE TABLE {table}(
                     Team_ID INT AUTO_INCREMENT primary key,
                     Q1 time(6) DEFAULT null,
                     Q2 time(6) DEFAULT null,
                     Q3 time(6) DEFAULT null,
                     Q4 time(6) DEFAULT null,
                     Q5 time(6) DEFAULT null,
                     Q6 time(6) DEFAULT null,
                     Q7 time(6) DEFAULT null,
                     Q8 time(6) DEFAULT null,
                     Q9 time(6) DEFAULT null,
                     Q10 time(6) DEFAULT null,
                     Q11 time(6) DEFAULT null,
                     Q12 time(6) DEFAULT null,
                     Q13 time(6) DEFAULT null,
                     Q14 time(6) DEFAULT null,
                     Q15 time(6) DEFAULT null
                     ) ;""")
    except:
        print(table)

def insert(cursor,table,teamId):
    cursor.execute(f"insert {table}(Team_ID) values({teamId})")
    print("insert into",table)

def populate(cursor,teamName):      #first input in teams teamName -> team id generates -> allcoate discord id
    try:
        cursor.execute(f"insert teams(Team_Name) values('{teamName}');")
        cursor.execute(f"select Team_ID from Teams where team_Name='{teamName}'")

        teamId=cursor.fetchone()[0]
        insert(cursor,"time_stamp",teamId)

        print("your team id is \n\n \t",teamId)
        
    except:
        print("team alredy exists")

def addUser(cursor):
    query=f"select Team_ID, Team_Name from teams;"
    cursor.execute(query)
    rows=cursor.fetchall()
    print("Select Team")
    for row in rows:
        print(row)

    teamId=int(input("enter Team Id\n\t"))
    for row in rows:
        if (teamId in row):
            discId=input("username\n\t")
            cursor.execute(f"insert members values({teamId}, '{discId}');")
            return
    print("invalid team selection")

load_dotenv()
dbUser=os.getenv("DBUSER")  
dbPass=os.getenv("DBPASS")
dataBase=os.getenv("DATABASE")

conn = mysql.connector.connect(host="localhost",user=dbUser,password=dbPass,database=dataBase)
cursor = conn.cursor()

crMembers(cursor)
crTeamQ(cursor)
crTimeSt(cursor)
print(dataBase)

while True:
    cursor=conn.cursor()
    print('''
\n
value   action
1       Add Team
2       Add User
3       List Teams
4       List Users
5       Find User
_       Exit
\n\n\n
''')
    try:
        choice=int(input("\t"))
    except:
        print("Abandoned")
        break
    match choice:
        case 1:
            Team_Name=input("team name \n")           #adds Teams
            if Team_Name:
                populate(cursor,Team_Name)
                conn.commit()
            cursor.close()
        case 2:
            addUser(cursor)                           #adds User
            conn.commit()
            cursor.close()
        case 3:                                       # List teams
            query="select Team_Id,Team_Name from Teams;"
            cursor.execute(query)
            rows=cursor.fetchall()
            for row in rows:
                print(row)
            cursor.close()
        case 4:                                       # List Users
            query="select * from members;"
            cursor.execute(query)
            rows=cursor.fetchall()
            for row in rows:
                print(row)
            cursor.close()
        case 5:                                       # Find User
            user = input("discord user id (get discord id by #info)\n")
            try:
                query=f"select members.Team_ID, teams.Team_Name, members.Disc_ID from members, teams where Disc_ID='{user}' and members.Team_ID=teams.Team_ID;"
                cursor.execute(query)
                rows=cursor.fetchall()
                
                for row in rows:
                    print(row)
            except:
                print(f"The username {user} couldnot be found")
            cursor.close()
        case _:
            print("unknown choice")
            cursor.close()
    cursor.close()


#cursor.execute("drop tables teams,members,Time_Stamp")

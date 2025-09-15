import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()
dbUser=os.getenv("DBUSER")
dbPass=os.getenv("DBPASS")
dataBase="test"
table="members"
print(dbUser,dbPass,dataBase,table,sep=" ")

conn = mysql.connector.connect(host="localhost",user=dbUser,password=dbPass,database=dataBase)
cursor = conn.cursor() 

try:
    cursor.execute(f"drop table {table}")
except:
    x=1
cursor.execute(f"""
CREATE TABLE {table} (
    Team_Name varchar(50),
    Disc_ID varchar(50)
)
""")
conn.commit()
for i in range(1,4):
    for j in range(1,4):
        team="Team"+str(i)
        disc="disc"+str(i)+str(j)
        query=f"insert into {table} values('{team}','{disc}');"
        cursor.execute(query)
conn.commit()
cursor.execute("select * from members;")
list=cursor.fetchall()
for rows in list:
    print(rows)

cursor.close()
conn.close()
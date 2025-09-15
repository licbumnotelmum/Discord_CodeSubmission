import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()
dbUser=os.getenv("DBUSER")
dbPass=os.getenv("DBPASS")
dataBase="test"
table="teams"
print(dbUser,dbPass,dataBase,table,sep=" ")

conn = mysql.connector.connect(host="localhost",user=dbUser,password=dbPass,database=dataBase)
cursor = conn.cursor() 

try:
    cursor.execute(f"drop table {table}")
except:
    x=1
cursor.execute(f"CREATE TABLE {table}(Team_ID INT AUTO_INCREMENT primary key,Team_Name varchar(50) UNIQUE);")
conn.commit()
for i in range(3):
        team="Team"+str(i+1)
        query=f"insert into {table} (Team_Name) values('{team}');"
        cursor.execute(query)
conn.commit()
cursor.execute(f"select * from {table};")
list=cursor.fetchall()
for rows in list:
    print(rows)

cursor.close()
conn.close()
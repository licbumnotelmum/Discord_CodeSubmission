import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()
dbUser=os.getenv("DBUSER")
dbPass=os.getenv("DBPASS")
dataBase="sakila"
table="teams"
#print(dbUser,dbPass,dataBase,table,sep=" ")

conn = mysql.connector.connect(
    host="localhost",
    user=dbUser,
    password=dbPass,
    database=dataBase)
cursor = conn.cursor()

cursor.execute(f"desc {table}")
list=cursor.fetchall()
for rows in list:
    print(rows)

team="Team1"
city="city"
query="insert into teams (lol,city) values( %s , %s );"
values=(team,city)

cursor.execute(query,values)
conn.commit()

cursor.execute(f"select * from {table};")
list=cursor.fetchall()
for rows in list:
    print(rows)

cursor.close()
conn.close()

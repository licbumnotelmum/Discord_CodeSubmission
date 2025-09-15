import mysql.connector
from dotenv import load_dotenv
import os
from datetime import datetime
#x=datetime.datetime(2025-09-12 18:48:13.492000+00:00)  x=datetime(2025,9,12,18,48,13)

load_dotenv()
dbUser=os.getenv("DBUSER")
dbPass=os.getenv("DBPASS")
dataBase="test"
table="timestamp"
print(dbUser,dbPass,dataBase,table,sep=" ")

conn = mysql.connector.connect(host="localhost",user=dbUser,password=dbPass,database=dataBase)
cursor = conn.cursor() 

try:
    cursor.execute(f"drop table {table}")
except:
    x=1
cursor.execute(f"CREATE TABLE {table}(Team_ID INT AUTO_INCREMENT primary key,Time_Stamp time(6) DEFAULT null);")
conn.commit()

x=datetime(2025,9,12,18,48,13,492000)
time=x.time()
print (time)

query=f"insert into {table} (Time_Stamp) values('{time}');"
cursor.execute(query)
conn.commit()

cursor.execute(f"select * from {table};")
list=cursor.fetchall()
for rows in list:
    print(rows)

cursor.close()
conn.close()
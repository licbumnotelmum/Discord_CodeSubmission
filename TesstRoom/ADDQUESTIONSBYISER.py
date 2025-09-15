import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()
dbUser=os.getenv("DBUSER")
dbPass=os.getenv("DBPASS")
dataBase="test"

conn = mysql.connector.connect(host="localhost",user=dbUser,password=dbPass,database=dataBase)
cursor = conn.cursor() 

#gets Team_ID for exchange of Disc_ID 
discId="disc12"
cursor.execute(f"select Team_ID from Teams where Team_Name=(select distinct Team_Name from members where Disc_ID='{discId}');")
teamId=cursor.fetchone()[0]
print(teamId)



cursor.close()
conn.close()
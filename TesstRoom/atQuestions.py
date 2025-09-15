import mysql.connector
from dotenv import load_dotenv
import os
import random

load_dotenv()
dbUser=os.getenv("DBUSER")
dbPass=os.getenv("DBPASS")
dataBase="test"
table="Questions"
print(dbUser,dbPass,dataBase,table,sep=" ")

conn = mysql.connector.connect(host="localhost",user=dbUser,password=dbPass,database=dataBase)
cursor = conn.cursor() 

try:
    cursor.execute(f"drop table {table}")
except:
    x=1

cursor.execute(f"""CREATE TABLE {table}(
               Team_ID INT AUTO_INCREMENT PRIMARY KEY, 
               Q1 varchar(10),
               Q2 varchar(10),
               Q3 varchar(10),
               Q4 varchar(10),
               Q5 varchar(10));""")
conn.commit()
      
for i in range(3):
        Q1=None
        Q2=None
        Q3=None
        Q4=None
        Q5=None

        if random.randint(1,10)>5:
            Q1=""
            Q1="T"+str(i)+"Q1"
        if random.randint(1,10)<5:
            Q2=""
            Q2="T"+str(i)+"Q2"
        if random.randint(1,10)<5:
            Q3=""
            Q3="T"+str(i)+"Q3"
        if random.randint(1,10)<5:
            Q4=""
            Q4="T"+str(i)+"Q4"
        if random.randint(1,10)<5:
            Q5=""
            Q5="T"+str(i)+"Q5"
        
        query = "INSERT INTO Questions(Q1, Q2, Q3, Q4, Q5) VALUES (%s, %s, %s, %s, %s)"
        values = (Q1,Q2,Q3,Q4,Q5)
        cursor.execute(query,values)
conn.commit()
cursor.execute(f"select * from {table};")
list=cursor.fetchall()
for rows in list:
    print(rows)

cursor.close()
conn.close()
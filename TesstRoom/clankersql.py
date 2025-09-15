import mysql.connector
from dotenv import load_dotenv
import os

# Connect to MySQL
# conn = mysql.connector.connect(
#     host="localhost",       # Change if not local
#     user="root",   # Replace with your MySQL username
#     password="667987",  # Replace with your MySQL password
#     database="test"   # Replace with your database name
# )

# cursor = conn.cursor()

load_dotenv()
dbUser=os.getenv("DBUSER")
dbPass=os.getenv("DBPASS")
dataBase="test"
table="teams"
print(dbUser,dbPass,dataBase,table,sep=" ")

conn = mysql.connector.connect(host="localhost",user=dbUser,password=dbPass,database=dataBase)
cursor = conn.cursor() #buffered=True,dictionary=True)

# Example: Create a table (only run once)
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT
)
""")

# --- WRITE DATA ---
def insert_student(name, age):
    sql = "INSERT INTO students (name, age) VALUES (%s, %s)"
    values = (name, age)
    cursor.execute(sql, values)
    conn.commit()
    print("Inserted:", cursor.rowcount, "record(s)")

# --- READ DATA ---
def fetch_students():
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

# Insert example
insert_student("Alice", 21)
insert_student("Bob", 22)

# Fetch example
fetch_students()

# Close connection
cursor.close()
conn.close()

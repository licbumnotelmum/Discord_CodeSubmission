def segment(text,maxSplit=2):
    return text.split(maxsplit=maxSplit)
    
def isSafe(text):
    seg = segment(text,2)
    questions = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']
    languages = "jc+"
    seg[0]=seg[0].lower()           #Q12
    seg[1]=seg[1].lower()           #java
    print(seg[0])
    if (len(seg) != 3):
        return False
    # if (len(seg[0]) != 2):
    #     return False
    if (len(seg[2]) < 20):
        return False
    
    if not(seg[0][1:] in questions):
        return False
    if not(seg[1][0] in languages):
        return False

    return True

def invokeSql():
    import mysql.connector
    import os
    from dotenv import load_dotenv
    load_dotenv()

    dbUser=os.getenv("DBUSER")
    dbPass=os.getenv("DBPASS")
    dataBase=os.getenv("DATABASE")
    conn = mysql.connector.connect(host="localhost",user=dbUser,password=dbPass,database=dataBase)
    cursor = conn.cursor() 
    return conn,cursor
    
def saveFile(Team_Id,qId,extention,code):
    fileFormat = {
        "j":".java",
        "c":".c",
        "+":".cpp"
    }
    Team_Id = str(Team_Id[0][0])
    quId = str(qId[1:])
    print(quId)

    fileName="T"+Team_Id+"Q"+quId

    file="codeVault/"+fileName+extention                 #change file name and file position

    with open(file, 'w') as f:
        f.write(code)

def updateTable(teamId,qId,ext,timeStamp):
    conn,cuntsor=invokeSql()

    # for timestamp table
    table="time_stamp"
    question="Q"+qId[1:]
    query=f"update {table} set {question}='{timeStamp}' where Team_ID={teamId[0][0]} "
    print("60")
    cuntsor.execute(query)
    conn.commit()   
    print(63,query)

    # for questions table
    table="Teams"
    entity="T"+str(teamId[0][0])+question+ext
    query=f"update {table} set {question}='{entity}' where Team_ID={teamId[0][0]}"
    cuntsor.execute(query)
    conn.commit()
    cuntsor.close()

def saveCode(user, timeStamp, qId, extention, code):
    conn,cursor=invokeSql()
    query=f"select Team_Id from members where Disc_ID='{user}';"
    cursor.execute(query)
    Team_Id = cursor.fetchall()
    time=timeStamp.time()
    print(79,Team_Id,user)
    cursor.close()

    saveFile(Team_Id,qId,extention,code)
    updateTable(Team_Id,qId,extention,time)



from codecs import StreamReader
from distutils.log import error
import re
import os
import psycopg2
import datetime

def DB_init(): # 初始化DB配置
    ##本機Database 連線方式
    # DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a yukibot-test').read()[:-1]
    # conn = psycopg2.connect(DATABASE_URL,sslmode='require') #利用前面得到的DATABASE_URL連接上 Heroku 給我們的資料庫。

    ###部屬到Heroku上 Database連線方式
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL,sslmode='require') #利用前面得到的DATABASE_URL連接上 Heroku 給我們的資料庫。

    return conn

def SearchDB() : #顯示資料庫
    conn = DB_init()
    cursor = conn.cursor() #初始化一個可以執行指令的cursor()。
    query = '''select * from account'''
    
    cursor.execute(query) #執行 SQL 指令。

    conn.commit() #用conn.commit()做確認，指令才會真正被執行

    data= []
    while True:
        temp = cursor.fetchone()
        if temp:
            data.append(temp)
        else:
            break
    #執行了指令，就可以利用最後兩行程式碼來關閉cursor以及中斷連線了。
    cursor.close()
            
    conn.close()

    return str(data)

def SearchDrawStraws(UserGuid): #搜尋抽籤次數
        conn = DB_init()
        cursor = conn.cursor() #初始化一個可以執行指令的cursor()。
        query = f'''select DrawStraws_Count from account where UserGuid = '{UserGuid}' '''
        
        cursor.execute(query) #執行 SQL 指令。
        conn.commit() #用conn.commit()做確認，指令才會真正被執行

        temp = cursor.fetchone()

        cursor.close() #最後兩行程式碼來關閉cursor
        conn.close() #以及中斷連線

        return temp[0]

def updateUserData(UserGuid,UserName): #新增使用者資料
        conn = DB_init()
        cursor = conn.cursor() #初始化一個可以執行指令的cursor()。
        records = [(UserGuid,UserName,0,datetime.date.today())]
        table_columns = '(UserGuid, UserName, DrawStraws_Count, date)'

        query = f'''INSERT INTO account {table_columns} VALUES (%s,%s,%s,%s);'''
        
        cursor.executemany(query,records) #執行 SQL 指令。

        conn.commit() #用conn.commit()做確認，指令才會真正被執行

        count = cursor.rowcount

        print("新增了",count,"筆資料")

        cursor.close() #最後兩行程式碼來關閉cursor
        conn.close() #以及中斷連線

def updateCount(UserGuid,DayCount): #新增抽籤次數
    DayCount = SearchDrawStraws(UserGuid)
    if(DayCount < 3):
        conn = DB_init()
        cursor = conn.cursor() #初始化一個可以執行指令的cursor()。
        query = f'''update account set DrawStraws_Count = DrawStraws_Count+1 where UserGuid = '{UserGuid}' '''
        
        cursor.execute(query) #執行 SQL 指令。
        conn.commit() #用conn.commit()做確認，指令才會真正被執行

        cursor.close() #最後兩行程式碼來關閉cursor
        conn.close() #以及中斷連線

        return True
    else:
        return False

def resetDrawStraws(UserGuid = ""): #重置抽籤次數

    conn = DB_init()
    cursor = conn.cursor() #初始化一個可以執行指令的cursor()。
    if(UserGuid != ''):
        query = f'''update account set DrawStraws_Count = 0 where UserGuid = '{UserGuid}' ''' 
    else:
        query = '''update account set DrawStraws_Count = 0 '''
    
    cursor.execute(query) #要執行 SQL 指令。
    conn.commit() #用conn.commit()做確認，指令才會真正被執行

    cursor.close() #最後兩行程式碼來關閉cursor
    conn.close() #以及中斷連線

def updateJudge(msg):
    importmsg = "," + msg
    conn = DB_init()
    cursor = conn.cursor()
    query = f'''Update judge set message = CONCAT(message,'{importmsg}')'''

    cursor.execute(query)
    count = cursor.rowcount
    conn.commit()
    
    cursor.close()
    conn.close()
    
    return count

def searchJudge():
    conn = DB_init()
    cursor = conn.cursor()
    query = '''SELECT message FROM judge'''

    cursor.execute(query)
    conn.commit()

    temp = cursor.fetchone()
    
    cursor.close()
    conn.close()

    exportList = []
    text = ""
    exportMsg = ""

    for string in temp:
        text+=string

    for msg in text:
        if(msg == ','):
            exportList.append(exportMsg)
            exportMsg = ""
        else:
            exportMsg += msg 
    exportList.append(exportMsg)

    # exportText = re.sub("\[|\]|","",str(exportList))
    return exportList
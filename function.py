import os
import psycopg2

# 初始化DB配置
def DB_init():
    DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a yukibot-test').read()[:-1]
    conn = psycopg2.connect(DATABASE_URL,sslmode='require') #利用前面得到的DATABASE_URL連接上 Heroku 給我們的資料庫。
    return conn

def Search():   
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
#搜尋抽籤次數
def SearchDrawStraws(UserGuid):
        conn = DB_init()
        cursor = conn.cursor() #初始化一個可以執行指令的cursor()。
        query = f'''select DrawStraws_Count from account where UserGuid = '{UserGuid}' '''
        
        cursor.execute(query) #執行 SQL 指令。
        conn.commit() #用conn.commit()做確認，指令才會真正被執行

        temp = cursor.fetchone()

        cursor.close() #最後兩行程式碼來關閉cursor
        conn.close() #以及中斷連線

        return temp[0]

#新增抽籤次數
def updateCount(UserGuid,DayCount): 
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

    
    
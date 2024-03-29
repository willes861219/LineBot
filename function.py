from codecs import StreamReader
from distutils.log import error
import re
import os
import psycopg2
import datetime


def DB_init():  # 初始化DB配置
    # # 本機Database 連線方式
    # # 換一個 New App 後，記得改成要連線的DATABASE
    # DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a yukibot-new').read()[:-1]
    # conn = psycopg2.connect(DATABASE_URL,sslmode='require') #利用前面得到的DATABASE_URL連接上 Heroku 給我們的資料庫。

    # 部屬到Heroku上 Database連線方式
    DATABASE_URL = os.environ['DATABASE_URL']
    # 利用前面得到的DATABASE_URL連接上 Heroku 給我們的資料庫。
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')

    return conn


def SearchDB():  # 顯示資料庫
    conn = DB_init()
    cursor = conn.cursor()  # 初始化一個可以執行指令的cursor()。
    query = '''select id,userguid,username,drawstraws_count,cast(date AS VARCHAR),cast(birthday AS VARCHAR) from account order by id'''

    cursor.execute(query)  # 執行 SQL 指令。

    conn.commit()  # 用conn.commit()做確認，指令才會真正被執行

    data = []
    while True:
        temp = cursor.fetchone()
        if temp:
            data.append(temp)
        else:
            break
    # 執行了指令，就可以利用最後兩行程式碼來關閉cursor以及中斷連線了。
    cursor.close()

    conn.close()

    return data


def SearchDrawStraws(UserGuid):  # 搜尋抽籤次數
    conn = DB_init()
    cursor = conn.cursor()  # 初始化一個可以執行指令的cursor()。
    query = '''select DrawStraws_Count from account where UserGuid = %s'''

    cursor.execute(query, [UserGuid])  # 執行 SQL 指令。
    conn.commit()  # 用conn.commit()做確認，指令才會真正被執行

    temp = cursor.fetchone()

    cursor.close()  # 最後兩行程式碼來關閉cursor
    conn.close()  # 以及中斷連線

    return temp[0]


def updateUserData(UserGuid, UserName):  # 新增使用者資料
    conn = DB_init()
    cursor = conn.cursor()  # 初始化一個可以執行指令的cursor()。
    records = [(UserGuid, UserName, 0, datetime.date.today())]
    table_columns = '(UserGuid, UserName, DrawStraws_Count, date)'

    query = f'''INSERT INTO account {table_columns} VALUES (%s,%s,%s,%s);'''

    cursor.executemany(query, records)  # 執行 SQL 指令。

    conn.commit()  # 用conn.commit()做確認，指令才會真正被執行

    count = cursor.rowcount

    print("新增了", count, "筆資料")

    cursor.close()  # 最後兩行程式碼來關閉cursor
    conn.close()  # 以及中斷連線


def updateCount(UserGuid, DayCount):  # 新增抽籤次數
    DayCount = SearchDrawStraws(UserGuid)
    if (DayCount < 3):
        conn = DB_init()
        cursor = conn.cursor()  # 初始化一個可以執行指令的cursor()。
        query = '''update account set DrawStraws_Count = DrawStraws_Count+1 where UserGuid = %s '''

        cursor.execute(query, [UserGuid])  # 執行 SQL 指令。
        conn.commit()  # 用conn.commit()做確認，指令才會真正被執行

        cursor.close()  # 最後兩行程式碼來關閉cursor
        conn.close()  # 以及中斷連線

        return True
    else:
        return False


def resetDrawStraws(UserGuid=""):  # 重置抽籤次數

    conn = DB_init()
    cursor = conn.cursor()  # 初始化一個可以執行指令的cursor()。
    if (UserGuid != ''):
        query = '''update account set DrawStraws_Count = 0 where UserGuid = %s '''
    else:
        query = '''update account set DrawStraws_Count = 0 '''

    cursor.execute(query, [UserGuid])  # 要執行 SQL 指令。
    conn.commit()  # 用conn.commit()做確認，指令才會真正被執行

    cursor.close()  # 最後兩行程式碼來關閉cursor
    conn.close()  # 以及中斷連線


def searchJudge():  # 搜尋黑名單
    conn = DB_init()
    cursor = conn.cursor()
    query = '''SELECT message FROM judge'''

    cursor.execute(query)
    conn.commit()

    temp = cursor.fetchone()

    cursor.close()
    conn.close()

    exportList = []  # 空list
    messages = ""  # 空字串
    exportMsg = ""  # 輸出空字串

    for string in temp:  # tuple for迴圈 撈出tuple的index內容
        messages += string  # 重整成新字串

    # messages範例字串："測試,測試2,測試3,測試4,測試5"
    for message in messages:  # for迴圈 跑messages的各字元
        if (message == ','):  # 字元是',' 就不加進exportMsg而是加入exportList，然後再把exportMsg變為空字串，繼續跑for迴圈直到結束
            exportList.append(exportMsg)
            exportMsg = ""
        else:  # 字元不為 ',' 就加上去
            exportMsg += message

    # 因為最後的字元不會是 ',' 所以上面for迴圈的判斷不會加到最後一個詞 如上範例(測試5讀不到)，所以需要自行把最後一個詞加入至List
    exportList.append(exportMsg)

    return exportList


def updateJudge(msg):  # 更新黑名單
    conn = DB_init()
    cursor = conn.cursor()
    query = '''update judge 
                set message = 
                case 
                when message is null or message = '' then 
                %s 
                else CONCAT(message,%s)
                end'''
    addMsg = f',{msg}'
    cursor.execute(query, (msg, addMsg))
    count = cursor.rowcount
    conn.commit()

    cursor.close()
    conn.close()

    return count


def deleteJudge(msg):  # 刪除黑名單
    lists = searchJudge()
    for list in lists:
        if (msg == list):
            lists.remove(list)
            message = ""
            for list in lists:
                message += list + ','

            conn = DB_init()
            cursor = conn.cursor()

            query = '''update judge set message = %s '''

            cursor.execute(query, [message[:-1]])

            conn.commit()

            cursor.close()
            conn.close()

            return f'''成功從黑名單中刪除 "{msg}"'''
        else:
            continue
    return "未找到相符字串"


def clearJudge():  # 清除黑名單清單
    conn = DB_init()
    cursor = conn.cursor()

    query = '''update judge set message = null '''

    cursor.execute(query)
    conn.commit()
    count = cursor.rowcount

    cursor.close()
    conn.close()

    return count


def searchBirthday():  # 取得今天生日人員GUID清單
    conn = DB_init()
    cursor = conn.cursor()
    query = '''select userguid from account where to_char(birthday,'MM-DD') = to_char(current_date,'MM-DD')'''

    cursor.execute(query)
    conn.commit()

    lists = cursor.fetchall()
    result = []
    cursor.close()
    conn.close()

    for list in lists:
        result.append(list[0])

    return result


def updateBirthday(date, userGuid):
    conn = DB_init()
    cursor = conn.cursor()

    query = '''update account set birthday= %s where userguid = %s '''

    cursor.execute(query, (date, userGuid))
    conn.commit()

    result = cursor.rowcount

    cursor.close()
    conn.close()

    return result


def setClock(date, time, userGuid):
    conn = DB_init()
    cursor = conn.cursor()

    query = '''update account set clockdate= %s,clocktime = %s where userguid = %s '''

    cursor.execute(query, (date, time, userGuid))
    conn.commit()

    result = cursor.rowcount

    cursor.close()
    conn.close()

    return result


def searchClock():
    conn = DB_init()
    cursor = conn.cursor()

    query = f"select username,cast(clockdate as varchar),cast(clocktime as varchar) from account where clockdate is not null and clocktime is not null and clockdate = current_date and clocktime < current_time order by clockdate,clocktime"
    cursor.execute(query)

    conn.commit()

    desc = cursor.description
    column_names = [col[0] for col in desc]
    data = [dict(zip(column_names, row))
            for row in cursor.fetchall()]
    # Lists = []
    # while True:
    #     temp = cursor.fetchone()
    #     if temp:
    #         Lists.append(temp)
    #     else:
    #         break

    cursor.close()
    conn.close()

    return data


def current_Time():
    conn = DB_init()
    cursor = conn.cursor()

    query = "select current_time(2)"

    cursor.execute(query)
    conn.commit()

    temp = cursor.fetchone()

    cursor.close()
    conn.close()

    return str(temp)

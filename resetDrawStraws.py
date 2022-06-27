import os
import psycopg2
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()


#利用scheduled_job()這個函數的第一個參數'cron'，告訴 Python，當幾年幾月幾日幾點幾分幾秒的時候，總而言之就是特定時間，執行下述程式碼。
@sched.scheduled_job('cron', day_of_week='mon-sun', minute='*/2')
def scheduled_job():
    print('========== 重置抽籤次數 =========')
    print('這個工作在每天的晚上12點執行')
    # 利用datetime查詢時間
    print(f'{datetime.datetime.now().ctime()}')
    print('========== 重置抽籤次數  =========')
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL,sslmode='require') #利用前面得到的DATABASE_URL連接上 Heroku 給我們的資料庫。

    cursor = conn.cursor() #初始化一個可以執行指令的cursor()。
    query =  f'''update account set DrawStraws_Count = 0 '''
    
    cursor.execute(query) #執行 SQL 指令。
    conn.commit() #用conn.commit()做確認，指令才會真正被執行

    cursor.close() #最後兩行程式碼來關閉cursor
    conn.close() #以及中斷連線

sched.start()
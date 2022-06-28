import datetime
import urllib.request 
import function as f
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()


#利用scheduled_job()這個函數的第一個參數'cron'，告訴 Python，當幾年幾月幾日幾點幾分幾秒的時候，總而言之就是特定時間，執行下述程式碼。
@sched.scheduled_job('cron', day_of_week='mon-fri', minute='*/20')
def scheduled_job():
    print('========== APScheduler CRON 定時呼叫器 =========')
    print('這個工作將在每過20分鐘執行一次呼叫')
    # 利用datetime查詢時間
    print(f'{datetime.datetime.now().ctime()}')
    print('========== APScheduler CRON 定時呼叫器 =========')

    url = "https://yukibot-test.herokuapp.com/"
    conn = urllib.request.urlopen(url)

    for key, value in conn.getheaders():
        print(key, value)

@sched.scheduled_job('cron', day_of_week='mon-sun', hour='0')
def resetDrawStraws():
    print('========== 重置抽籤次數 =========')
    print('這個工作在每天的晚上12點執行')
    # 利用datetime查詢時間
    print(f'{datetime.datetime.now().ctime()}')
    print('========== 重置抽籤次數  =========')
    f.resetDrawStraws() #重置抽籤次數
    
sched.start()
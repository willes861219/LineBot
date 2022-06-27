import datetime
import urllib.request 
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()


#利用scheduled_job()這個函數的第一個參數'cron'，告訴 Python，當幾年幾月幾日幾點幾分幾秒的時候，總而言之就是特定時間，執行下述程式碼。
@sched.scheduled_job('cron', day_of_week='mon-fri', minute='*/20')
def scheduled_job():
    print('========== APScheduler CRON =========')
    print('This job runs every day */20 min.')
    # 利用datetime查詢時間
    print(f'{datetime.datetime.now().ctime()}')
    print('========== APScheduler CRON =========')

    url = "https://yukibot-test.herokuapp.com/"
    conn = urllib.request.urlopen(url)

    for key, value in conn.getheaders():
        print(key, value)

sched.start()
import urllib.request 
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()


@sched.scheduled_job('cron', day_of_week='mon-fri', second="*/5")
def scheduled_job():
    url = "https://yukibot-test.herokuapp.com/"
    conn = urllib.request.urlopen(url)

    for key, value in conn.getheaders():
        print(key, value)

sched.start()

# @sched.scheduled_job('interval', minutes=3)
# def timed_job():
#     print('This job is run every three minutes.')
# # 利用scheduled_job()這個函數的第一個參數'interval'，告訴 Python，請每隔多少時間，就執行下述程式碼。
# # 以這行程式碼為例，就是希望每隔 3 分鐘執行一次。

# @sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
# def scheduled_job():
#     print('This job is run every weekday at 5pm.')
# #利用scheduled_job()這個函數的第一個參數'cron'，告訴 Python，當幾年幾月幾日幾點幾分幾秒的時候，總而言之就是特定時間，執行下述程式碼。
# #以這行程式碼為例，就是希望星期一到星期五的下午 5 點，都請執行一次。
# sched.start()
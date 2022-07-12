import datetime
import schedule
import threading
import time
import os


def job1():
    print("I'm working for job1")
    #time.sleep(2)
    print("job1:", datetime.datetime.now())


def job2(cmd):
    print("I'm working for job2")
    os.system(cmd)
    print("job2:", datetime.datetime.now())


def job1_task():
    threading.Thread(target=job1).start()


def job2_task():
    threading.Thread(target=job2,args=("python3 clock.py",)).start()  #args傳元組格式

schedule.every(10).seconds.do(job1_task)
schedule.every(30).seconds.do(job2_task)

#while True保持持續運行
while True:
    #schedule.run_pending()是保持schedule一直運行，去查詢上面那一堆的任務，在任務中，就可以設置不同的時間去運行
    schedule.run_pending()
    time.sleep(1)
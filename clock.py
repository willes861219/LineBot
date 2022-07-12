from cgitb import text
from datetime import datetime
import urllib.request 
import function as f
from apscheduler.schedulers.blocking import BlockingScheduler
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError


sched = BlockingScheduler()

# LINE BOT info
line_bot_api = LineBotApi('Oab2kpZ3f0t35+8oYNfTpYbq9T4taRyVminiW9gHGUAbgnWfiWPpUoqmn2LpXEySzWu33oZgZQNY3xHDE67nH6+spvtyxzy7OZy+F3y8LqHYXHPZM7qJenb7ULux0oOcXLbn9Lg5D8oRzfm8ic8NBAdB04t89/1O/w1cDnyilFU=')
myId = 'U8ff193174b01bfa73c2e4e9c178d003c'

#利用scheduled_job()這個函數的第一個參數'cron'，告訴 Python，當幾年幾月幾日幾點幾分幾秒的時候，總而言之就是特定時間，執行下述程式碼。
@sched.scheduled_job('cron', day_of_week='mon-sun', minute='*/20')
def scheduled_job():
    print('========== APScheduler CRON 定時呼叫器 =========')
    print('這個工作將在每過20分鐘執行一次呼叫')
    # 利用datetime查詢時間
    print(f'{datetime.now().ctime()}')
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
    print(f'{datetime.now().ctime()}')
    print('========== 重置抽籤次數  =========')
    f.resetDrawStraws() #重置抽籤次數
    
@sched.scheduled_job('cron', day_of_week='mon-sun', hour='12')
def checkBirthday():
    print('========== 判斷有沒有人生日 =========')
    print('這個工作在每天的中午12點執行')
    # 利用datetime查詢時間
    print(f'現在時間：{datetime.now().ctime()}')
    Lists = f.searchBirthday()
    if Lists != []:
        line_bot_api.multicast(Lists,TextSendMessage(text = '祝你生日快樂'))
        try:
            for List in Lists:
                profile = line_bot_api.get_profile(List)
                print(f'''今天是{profile.display_name}生日''')
                line_bot_api.push_message('Ce0a20c9eea131c7fce6deef569fff38e',TextSendMessage(text=f'''{profile.display_name},祝你生日快樂'''))
        except LineBotApiError as e: 
            print(f'''錯誤訊息：{e}''')
    else :
        print("今天無人生日")
    print('========== 判斷有沒有人生日 =========')


# @sched.scheduled_job('cron', day_of_week='mon-sun', hour='',minute='*/1',)
# def checkBirthday():
#     print('========== 設定鬧鐘 =========')
#     # 利用datetime查詢時間
#     print(f'現在時間：{datetime.now().ctime()}')

#     listDic = f.searchClock()

#     for dic in listDic:    
#         if datetime.today().strftime("%Y-%m-%d") == dic['clockdate']:
#         else:
#           print("非今日鬧鐘")

#     Lists = f.searchBirthday()
#     if Lists != []:
#         line_bot_api.multicast(Lists,TextSendMessage(text = ''))    
#         try:
#             for List in Lists:
#                 profile = line_bot_api.get_profile(List)
#                 line_bot_api.push_message('Ce0a20c9eea131c7fce6deef569fff38e',TextSendMessage(text=f'''{profile.display_name},祝你生日快樂'''))
#         except LineBotApiError as e: 
#             print(f'''錯誤訊息：{e}''')
#     else :
     
#     print('========== 設定鬧鐘 =========')


sched.start()


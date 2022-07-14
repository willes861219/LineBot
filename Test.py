from datetime import datetime
from distutils.log import error
import telnetlib
from typing import List
import function as f
import re 
import json
import function as f
import random

from linebot import LineBotApi
from linebot.models import TextSendMessage

# results = f.searchClock()

# print(datetime.today().strftime("%Y-%m-%d"))

# today = datetime.today().strftime("%Y-%m-%d"
#datetime.today().strftime("%Y-%m-%d"

listDict=f.searchClock()
if listDict != []:
    for dic in listDict:    
        if datetime.today().strftime("%Y-%m-%d") == dic['clockdate']:
            print("今日鬧鐘")
            
        else:
          print("非今日鬧鐘")
else:
    print("空的")

# message = '對不對'

# textMessage = random.choice(('會','不會')) if "會不會" in message else random.choice(('是','不是'))  if "是不是" in message else random.choice(('要','不要')) if '要不要' in message else random.choice(('對','不對'))

# print(textMessage)


# for result in results:    
#    if datetime.today().strftime("%Y-%m-%d") == result['clockdate']:
#       print(result)
#    else:
#       print("非今日鬧鐘")

      
#FB看到的問題
# lists = [[1,2,3],[4,5],[6,7,8],[9]]
# #第一種
# for list in lists:
#     lens = len(list)
#     i = 0
#     while i < lens:
#         print(list[i])
#         i +=1

# #第二種
# print("=========")
# for list in lists:
#     for lis in list:
#         print(lis)





# message = "我不知道"
# blackLists = f.searchJudge()
# print(blackLists)
# if(blackLists != []):
#     # if message in blackLists: ## message 100%符合搜尋
#     #     isJudgeMsg =True
#     # else:
#     #     isJudgeMsg = False
#     for list in blackLists:
#         print(list)
#     if any(list in message for list in blackLists): ## message模糊搜尋
#         isJudgeMsg = True
#         print("黑名單True")
#     else:
#         isJudgeMsg = False
#         print("黑名單False")



# lists = f.updateBirthday()
# LINE BOT info
# line_bot_api = LineBotApi('Oab2kpZ3f0t35+8oYNfTpYbq9T4taRyVminiW9gHGUAbgnWfiWPpUoqmn2LpXEySzWu33oZgZQNY3xHDE67nH6+spvtyxzy7OZy+F3y8LqHYXHPZM7qJenb7ULux0oOcXLbn9Lg5D8oRzfm8ic8NBAdB04t89/1O/w1cDnyilFU=')
# myId = 'U8ff193174b01bfa73c2e4e9c178d003c'
# List = f.searchBirthday()
# for List in List:
#     print(List)

# f.updateUserData("Ubf86b62b8d21fc113481b795753ea9b9","劉仲恩")
# member = [{"type": "user", "userId": "U8ff193174b01bfa73c2e4e9c178d003c"}]

# print(member[0]["userId"])
# test = next((x for x in member),None)
# print(test['userId'])


# print(f.searchJudge())
# msg = "哈囉"
# mylist = ['測試1','哈囉','測試2'] 

# if msg in mylist:
#     print("yes")
# else:
#     print("no")
# test = lambda x: x == msg
# print("test lambda and map = "+ mylist(msg))

# blackLists = f.searchJudge()
#     if(blackLists != []):
#         map(,blackLists)
#         for list in blackLists:
#             if(list in message):
#                 isJudgeMsg = True
#                 break
#             else:
#                 isJudgeMsg = False
#     print("成功取得黑名單")
# # a = 0
# msg = "測試1"
# lists = ['測試1','測試2','測試3','測試4']
# message = ""
# for list in lists:
#     if(list == msg):
#         lists.remove(list)
#         for list in lists:
#             message += list + ','
#         print(message[:-1])
#     else:
#         continue
# for list in lists:
#     message += list + ','
# print(message[:-1])
# print(lists)

# msg = "黑名單 靠"
# b = msg.split(" ")
# print(len(b))

# result = f.searchJudge()
# print(result)
#elif('爛' in message or '幹' in message or '垃圾' in message or '低能兒' in message or '沒料' in message):

# import numpy as np

# a = np.array([1,2,3])
# print(a)

# b = np.array([[5,3,6,7,1], [1,2,3,4,5]])
# print(b[1,3])
# print(b)


# #一個骰子
# #大 小 單 雙 四種組合
# #456 123 
# #先說要大或小 單或雙，然後機器人講骰到幾點，然後講誰贏誰輸 誰拿走多少籌碼
# #大或小 單或雙 這個應該是8種組合
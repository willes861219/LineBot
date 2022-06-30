from distutils.log import error
import telnetlib
from typing import List
import function as f
import re 

# print(f.searchJudge())


# f.clearJudge()

f.updateJudge("測試一")


# a = 0
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
from __future__ import barry_as_FLUFL
from array import array
from ast import ListComp
from itertools import count
from operator import index
from this import d
from unittest import TextTestResult
from uuid import RESERVED_FUTURE

import function as f
import os
import json
import random
from flask import Flask, request, abort,render_template
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


app = Flask(__name__)
# LINE BOT info
line_bot_api = LineBotApi('Oab2kpZ3f0t35+8oYNfTpYbq9T4taRyVminiW9gHGUAbgnWfiWPpUoqmn2LpXEySzWu33oZgZQNY3xHDE67nH6+spvtyxzy7OZy+F3y8LqHYXHPZM7qJenb7ULux0oOcXLbn9Lg5D8oRzfm8ic8NBAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('aff823673f1d48c14b2875b853ebb17f') 

# 增加的這段放在下面
@app.route("/")
def home():
    return render_template("home.html")
# 增加的這段放在上面

# 指定在 /callback 通道上接收訊息，且方法是 POST，而callback()是為了要檢查連線是否正常
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print(body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:  
        abort(400)
    return 'OK'

# Message event
@handler.add(MessageEvent)
def handle_message(event):
    message_type = event.message.type
    user_id = event.source.user_id
    reply_token = event.reply_token
    message = event.message.text    
    profile = line_bot_api.get_profile(user_id) #取得使用者資訊 
    #{
    #   "userId": "U82******************",
    #   "displayName": "張君祥", // 傳訊息使用者的帳號名字
    #   "pictureUrl": "https://sprofile.line-scdn.net/***/", // 使用者的大頭照圖片網址
    #   "statusMessage": "蘋果仁 IG 編輯\n做個無所畏懼s的謙卑之人",  // 使用者的 Bio
    #   "language": "zh-Hant" // 使用者的偏好語言
    #}
    print(profile.display_name, "：",message) #傳送訊息Log
    ###判斷是否為黑名單內字元
    try:
        blackLists = f.searchJudge()
        if(blackLists != []):
            for list in blackLists:
                if(list in message):
                    isJudgeMsg = True
                    break
                else:
                    isJudgeMsg = False
        print("成功取得黑名單")
    except:
        isJudgeMsg =False
        blackLists = "黑名單內無資料"
        print("失敗取得黑名單")

    if(message_type == "sticker"):
        num = random.randint(76,99)
        exportNum = '105513'+str(num)
        sticker_message = StickerSendMessage(package_id='6136',sticker_id=exportNum)
        line_bot_api.reply_message(reply_token, sticker_message)
    elif("清除黑名單" in message):
        if(user_id == "U8ff193174b01bfa73c2e4e9c178d003c"):
            try:    
                count = f.clearJudge()
                text_message = TextSendMessage(text = f"成功清除黑名單，異動紀錄{count}筆")
                line_bot_api.reply_message(reply_token,text_message)
            except:
                text_message = TextSendMessage(text = "清除失敗，請至Heroku Log查看錯誤訊息")
                line_bot_api.reply_message(reply_token,text_message)
        else:
            text_message = TextSendMessage(text = profile.display_name + "的權限不足")
            line_bot_api.reply_message(reply_token, text_message)
    elif("刪除黑名單" in message):
        # if(user_id == "U8ff193174b01bfa73c2e4e9c178d003c"):
        msgList = str(message).split(" ")
        if(len(msgList) >= 1 and msgList[0] == "刪除黑名單"):
            text_message = TextSendMessage(text = f.deleteJudge(msgList[1]))
            line_bot_api.reply_message(reply_token,text_message)
        else:
            text_message = TextSendMessage(text = "格式錯誤")
            line_bot_api.reply_message(reply_token,text_message)
        # else:
        #     text_message = TextSendMessage(text = profile.display_name + "的權限不足")
        #     line_bot_api.reply_message(reply_token, text_message)
    elif("加入黑名單" in message):
        # if(user_id == "U8ff193174b01bfa73c2e4e9c178d003c"):
        msgList = str(message).split(" ")
        if(len(msgList) > 1 and msgList[0] == "加入黑名單"): # 判斷List長度是否大於1 
            isblackList = False 
            for list in blackLists:
                if(list == msgList[1]):
                    isblackList = True  
                    print("已有在黑名單中")
                    break
                else:
                    continue
            if(isblackList != True):
                count = f.updateJudge(msgList[1])
                if(count >= 1):
                    text_message = TextSendMessage(text = msgList[1] +" 已加入黑名單")
                    line_bot_api.reply_message(reply_token, text_message)
                else:
                    text_message = TextSendMessage(text = msgList[1] +" 加入失敗")
                    line_bot_api.reply_message(reply_token, text_message)
            else:
                text_message = TextSendMessage(text = msgList[1] +" 已有在黑名單中")
                line_bot_api.reply_message(reply_token, text_message)
        else:
            text_message = TextSendMessage(text = "輸入格式錯誤")
            line_bot_api.reply_message(reply_token, text_message)
        # else:
        #     text_message = TextSendMessage(text = profile.display_name + "的權限不足")
        #     line_bot_api.reply_message(reply_token, text_message)
    elif("黑名單清單" in message):
        text_message = TextSendMessage(text = str(blackLists))
        line_bot_api.reply_message(reply_token, text_message)
    elif("嗨" in message or "安安" in message ):
        text_message = TextSendMessage(text = profile.display_name + ",嗨嗨")
        line_bot_api.reply_message(reply_token, text_message)
    elif(message == '貼圖一'):
        num = random.randint(76,99)
        exportNum = '105513'+str(num)
        sticker_message = StickerSendMessage(package_id='6136',sticker_id=exportNum)
        line_bot_api.reply_message(reply_token, sticker_message)
    elif(message == '貼圖二'):
        num = random.randint(4,24) 
        exportNum = '109799'+str(num)
        sticker_message = StickerSendMessage(package_id='6325',sticker_id=exportNum)
        line_bot_api.reply_message(reply_token, sticker_message)
    elif("罵他" in message or "罵罵" in message):
        if(event.message.mention != None):
            tagInfo = event.message.mention.mentionees
            tagOneData = next((x for x in tagInfo), None)
            strData = str(tagOneData)
            j = json.loads(strData)
            tagProfileData = line_bot_api.get_profile(j['userId'])
            if(j['userId'] == "U8ff193174b01bfa73c2e4e9c178d003c"):
               text_message = TextSendMessage(text = profile.display_name + random.choice((',你才垃圾', ',你才低能兒', ',你才沒料')))
               line_bot_api.reply_message(reply_token, text_message)
            else:
                text_message = TextSendMessage(text = tagProfileData.display_name + random.choice(('垃圾', '低能兒', '沒料')))
                line_bot_api.reply_message(reply_token, text_message)
    elif('誇我' in message):
        text_message = TextSendMessage(text = profile.display_name + random.choice(('你就很猛', '你好棒', '你是鬼')))
        line_bot_api.reply_message(reply_token, text_message)
    elif(isJudgeMsg):
        if(user_id == "U8ff193174b01bfa73c2e4e9c178d003c"):
            text_message = TextSendMessage(text = '確實')
            line_bot_api.reply_message(reply_token, text_message)
        else:
            text_message = TextSendMessage(text = profile.display_name + ',你講話可不可以不要這麼臭')
            line_bot_api.reply_message(reply_token, text_message)
    elif('謝' in message):
        text_message = TextSendMessage(text = '不客氣')
        line_bot_api.reply_message(reply_token, text_message)
    elif('對不起' in message):
        text_message = TextSendMessage(text = profile.display_name + ',我原諒你')
        line_bot_api.reply_message(reply_token, text_message)
    elif('恐怖' in message):
        if(user_id == "U8ff193174b01bfa73c2e4e9c178d003c"):
            text_message = TextSendMessage(text = '真的恐怖')
            line_bot_api.reply_message(reply_token, text_message)
        else:
            text_message = TextSendMessage(text = profile.display_name + ',沒你長的恐怖')
            line_bot_api.reply_message(reply_token, text_message)
    elif(message == '早餐'):
        FlexMessage = json.load(open('burger.json','r',encoding='utf-8'))
        line_bot_api.reply_message(reply_token, FlexSendMessage('123',FlexMessage))
    elif(message == '重置抽籤'):
        f.resetDrawStraws(user_id)
        result = TextSendMessage(text = f'已重置{profile.display_name}的抽籤次數')
        line_bot_api.reply_message(reply_token,result)
    elif(message == '抽籤次數'):
        Count = f.SearchDrawStraws(user_id)
        result =  TextSendMessage(text = profile.display_name + f',今日抽籤次數：{Count}次')
        line_bot_api.reply_message(reply_token, result)
    elif(message == '抽籤' or '我抽籤' in message):
        Count = f.SearchDrawStraws(user_id)
        addcount = f.updateCount(user_id,Count) #新增抽籤次數
        if(addcount == True):
            if(user_id == "U8ff193174b01bfa73c2e4e9c178d003c"):
                result =  TextSendMessage(text = profile.display_name+',本次抽籤結果：' + random.choice(['大吉','中吉','小吉']) + f'，今日已抽籤：{Count+1}次')
                line_bot_api.reply_message(reply_token, result)
            # elif(user_id == 'Uee42ddfe4ff01ddf857dfda5d1db9537' or user_id == 'U771d831b3496944d6ba094e05b0d9ebb' ): 
            #     result =  TextSendMessage(random.choice(['凶','大凶'])+f'，今日已抽籤：{Count+1}次')
            #     line_bot_api.reply_message(reply_token, result)
            else:
                result =  TextSendMessage(text = profile.display_name+',本次抽籤結果：'+ random.choice(['大吉','中吉','小吉','吉','末吉','凶','大凶']) + f'，今日已抽籤：{Count+1}次')
                line_bot_api.reply_message(reply_token, result)
        else:
            result =  TextSendMessage(text = profile.display_name+',已超過次數，無法抽籤')
            line_bot_api.reply_message(reply_token, result)
    elif('已讀' in message):
        text_message = TextSendMessage(text = '絕對不是我已讀的')
        line_bot_api.reply_message(reply_token, text_message)
    elif(message == '測試'):
        msg = f.SearchDB()
        text_message = TextSendMessage(text = msg)
        line_bot_api.reply_message(reply_token, text_message)
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT',80))
    app.run(host='0.0.0.0', port=port)
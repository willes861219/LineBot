import function as f
import os
import json
import random
from flask import Flask, request, abort, render_template
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


app = Flask(__name__)
# LINE BOT info
line_bot_api = LineBotApi('<填入你 Linebot 的 channel access token>')
handler = WebhookHandler('<填入你 Linebot 的 Channel secret>')

# 增加的這段放在下面


@app.route("/")
def home():
    return render_template("home.html")
# 增加的這段放在上面

# 接收 LINE 的資訊，指定在 /callback 通道上接收訊息，且方法是 POST，而callback()是為了要檢查連線是否正常


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

# 成員加入群組事件


@handler.add(MemberJoinedEvent)
def handle_follow(event):
    reply_token = event.reply_token
    members = event.joined.members
    print(f"成員：{members}")
    dictData = next((x for x in members), None)
    strData = str(dictData)
    j = json.loads(strData)
    userId = j['userId']
    profile = line_bot_api.get_profile(userId)

    print(f"使用者：{profile.display_name}")
    try:
        f.updateUserData(userId, profile.display_name)
        text_message = TextSendMessage(
            text=f"安安歡迎{profile.display_name}，加入資料庫成功")
        line_bot_api.reply_message(reply_token, text_message)
    except:
        text_message = TextSendMessage(
            text=f"安安歡迎{profile.display_name}，加入資料庫失敗")
        line_bot_api.reply_message(reply_token, text_message)

# @handler.add(MemberLeftEvent)
# def handle_follow(event):
    # reply_token = event.reply_token
    # members = event.joined.members
    # type = event.type
    # print(f"成員：{members}")
    # print(f"外層：{event}")

    # if type == 'memberJoined':
    #     print(f"MemberJoined:{json.load(event)}")
    #     print("加入")
    #     text_message = TextSendMessage(text = f"MemberJoined {event.source.type}")
    #     line_bot_api.reply_message(reply_token, text_message)
    # elif type == 'memberLeft':
    #     print(f"MemberLeft:{json.load(event)}")
    #     print("離開")
    #     text_message = TextSendMessage(text = f"MemberLeft {event.source.type}")
    #     line_bot_api.reply_message(reply_token, text_message)

# Message event


@handler.add(MessageEvent)
def handle_message(event):
    message_type = event.message.type
    user_id = event.source.user_id
    reply_token = event.reply_token
    message = event.message.text
    profile = line_bot_api.get_profile(user_id)  # 取得使用者資訊
    # {
    #   "userId": "U82******************",
    #   "displayName": "陳威延", // 傳訊息的用戶名稱
    #   "pictureUrl": "https://sprofile.line-scdn.net/***/", // 使用者大頭照網址
    #   "statusMessage": "",  // 狀態資訊
    #   "language": "zh-Hant" // 偏好語言
    # }
    print(profile.display_name, "：", message)  # 傳送訊息Log
    # 判斷是否為黑名單內字元
    try:
        blackLists = f.searchJudge()
        if (blackLists != []):
            # if message in blackLists: ## message 100%符合搜尋
            #     isJudgeMsg =True
            # else:
            #     isJudgeMsg = False

            if any(list in message for list in blackLists):  # message模糊搜尋
                isJudgeMsg = True
                print("黑名單True")
            else:
                isJudgeMsg = False
                print("黑名單False")

        print("成功判斷文字是否在黑名單內")
    except:
        isJudgeMsg = False
        blackLists = "黑名單內無資料"
        print("失敗取得黑名單")

    if (message_type == "sticker"):
        # num = random.randint(20,43)
        exportNum = '110879'+str(random.randint(20, 43))
        sticker_message = StickerSendMessage(
            package_id='6362', sticker_id=exportNum)
        line_bot_api.reply_message(reply_token, sticker_message)
    elif ("time" in message):
        nowtime = f.current_Time()
        text_message = TextSendMessage(text=nowtime)
        line_bot_api.reply_message(reply_token, text_message)
    elif ("會不會" in message or "是不是" in message or "要不要" in message or '對不對' in message or '有沒有' in message or '知不知道' in message):
        replytext = random.choice(('會', '不會')) if "會不會" in message else random.choice(('是', '不是')) if "是不是" in message else random.choice(
            ('要', '不要')) if '要不要' in message else random.choice(('對', '不對')) if '對不對' in message else random.choice(('有', '沒有')) if '有沒有' in message else random.choice(('知道', '不知道', '知你媽'))
        text_message = TextSendMessage(text=replytext)
        line_bot_api.reply_message(reply_token, text_message)
    elif ("不是問你" in message or "不是跟你說" in message or "不是跟你講" in message):
        replytext = random.choice(('喔', '我也不是回你'))
        text_message = TextSendMessage(text=replytext)
        line_bot_api.reply_message(reply_token, text_message)
    elif ('真假' in message):
        text_message = TextSendMessage(text=random.choice(('真的', '假的')))
        line_bot_api.reply_message(reply_token, text_message)
    elif ("清除黑名單" in message):
        if (user_id == "U8ff193174b01bfa73c2e4e9c178d003c"):
            try:
                count = f.clearJudge()
                text_message = TextSendMessage(text=f"成功清除黑名單，異動紀錄{count}筆")
                line_bot_api.reply_message(reply_token, text_message)
            except:
                text_message = TextSendMessage(text="清除失敗，請至Heroku Log查看錯誤訊息")
                line_bot_api.reply_message(reply_token, text_message)
        else:
            text_message = TextSendMessage(text=profile.display_name + "的權限不足")
            line_bot_api.reply_message(reply_token, text_message)
    elif ("刪除黑名單" in message):
        # if(user_id == "U8ff193174b01bfa73c2e4e9c178d003c"):
        msgList = str(message).split(" ")
        if (len(msgList) >= 1 and msgList[0] == "刪除黑名單"):
            text_message = TextSendMessage(text=f.deleteJudge(msgList[1]))
            line_bot_api.reply_message(reply_token, text_message)
        else:
            text_message = TextSendMessage(text="格式錯誤")
            line_bot_api.reply_message(reply_token, text_message)
        # else:
        #     text_message = TextSendMessage(text = profile.display_name + "的權限不足")
        #     line_bot_api.reply_message(reply_token, text_message)
    elif ("加入黑名單" in message):
        # if(user_id == "U8ff193174b01bfa73c2e4e9c178d003c"):
        msgList = str(message).split(" ")
        if (len(msgList) > 1 and msgList[0] == "加入黑名單"):  # 判斷List長度是否大於1
            isblackList = False
            for list in blackLists:
                if (list == msgList[1]):
                    isblackList = True
                    print("已有在黑名單中")
                    break
                else:
                    continue
            if (isblackList != True):
                count = f.updateJudge(msgList[1])
                if (count >= 1):
                    text_message = TextSendMessage(text=msgList[1] + " 已加入黑名單")
                    line_bot_api.reply_message(reply_token, text_message)
                else:
                    text_message = TextSendMessage(text=msgList[1] + " 加入失敗")
                    line_bot_api.reply_message(reply_token, text_message)
            else:
                text_message = TextSendMessage(text=msgList[1] + " 已有在黑名單中")
                line_bot_api.reply_message(reply_token, text_message)
        else:
            text_message = TextSendMessage(text="輸入格式錯誤")
            line_bot_api.reply_message(reply_token, text_message)
        # else:
        #     text_message = TextSendMessage(text = profile.display_name + "的權限不足")
        #     line_bot_api.reply_message(reply_token, text_message)
    elif ("黑名單清單" in message):
        text_message = TextSendMessage(text=str(blackLists))
        line_bot_api.reply_message(reply_token, text_message)
    elif ("嗨" in message or "安安" in message):
        text_message = TextSendMessage(text=profile.display_name + ",嗨嗨")
        line_bot_api.reply_message(reply_token, text_message)
    elif (message == '貼圖一'):
        num = random.randint(76, 99)
        exportNum = '105513'+str(num)
        sticker_message = StickerSendMessage(
            package_id='6136', sticker_id=exportNum)
        line_bot_api.reply_message(reply_token, sticker_message)
    elif (message == '貼圖二'):
        num = random.randint(4, 24)
        exportNum = '109799'+str(num)
        sticker_message = StickerSendMessage(
            package_id='6325', sticker_id=exportNum)
        line_bot_api.reply_message(reply_token, sticker_message)
    elif ("罵他" in message or "罵罵" in message):
        if (event.message.mention != None):
            tagInfo = event.message.mention.mentionees
            tagOneData = next((x for x in tagInfo), None)
            strData = str(tagOneData)
            j = json.loads(strData)
            tagProfileData = line_bot_api.get_profile(j['userId'])
            if (j['userId'] == "U8ff193174b01bfa73c2e4e9c178d003c"):
                text_message = TextSendMessage(
                    text=profile.display_name + random.choice((',你才垃圾', ',你才低能兒', ',你才沒料')))
                line_bot_api.reply_message(reply_token, text_message)
            else:
                text_message = TextSendMessage(
                    text=tagProfileData.display_name + random.choice(('垃圾', '低能兒', '沒料')))
                line_bot_api.reply_message(reply_token, text_message)
    elif ('誇我' in message):
        text_message = TextSendMessage(
            text=profile.display_name + random.choice(('你就很猛', '你好棒', '你是鬼')))
        line_bot_api.reply_message(reply_token, text_message)
    elif (isJudgeMsg):
        if (user_id == "U8ff193174b01bfa73c2e4e9c178d003c"):
            text_message = TextSendMessage(text='確實')
            line_bot_api.reply_message(reply_token, text_message)
        else:
            replyMessage = random.choice((',你講話怎麼這麼難聽', ',你講話可不可以不要這麼臭'))
            text_message = TextSendMessage(
                text=profile.display_name + replyMessage)
            line_bot_api.reply_message(reply_token, text_message)
    elif ('道歉' in message):
        if (user_id == "U8ff193174b01bfa73c2e4e9c178d003c"):
            text_message = TextSendMessage(text=profile.display_name + '對不起')
            line_bot_api.reply_message(reply_token, text_message)
        else:
            replyMessage = random.choice(('道你媽', '你才該道歉'))
            text_message = TextSendMessage(
                text=profile.display_name + replyMessage)
            line_bot_api.reply_message(reply_token, text_message)
    elif ('謝' in message):
        text_message = TextSendMessage(text='不客氣')
        line_bot_api.reply_message(reply_token, text_message)
    elif ('對不起' in message):
        text_message = TextSendMessage(text=profile.display_name + ',我原諒你')
        line_bot_api.reply_message(reply_token, text_message)
    elif ('恐怖' in message):
        if (user_id == "U8ff193174b01bfa73c2e4e9c178d003c"):
            text_message = TextSendMessage(text='真的恐怖')
            line_bot_api.reply_message(reply_token, text_message)
        else:
            text_message = TextSendMessage(
                text=profile.display_name + ',沒你長的恐怖')
            line_bot_api.reply_message(reply_token, text_message)
    elif (message == '早餐'):
        FlexMessage = json.load(open('burger.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(
            reply_token, FlexSendMessage('123', FlexMessage))
    elif (message == '重置抽籤'):
        f.resetDrawStraws(user_id)
        result = TextSendMessage(text=f'已重置{profile.display_name}的抽籤次數')
        line_bot_api.reply_message(reply_token, result)
    elif (message == '抽籤次數'):
        Count = f.SearchDrawStraws(user_id)
        result = TextSendMessage(
            text=profile.display_name + f',今日抽籤次數：{Count}次')
        line_bot_api.reply_message(reply_token, result)
    elif (message == '抽籤' or '我抽籤' in message):
        Count = f.SearchDrawStraws(user_id)
        addcount = f.updateCount(user_id, Count)  # 新增抽籤次數
        if (addcount == True):
            if (user_id == "U8ff193174b01bfa73c2e4e9c178d003c"):
                result = TextSendMessage(
                    text=profile.display_name+',本次抽籤結果：' + random.choice(['大吉', '中吉', '小吉']) + f'，今日已抽籤：{Count+1}次')
                line_bot_api.reply_message(reply_token, result)
            # elif(user_id == 'Uee42ddfe4ff01ddf857dfda5d1db9537' or user_id == 'U771d831b3496944d6ba094e05b0d9ebb' ):
            #     result =  TextSendMessage(random.choice(['凶','大凶'])+f'，今日已抽籤：{Count+1}次')
            #     line_bot_api.reply_message(reply_token, result)
            else:
                result = TextSendMessage(text=profile.display_name+',本次抽籤結果：' + random.choice(
                    ['大吉', '中吉', '小吉', '吉', '末吉', '凶', '大凶']) + f'，今日已抽籤：{Count+1}次')
                line_bot_api.reply_message(reply_token, result)
        else:
            result = TextSendMessage(text=profile.display_name+',已超過次數，無法抽籤')
            line_bot_api.reply_message(reply_token, result)
    elif ('已讀' in message):
        text_message = TextSendMessage(text='絕對不是我已讀的')
        line_bot_api.reply_message(reply_token, text_message)
    elif (message == '測試'):
        msg = str(f.SearchDB())
        text_message = TextSendMessage(text=msg)
        line_bot_api.reply_message(reply_token, text_message)
    elif message == '時間':
        result = f.searchClock()
        text_message = TextSendMessage(text=str(result))
        line_bot_api.reply_message(reply_token, text_message)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port, debug=True)

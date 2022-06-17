import json
import random
from flask import Flask, request, abort
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
    if(message == '嗨'):
        text_message = TextSendMessage(text = 'No嗨')
        line_bot_api.reply_message(reply_token, text_message)
    elif(message == '貼圖'):
        sticker_message = StickerSendMessage(package_id='6325',sticker_id='10979907')
        line_bot_api.reply_message(reply_token, sticker_message)
    elif(message == '圖片'):
        image_message = ImageSendMessage(original_content_url='https://file-examples-com.github.io/uploads/2017/10/file_example_PNG_500kB.png',preview_image_url='https://file-examples-com.github.io/uploads/2017/10/file_example_PNG_500kB.png')
        line_bot_api.reply_message(reply_token, image_message)
    elif(message == '影片'):
        video_message = VideoSendMessage(original_content_url='https://file-examples-com.github.io/uploads/2017/04/file_example_MP4_480_1_5MG.mp4',preview_image_url='https://file-examples-com.github.io/uploads/2017/10/file_example_PNG_500kB.png')
        line_bot_api.reply_message(reply_token, video_message)
    elif(message == '聲音'):
        audio_message = AudioSendMessage(original_content_url='https://file-examples-com.github.io/uploads/2017/11/file_example_MP3_700KB.mp3',duration=3000)
        line_bot_api.reply_message(reply_token, audio_message)
    elif(message == 'Location'):
        location_message = LocationSendMessage(title='my location',address='Tokyo',latitude=35.65910807942215,longitude=139.70372892916203)
        line_bot_api.reply_message(reply_token, location_message)
    elif(message == '早餐'):
        FlexMessage = json.load(open('burger.json','r',encoding='utf-8'))
        line_bot_api.reply_message(reply_token, FlexSendMessage('123',FlexMessage))
    elif(message == '抽籤'):
        result =  TextSendMessage(random.choice(['大吉','中吉','小吉','吉','末吉','凶','大凶']))
        line_bot_api.reply_message(reply_token, result)
    line_bot_api.reply_message(reply_token, TextSendMessage(text = "我不知道你在說什麼，你可以輸入\"早餐\"or\"抽籤\""))
    print(message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT',8080))
    app.run(host='localhost', port=port)
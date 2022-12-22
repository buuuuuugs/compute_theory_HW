from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re
app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('kv7WepC6RAvFR9a0nXxYfGQhZ3hJYLzAFuwrULyI+EIOU4sHY78p5fQFlEfO+jX0p2hRcSmgxe4l72SSerOZ3Eh6eo29AVAaytqy5UJkBaX3JvwI7Cb+Xlt9YpZbdW3PaBzJsRhfCnHyoKGsxB5CFAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('3e999dcd43d945411168f6de59fde57e')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = text=event.message.text
    if message in [ 'help', '幫助']:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='?'))
    if re.match('告訴我秘密',message):
        buttons_template_message = TemplateSendMessage(
        alt_text='秘密區',
        template=ButtonsTemplate(
            thumbnail_image_url='https://i.imgur.com/EKnxFZn.jpg',
            title='個人助理為您服務',
            text='選單功能',
            actions=[
                PostbackAction(
                    label='偷偷傳資料',
                    display_text='檯面上',
                    data='action=檯面下'
                ),
                MessageAction(
                    label='光明正大傳資料',
                    text='我就是資料'
                ),
                URIAction(
                    label='行銷搬進大程式',
                    uri='https://marketingliveincode.com/'
                )
            ]
        )
    )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
        
    # # if message in [ 'help', '幫助']:
    # # else:
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text='輸入"幫助"查看如何使用'))
    

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
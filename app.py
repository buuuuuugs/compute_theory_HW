from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re

from flask import Flask, request, abort
from flask import jsonify,  send_file
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from flask import render_template, jsonify, send_from_directory
from fsm import TocMachine




app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('kv7WepC6RAvFR9a0nXxYfGQhZ3hJYLzAFuwrULyI+EIOU4sHY78p5fQFlEfO+jX0p2hRcSmgxe4l72SSerOZ3Eh6eo29AVAaytqy5UJkBaX3JvwI7Cb+Xlt9YpZbdW3PaBzJsRhfCnHyoKGsxB5CFAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('3e999dcd43d945411168f6de59fde57e')


machine = TocMachine(
    states=["user", "secretState", "noteState",
            "jokeState", "searchImage", "help", "weather"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "secretState",
            "conditions": "is_going_to_secretState",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "noteState",
            "conditions": "is_going_to_noteState",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "jokeState",
            "conditions": "is_going_to_jokeState",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "searchImage",
            "conditions": "is_going_to_searchImage",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "help",
            "conditions": "is_going_to_help",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "weather",
            "conditions": "is_going_to_weather",
        },
        {"trigger": "go_back", "source": [
            "secretState", "noteState", "jokeState", "searchImage", "help", "weather"], "dest": "user"},
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)


line_bot_api.push_message('U20ef15015b2a770224a03288132f4a31', TextSendMessage(text='我是你的個人小助理，很高興為你服務，輸入"幫助"查看如何使用'))


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
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":

        #'

        # for i in event.message.text:

        #     pretty_text += i
        #     pretty_text += random.choice(pretty_note)
        response = machine.advance(event)
        if response == False:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='輸入"幫助"查看如何使用')
            )
    
        
    

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
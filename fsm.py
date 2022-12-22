from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from transitions.extensions import GraphMachine

from flask import Flask, request, abort
from flask import jsonify,  send_file
from flask_ngrok import run_with_ngrok
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
from flask import render_template, jsonify, send_from_directory


import re
import random

from urllib import request
from urllib.parse import urlencode
import requests

import json


# Channel Access Token
line_bot_api = LineBotApi('kv7WepC6RAvFR9a0nXxYfGQhZ3hJYLzAFuwrULyI+EIOU4sHY78p5fQFlEfO+jX0p2hRcSmgxe4l72SSerOZ3Eh6eo29AVAaytqy5UJkBaX3JvwI7Cb+Xlt9YpZbdW3PaBzJsRhfCnHyoKGsxB5CFAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('3e999dcd43d945411168f6de59fde57e')

app = Flask(__name__, static_url_path='/image')

to_user = 'U20ef15015b2a770224a03288132f4a31'



jokes = ["醫生問小明：如果把你一邊耳朵割掉你會怎麼樣？\n小明：我會聽不見\n醫生又問：那再割掉另一個耳朵呢？\n小明：我會看不見\n醫生問他為什麼...\n小明：因為我有戴眼鏡",
         "其實你有一億的存款\n只不過你忘了密碼\n每輸入一次只需要50元\n一旦正確，錢就是你的\n不著急 不放棄 心若在 夢就在\n               台灣彩卷",
         "永遠不要看輕你自己\n馬雲、比爾蓋茲、伊隆馬斯克、馬克·祖克柏、還有你\n你們的資產加起來足以撼動整個亞洲甚至全世界的金融體系",
         "一名男子僅用0.22口徑手槍\n在柯迪亞克棕熊的攻擊下存活\n他膝蓋被射傷的朋友則沒那麼幸運....",
         "MOM said:Alcohol is your enemy\nJESUS said:Love your enemy\n          -CASE CLOSED- \n              CHEERS"]
bool_jokes = [False for i in range(5)]


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_secretState(self, event):
        text = event.message.text
        return ("秘密" in text)

    def is_going_to_noteState(self, event):
        text = event.message.text
        return ("筆記" in text)            

    def is_going_to_jokeState(self, event):
        text = event.message.text
        return ("笑話" in text)              

    def is_going_to_searchImage(self, event):
        text = event.message.text
        return ("搜尋" in text)
    def is_going_to_help(self, event):
        text = event.message.text
        return (("幫助" in text) or ("help" in text))

    def is_going_to_weather(self, event):
        text = event.message.text
        return ("天氣" in text)

    # image
    def on_enter_secretState(self, event):
        
        buttons_template_message = TemplateSendMessage(
            alt_text='秘密區',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/EKnxFZn.jpg',
                title='個人助理為您服務',
                text='選單功能',
                actions=[
                    
                    URIAction(
                        label='秘密1',
                        uri='https://drive.google.com/file/d/1GDC-cZnJd2vEk4N184HasUbAZnI_yCkF/view?usp=share_link'
                    ),
                    URIAction(
                        label='秘密2',
                        uri='https://drive.google.com/file/d/1dadmZGBD7XgPNd2Q2gPyoX9W-YEzn24y/view?usp=share_link'
                    )
                ]
            )
        
        )    
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
           
        self.go_back()

    def on_exit_secretState(self):
        line_bot_api.push_message(to_user, TextSendMessage(text="Have a nice day"))

    # tt

    def on_enter_noteState(self, event):
        buttons_template_message = TemplateSendMessage(
            alt_text='讀書區',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/Hd5mzoo.jpg',
                title='共同筆記為您服務',
                text='筆記選單',
                actions=[
                    
                    URIAction(
                        label='微算機',
                        uri='https://docs.google.com/document/d/104cQf1RhhweJqQmJJrZtGidI5eOHU7lxYAbf9fbFp4U/edit?usp=share_link'
                    ),
                    URIAction(
                        label='OS',
                        uri='https://docs.google.com/document/d/1cV5UvrJ9XJY2pSalITErLRTHrqg4obSV0r-i73qcikM/edit?usp=share_link'
                    ),
                    URIAction(
                        label='多平行',
                        uri='https://docs.google.com/document/d/172_yb-VXfxMqvjy4SKdodkKdrU88baKoqaAMD-p44Kc/edit?usp=share_link'
                    ),
                    URIAction(
                        label='計算理論',
                        uri='https://docs.google.com/document/d/1dzfyBlvCVdxAqRErFwTJhZAe0HkxWmq6UNa_-CyB5sA/edit?usp=share_link'
                    )
                ]
            )
        
        )    
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
           
        self.go_back()

    def on_exit_noteState(self):
        line_bot_api.push_message(to_user, TextSendMessage(text="讀書加油"))

    # joke

    def on_enter_jokeState(self, event):
        global bool_jokes

        index = random.randint(0, 4)
        while bool_jokes[index] is True:
            index = random.randint(0, 4)

        bool_jokes[index] = True
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=jokes[index]))

        if False not in bool_jokes:
            bool_jokes = [False for i in range(5)]

        self.go_back()

    def on_exit_jokeState(self):
        line_bot_api.push_message(to_user, TextSendMessage(text="希望你喜歡"))

    # search image

    def on_enter_searchImage(self, event):
        text = str(event.message.text)
        tmp = text.split(" ")
        text = tmp[1]

        img_search = {'tbm': 'isch', 'q': text}
        query = urlencode(img_search)
        base = "https://www.google.com/search?"
        url = str(base+query)

        headers = {'user-agent':
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
        res = request.Request(url, headers=headers)
        con = request.urlopen(res)
        data = con.read()

        pattern = '"(https://encrypted-tbn0.gstatic.com[\S]*)"'

        img_list = []
        for match in re.finditer(pattern, str(data, "utf-8")):
            if len(match.group(1)) < 150:
                img_list.append(match.group(1))

        random_img_url = img_list[random.randint(0, len(img_list)+1)]

        line_bot_api.push_message(to_user, ImageSendMessage(original_content_url=random_img_url,
                                                            preview_image_url=random_img_url))

        self.go_back()

    def on_exit_searchImage(self):
        line_bot_api.push_message(to_user, TextSendMessage(text="希望這是你要搜尋的圖片"))

    # answer

    def on_enter_help(self, event):
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="可用指令'幫助''筆記''搜尋''天氣'"))
        self.go_back()

    def on_exit_help(self):
        line_bot_api.push_message(to_user, TextSendMessage(text="有問題歡迎問我"))

    # weather
    def on_enter_weather(self, event):
        text = str(event.message.text)
        tmp = text.split(" ")
        city = tmp[1]

        token = "CWB-7A3D016E-7F19-40AA-94D6-E29866104ED3"
        url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=' + \
            token + '&format=JSON&locationName=' + city
        Data = requests.get(url)
        print(Data.text)
        f = open('weather.json', 'w', encoding='utf-8')
        f.write(Data.text)
        f.close()

        jf = open('weather.json', 'r', encoding='utf-8')
        dic_data = json.load(jf)
        jf.close()

        res = dic_data['records']['location'][0]['weatherElement']
        stime = res[1]["time"][0]["startTime"]
        etime = res[1]["time"][0]["endTime"]
        condition = res[0]["time"][0]["parameter"]["parameterName"]
        pop = res[1]["time"][0]["parameter"]["parameterName"]
        mint = res[2]["time"][0]["parameter"]["parameterName"]
        maxt = res[4]["time"][0]["parameter"]["parameterName"]

        t1 = f'{city}十二小時天氣預報\n'
        t2 = f'(從{stime}到{etime})\n'
        t3 = f'天氣狀況: {condition}\n'
        t4 = f'最高溫: {maxt}\n'
        t5 = f'最低溫: {mint}\n'
        t6 = f'降雨機率: {pop}'
        t = t1+t2+t3+t4+t5+t6

        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=t))
        if int(maxt) < 20:
            line_bot_api.push_message(
                to_user, TextSendMessage(text="天氣冷要注意保暖，出門記得帶個雨具<3"))

        self.go_back()

    def on_exit_weather(self):
        pass
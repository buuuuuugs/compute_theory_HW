from transitions.extensions import GraphMachine
# from utils import send_text_message, send_carousel_message, send_button_message, send_image_message
# from bs4 import BeautifulSoup
import requests
from linebot.models import ImageCarouselColumn, URITemplateAction, MessageTemplateAction
# import pandas as pd

# global variable


class TocMachine(GraphMachine):

    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    # user start
    def menu(self, event):
        text = event.message.text
        return text.lower() == 'fitness'
    def help(self, event):
       if re.match('告訴我秘密',event.message):
        buttons_template_message = TemplateSendMessage(
        alt_text='這個看不到',
        template=ButtonsTemplate(
            thumbnail_image_url='https://i.imgur.com/wpM584d.jpg',
            title='行銷搬進大程式',
            text='選單功能－TemplateSendMessage',
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


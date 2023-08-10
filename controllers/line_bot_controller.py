'''
當用戶關注時，必須取用照片，並存放至指定bucket位置，而後生成User物件，存回db
當用戶取消關注時，
    從資料庫提取用戶數據，修改用戶的封鎖狀態後，存回資料庫
'''

from linebot import (
    LineBotApi, WebhookHandler
)
import os

from linebot.models import(
    TextSendMessage, ImageSendMessage
)

# 載入Follow事件
from linebot.models.events import (
    FollowEvent, UnfollowEvent
)

from services.image_service import ImageService
from services.user_service import UserService
from services.video_service import VideoService
from services.audio_service import AudioService

from urllib.parse import parse_qs, parse_qsl

from models import func

line_bot_api=LineBotApi(channel_access_token=os.environ["LINE_CHANNEL_ACCESS_TOKEN"])

class LineBotController:

    # 將消息交給用戶服務處理
    @classmethod
    def follow_event(cls, event):
        # print(event)
        line_bot_api.reply_message(
                                    event.reply_token,
                                    [TextSendMessage('Hello！您好👋👋👋\n我們是司康販賣所！\n目前只有販售司康，分別有經典司康、派式司康、夾醬司康三種類型；\n如果對於我們的司康想多了解，可以點選"查詢品項"，我們會為您做介紹呦⸜( •⌄• )⸝~')])
        UserService.line_user_follow(event)

    @classmethod
    def unfollow_event(cls, event):
        UserService.line_user_unfollow(event)

    # 未來可能會判斷用戶快取狀態
    # 現在暫時無
    @classmethod
    def handle_text_message(cls, event):
        if(event.message.text.find('我要菜單')!= -1):
            line_bot_api.reply_message(
                                            event.reply_token,
                                            func.sendMenu(event)
                                            )
        elif(event.message.text.find('我要點餐')!= -1):
            line_bot_api.reply_message(
                                            event.reply_token,
                                            func.sendButton(event)
                                            )
        elif(event.message.text.find('我想查詢品項')!= -1):
            line_bot_api.reply_message(
                                            event.reply_token,
                                            func.sendback_item(event)
                                            )
        elif(event.message.text.find('我要店家資訊')!= -1):
            line_bot_api.reply_message(
                                            event.reply_token,
                                            func.sendback_location(event)
                                            )
        elif(event.message.text.find('@')!= -1):
            line_bot_api.reply_message(
                                            event.reply_token,
                                            func.template_message_dict.get(event.message.text)
                                            )
        else:
            pass

        # return None


    # 用戶收到照片時的處理辦法
    @classmethod
    def handle_image_message(cls, event):
        ImageService.line_user_upload_image(event)
        return "OK"

    # 用戶收到影片時的處理辦法
    @classmethod
    def handle_video_message(cls, event):
        VideoService.line_user_upload_video(event)
        return "OK"

    @classmethod
    def handle_audio_message(cls, event):
        AudioService.line_user_upload_video(event)
        return "OK"

    
    @classmethod
    def handle_postback_event(cls, event):
        backdata = dict(parse_qsl(event.postback.data))
        result = event.postback.data[2:].split('&')
        nn = event.source.user_id #儲存使用者 ID

        if backdata.get('action') == '經典司康':
            func.sendback_original(event, backdata)

        elif backdata.get('action') == '派式司康':
            func.sendback_pei(event, backdata)

        elif backdata.get('action') == '夾醬司康':
            func.sendback_sause(event, backdata)

        elif event.postback.data[0:1] == "A": # data="A&飲料名稱"
            num = event.postback.data[2:]
            func.sendback_num(event, backdata, num)

        elif event.postback.data[0:1] == "B": #確認當前輸入的訂單
            func.sendback_confirm(event, backdata, result, nn)

        elif event.postback.data[0:1] == "C": #繼續購物
            func.sendButton_Again(event)

        elif event.postback.data[0:1] == "D": #結帳
            func.sendRECEIPT(event)

        else:
            pass
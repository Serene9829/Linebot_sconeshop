'''

用戶上傳音訊時，將照片從Line取回，放入CloudStorage

瀏覽用戶目前擁有多少張音訊（未）

'''

from models.user import User
from flask import Request
from linebot import (
    LineBotApi
)

import os
from daos.user_dao import UserDAO
from linebot.models import (
    TextSendMessage
)


# 音訊下載與上傳專用
import urllib.request
from google.cloud import storage


class AudioService:
    
    line_bot_api = LineBotApi(channel_access_token=os.environ["LINE_CHANNEL_ACCESS_TOKEN"])

    '''
    用戶上傳音訊
    將音訊取回
    將音訊存入CloudStorage內
    '''
    @classmethod
    def line_user_upload_video(cls,event):

        # 取出音訊
        image_blob = cls.line_bot_api.get_message_content(event.message.id)
        temp_file_path=f"""{event.message.id}.mp3"""

        #
        with open(temp_file_path, 'wb') as fd:
            for chunk in image_blob.iter_content():
                fd.write(chunk)

        # 上傳至bucket
        storage_client = storage.Client()

        
        bucket_name = os.environ['USER_INFO_GS_BUCKET_NAME']

        destination_blob_name = f'{event.source.user_id}/audio/{event.message.id}.mp3'
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(temp_file_path)

        # 移除本地檔案
        os.remove(temp_file_path)
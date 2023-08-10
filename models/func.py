from linebot.models import (
                            TemplateSendMessage , TextSendMessage, ImageSendMessage, FlexSendMessage,
                            MessageEvent, PostbackEvent, MessageAction,
                            PostbackTemplateAction,  QuickReply, QuickReplyButton, BubbleContainer,
                            BoxComponent, TextComponent, SeparatorComponent, ButtonComponent
                            )

# 引入按鍵模板
from linebot.models.template import(ButtonsTemplate)

from linebot import (LineBotApi, WebhookHandler)

import json

line_bot_api=LineBotApi(channel_access_token=os.environ["LINE_CHANNEL_ACCESS_TOKEN"])

menu = {
        "經典奶油司康":"40","伯爵茶司康":"40", "黑糖麻糬司康":"60","烤布丁司康":"60",

        "糖皮厚奶油芋頭":"70","香橙乳酪":"70", "可可綠葡萄卡士達":"80","濃濃香蕉可可":"80"
        }

template_message_dict = {
                        "@經典奶油司康":(ImageSendMessage(
                                                        original_content_url='https://i.pinimg.com/564x/36/74/e9/3674e9c7c5f13782748d0faf22b7cac9.jpg',
                                                        preview_image_url='https://i.pinimg.com/564x/36/74/e9/3674e9c7c5f13782748d0faf22b7cac9.jpg'
                                                        ), TextSendMessage(text='無敵經典的奶油司康，簡單卻美味！每一口都充滿著香酥奶油的滋味，讓你回味無窮😋')),
                        "@伯爵茶司康":(ImageSendMessage(
                                                        original_content_url='https://i.pinimg.com/564x/ce/f8/3f/cef83fcc85e10750db29a57803523b0c.jpg',
                                                        preview_image_url='https://i.pinimg.com/564x/ce/f8/3f/cef83fcc85e10750db29a57803523b0c.jpg'
                                                        ), TextSendMessage(text='讓你一口咬下去就能感受到貴族級的享受！伯爵茶的香氣在嘴裡綻放，絕對是茶控☕的最愛')),
                        "@烤布丁司康":(ImageSendMessage(
                                                        original_content_url='https://i.pinimg.com/736x/5e/0d/13/5e0d13f39f9800e1cb5f79de31536bca.jpg',
                                                        preview_image_url='https://i.pinimg.com/736x/5e/0d/13/5e0d13f39f9800e1cb5f79de31536bca.jpg'
                                                        ), TextSendMessage(text='讓你吃到一口口的驚喜！內餡是滑順的布丁餡🍮，烤得微焦的外皮更加增添了口感的層次')),
                        "@糖皮厚奶油芋頭":(ImageSendMessage(
                                                            original_content_url='https://i.pinimg.com/564x/fd/8e/ce/fd8ece3b3d2f9e74c56972d777850c54.jpg',
                                                            preview_image_url='https://i.pinimg.com/564x/fd/8e/ce/fd8ece3b3d2f9e74c56972d777850c54.jpg'
                                                            ), TextSendMessage(text='吃得到幸福的甜蜜霜！司康表面的糖霜和內餡的厚鹹奶油與芋頭泥相互輝映，讓你嚐到極致的濃郁口感😍')),
                        "@香橙乳酪":(ImageSendMessage(
                                                    original_content_url='https://i.pinimg.com/564x/bf/f2/64/bff2648d8998549b355dc10c6796f3a6.jpg',
                                                    preview_image_url='https://i.pinimg.com/564x/bf/f2/64/bff2648d8998549b355dc10c6796f3a6.jpg'
                                                    ), TextSendMessage(text='橙香四溢的夏日滋味！柳橙味🍊的卡士達醬在司康上形成絕妙的配搭，再加上橙子切片的點綴，帶給你清新又迷人的口感')),
                        "@可可綠葡萄卡士達":(ImageSendMessage(
                                                            original_content_url='https://i.pinimg.com/564x/a4/c4/bb/a4c4bb3a2b53b814b69e6b499ef9de4c.jpg',
                                                            preview_image_url='https://i.pinimg.com/564x/a4/c4/bb/a4c4bb3a2b53b814b69e6b499ef9de4c.jpg'
                                                            ), TextSendMessage(text='探索味蕾的冒險之旅！卡士達與綠葡萄的組合，讓你感受到奇妙的口感交融，司康本身帶著可可🍫的香氣，讓你愛不釋口')),
                        "@濃濃香蕉可可":(ImageSendMessage(
                                                        original_content_url='https://i.pinimg.com/564x/53/14/f6/5314f6116951256cd5a974717424bf1e.jpg',
                                                        preview_image_url='https://i.pinimg.com/564x/53/14/f6/5314f6116951256cd5a974717424bf1e.jpg'
                                                        ), TextSendMessage(text='犒賞自己的甜蜜享受！香蕉塊🍌與巧克力醬的結合讓你愛不釋手，司康本身的香蕉可可味更是讓你陶醉其中')),
                        "@黑糖麻糬司康":(ImageSendMessage(
                                                        original_content_url='https://i.pinimg.com/564x/26/45/b8/2645b82dc16ed2495358b7e969873eb1.jpg',
                                                        preview_image_url='https://i.pinimg.com/564x/26/45/b8/2645b82dc16ed2495358b7e969873eb1.jpg'
                                                        ), TextSendMessage(text='麻糬愛好者絕對不能錯過！黑糖的濃郁與麻糬的彈牙結合，咬下去瞬間釋放甜蜜的幸福感😊'))
}


def sendMenu(event):
    try:
        message = ImageSendMessage(
            original_content_url="https://i.pinimg.com/564x/f3/1e/da/f31eda0171e683c83ca023cd3c3c6b27.jpg",
            preview_image_url="https://i.pinimg.com/564x/f3/1e/da/f31eda0171e683c83ca023cd3c3c6b27.jpg"
            )
        line_bot_api.reply_message(event.reply_token,message)

    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='不'))


def sendButton(event):
    try:
        buttons_template_message = TemplateSendMessage(
            alt_text='Buttons template',
            template = ButtonsTemplate(
                thumbnail_image_url="https://i.pinimg.com/750x/78/1b/49/781b4946957612bb5817112c534e4243.jpg",
                title='Menu',
                text='請問要哪個種類的司康',
                actions=[
                    PostbackTemplateAction(
                        label='經典司康',
                        text='經典司康',
                        data='action=經典司康'
                    ),
                    PostbackTemplateAction(
                        label='派式司康',
                        text='派式司康',
                        data='action=派式司康'
                    ),
                    PostbackTemplateAction(
                        label='夾醬司康',
                        text='夾醬司康',
                        data='action=夾醬司康'
                    )

                ]
            )

        )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)

    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='不'))


def sendback_original(event, backdata):
    try:
        flex_message = FlexSendMessage(
        alt_text='經典司康',
        contents={
            "type":
            "carousel",
            "contents": [
            {
                'type': 'bubble',
                'direction': 'ltr',
                "header": {
                "type":
                "box",
                "layout":
                "vertical",
                "contents": [{
                    "type": "text",
                    "text": "經典奶油司康 $40",
                    "weight": "bold",
                    "margin": "sm",
                    "size": "md",
                    "wrap": True
                }]
                },
                'hero': {
                'type': 'image',
                'url':
                'https://i.pinimg.com/564x/36/74/e9/3674e9c7c5f13782748d0faf22b7cac9.jpg',
                'size': 'full',
                'aspectRatio': '1:1',
                'aspectMode': 'cover',
                },
                'body': {
                "type":
                "box",
                "layout":
                "vertical",
                "spacing":
                "sm",
                "contents": [
                    {
                    "type": "button",
                    "style": "secondary",
                    "color": "#F6DCCB",
                    "action": {
                        'type': 'postback',
                        'label': '經典奶油司康',
                        'text': '想吃 經典奶油司康',
                        'data': 'A&經典奶油司康'
                    }
                    },
                ]
                }
            },
            {
                'type': 'bubble',
                'direction': 'ltr',
                "header": {
                "type":
                "box",
                "layout":
                "vertical",
                "contents": [{
                    "type": "text",
                    "text": "伯爵茶司康 $40",
                    "weight": "bold",
                    "margin": "sm",
                    "size": "md",
                    "wrap": True
                }]
                },
                'hero': {
                'type': 'image',
                'url':
                'https://i.pinimg.com/564x/ce/f8/3f/cef83fcc85e10750db29a57803523b0c.jpg',
                'size': 'full',
                'aspectRatio': '1:1',
                'aspectMode': 'cover',
                },
                'body': {
                "type":
                "box",
                "layout":
                "vertical",
                "spacing":
                "sm",
                "contents": [
                    {
                    "type": "button",
                    "style": "secondary",
                    "color": "#F6DCCB",
                    "action": {
                        'type': 'postback',
                        'label': '伯爵茶司康',
                        'text': '想吃 伯爵茶司康',
                        'data': 'A&伯爵茶司康'
                    }
                    },
                ]
                }
            }
            ]
        })

        line_bot_api.reply_message(event.reply_token, flex_message)

    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='不'))

def sendback_pei(event, backdata):
    try:
        flex_message = FlexSendMessage(
        alt_text='派式司康',
        contents={
            "type":
            "carousel",
            "contents": [
            {
                'type': 'bubble',
                'direction': 'ltr',
                "header": {
                "type":
                "box",
                "layout":
                "vertical",
                "contents": [{
                    "type": "text",
                    "text": "黑糖麻糬司康 $60",
                    "weight": "bold",
                    "margin": "sm",
                    "size": "md",
                    "wrap": True
                }]
                },
                'hero': {
                'type': 'image',
                'url':
                'https://i.pinimg.com/564x/26/45/b8/2645b82dc16ed2495358b7e969873eb1.jpg',
                'size': 'full',
                'aspectRatio': '1:1',
                'aspectMode': 'cover',
                },
                'body': {
                "type":
                "box",
                "layout":
                "vertical",
                "spacing":
                "sm",
                "contents": [
                    {
                    "type": "button",
                    "style": "secondary",
                    "color": "#F6DCCB",
                    "action": {
                        'type': 'postback',
                        'label': '黑糖麻糬司康',
                        'text': '想吃 黑糖麻糬司康',
                        'data': 'A&黑糖麻糬司康'
                    }
                    },
                ]
                }
            },
            {
                'type': 'bubble',
                'direction': 'ltr',
                "header": {
                "type":
                "box",
                "layout":
                "vertical",
                "contents": [{
                    "type": "text",
                    "text": "烤布丁司康 $60",
                    "weight": "bold",
                    "margin": "sm",
                    "size": "md",
                    "wrap": True
                }]
                },
                'hero': {
                'type': 'image',
                'url':
                'https://i.pinimg.com/736x/5e/0d/13/5e0d13f39f9800e1cb5f79de31536bca.jpg',
                'size': 'full',
                'aspectRatio': '1:1',
                'aspectMode': 'cover',
                },
                'body': {
                "type":
                "box",
                "layout":
                "vertical",
                "spacing":
                "sm",
                "contents": [
                    {
                    "type": "button",
                    "style": "secondary",
                    "color": "#F6DCCB",
                    "action": {
                        'type': 'postback',
                        'label': '烤布丁司康',
                        'text': '想吃 烤布丁司康',
                        'data': 'A&烤布丁司康'
                    }
                    },
                ]
                }
            }
            ]
        })

        line_bot_api.reply_message(event.reply_token, flex_message)

    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='不'))


def sendback_sause(event, backdata):
    try:
        flex_message = FlexSendMessage(
        alt_text='夾醬司康',
        contents={
            "type":"carousel",
            "contents": [
            {
                'type': 'bubble',
                'direction': 'ltr',
                "header": {
                "type":"box",
                "layout":"vertical",
                "contents": [{
                    "type": "text",
                    "text": "糖皮厚奶油芋頭 $70",
                    "weight": "bold",
                    "margin": "sm",
                    "size": "md",
                    "wrap": True
                }]
                },
                'hero': {
                'type': 'image',
                'url':'https://i.pinimg.com/564x/fd/8e/ce/fd8ece3b3d2f9e74c56972d777850c54.jpg',
                'size': 'full',
                'aspectRatio': '1:1',
                'aspectMode': 'cover',
                },
                'body': {
                "type":"box",
                "layout":"vertical",
                "spacing":"sm",
                "contents": [
                    {
                    "type": "button",
                    "style": "secondary",
                    "color": "#F6DCCB",
                    "action": {
                        'type': 'postback',
                        'label': '糖皮厚奶油芋頭',
                        'text': '想吃 糖皮厚奶油芋頭',
                        'data': 'A&糖皮厚奶油芋頭'
                    }
                    },
                ]
                }
            },
            {
                'type': 'bubble',
                'direction': 'ltr',
                "header": {
                "type":"box",
                "layout":"vertical",
                "contents": [{
                    "type": "text",
                    "text": "香橙乳酪 $70",
                    "weight": "bold",
                    "margin": "sm",
                    "size": "md",
                    "wrap": True
                }]
                },
                'hero': {
                'type': 'image',
                'url':'https://i.pinimg.com/736x/bf/f2/64/bff2648d8998549b355dc10c6796f3a6.jpg',
                'size': 'full',
                'aspectRatio': '1:1',
                'aspectMode': 'cover',
                },
                'body': {
                "type":"box",
                "layout":"vertical",
                "spacing":"sm",
                "contents": [
                    {
                    "type": "button",
                    "style": "secondary",
                    "color": "#F6DCCB",
                    "action": {
                        'type': 'postback',
                        'label': '香橙乳酪',
                        'text': '想吃 香橙乳酪',
                        'data': 'A&香橙乳酪'
                    }
                    },
                ]
                }
            },
            {
                'type': 'bubble',
                'direction': 'ltr',
                "header": {
                "type":"box",
                "layout":"vertical",
                "contents": [{
                    "type": "text",
                    "text": "可可綠葡萄卡士達 $80",
                    "weight": "bold",
                    "margin": "sm",
                    "size": "md",
                    "wrap": True
                }]
                },
                'hero': {
                'type': 'image',
                'url':'https://i.pinimg.com/564x/a4/c4/bb/a4c4bb3a2b53b814b69e6b499ef9de4c.jpg',
                'size': 'full',
                'aspectRatio': '1:1',
                'aspectMode': 'cover',
                },
                'body': {
                "type":"box",
                "layout":"vertical",
                "spacing":"sm",
                "contents": [
                    {
                    "type": "button",
                    "style": "secondary",
                    "color": "#F6DCCB",
                    "action": {
                        'type': 'postback',
                        'label': '可可綠葡萄卡士達',
                        'text': '想吃 可可綠葡萄卡士達',
                        'data': 'A&可可綠葡萄卡士達'
                    }
                    },
                ]
                }
            },
            {
                'type': 'bubble',
                'direction': 'ltr',
                "header": {
                "type":"box",
                "layout":"vertical",
                "contents": [{
                    "type": "text",
                    "text": "濃濃香蕉可可 $80",
                    "weight": "bold",
                    "margin": "sm",
                    "size": "md",
                    "wrap": True
                }]
                },
                'hero': {
                'type': 'image',
                'url':'https://i.pinimg.com/564x/53/14/f6/5314f6116951256cd5a974717424bf1e.jpg',
                'size': 'full',
                'aspectRatio': '1:1',
                'aspectMode': 'cover',
                },
                'body': {
                "type":"box",
                "layout":"vertical",
                "spacing":"sm",
                "contents": [
                    {
                    "type": "button",
                    "style": "secondary",
                    "color": "#F6DCCB",
                    "action": {
                        'type': 'postback',
                        'label': '濃濃香蕉可可',
                        'text': '想吃 濃濃香蕉可可',
                        'data': 'A&濃濃香蕉可可'
                    }
                    },
                ]
                }
            }
            ]
        })

        line_bot_api.reply_message(event.reply_token, flex_message)

    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='不'))


def sendback_num(event, backdata, num):
    try:
        message = TextSendMessage(
            text='請問要幾份',
            quick_reply=QuickReply(items=[
                QuickReplyButton(action=PostbackTemplateAction(label="1", text="1份", data='B&' + num + '&1')),
                QuickReplyButton(action=PostbackTemplateAction(label="2", text="2份", data='B&' + num + '&2')),
                QuickReplyButton(action=PostbackTemplateAction(label="3", text="3份", data='B&' + num + '&3')),
                QuickReplyButton(action=PostbackTemplateAction(label="4", text="4份", data='B&' + num + '&4')),
                QuickReplyButton(action=PostbackTemplateAction(label="5", text="5份", data='B&' + num + '&5')),

            ]))

        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='不買'))


def sendback_confirm(event, backdata, result, nn):
    try:
        food = result[0]
        amount = result[1]
        uid = nn

        price = menu[food]

        #將資料新增到資料庫
        unit = {"food":food, "price":price, "amount":amount, "uid":uid}
        
        with open("user_profile_bill_"+nn+".json", "a") as myfile:
        # with open("user_profile_bill.json", "a") as myfile:
          myfile.write(json.dumps(unit, sort_keys=True))
          myfile.write('\n')

        bubble = BubbleContainer(
            direction='ltr',
            header = BoxComponent(
                layout='vertical',
                #background_color='#DBD3D8',
                contents=[

                    TextComponent(
                        text = "已加入： " + amount + " 個 " + food,
                        size="md",
                        weight="bold",
                        ),
                    SeparatorComponent(
                        color="#C8BCC3",
                        margin="xxl"
                        ),
                    ]
                ),
            body = BoxComponent(
                layout='vertical',
                contents=[

                    TextComponent(
                        text = "\n一個單價：" + price
                        ),
                    TextComponent(
                        text = "\n"
                        ),
                    TextComponent(
                        text = "\n請問要結束購買嗎",
                        weight="bold",
                        ),

                ]
                ),
            footer=BoxComponent(
                layout='vertical',
                spacing='xs',
                contents=[
                    BoxComponent(
                        layout='horizontal',
                        spacing='xs',
                        contents=[
                            # ButtonComponent(
                            #     style='secondary',
                            #     color="#E8F1E4",
                            #     action=PostbackTemplateAction(
                            #         label='修改此筆訂單',
                            #         text='修改此筆訂單',
                            #         data='E'
                            #     )
                            #     ),
                            ButtonComponent(
                                style='secondary',
                                color="#C4DABB",
                                action=PostbackTemplateAction(
                                    label='繼續購物',
                                    text='繼續購物',
                                    data='C'
                                )
                                )

                            ]

                        ),
                    ButtonComponent(
                        style='secondary',
                        color="#F6DCCB",
                        action=PostbackTemplateAction(
                            label='結帳',
                            text='結帳',
                            data='D'
                        )

                        )

                    ]
                )

            )

        message = FlexSendMessage(alt_text="確認訂單",contents=bubble)
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='不'))


def sendButton_Again(event):
    try:
        message = TemplateSendMessage(
            alt_text='Buttons template',
            template = ButtonsTemplate(
                thumbnail_image_url="https://i.pinimg.com/750x/78/1b/49/781b4946957612bb5817112c534e4243.jpg",
                title='Menu',
                text='請問要哪個種類的司康',
                actions=[
                    PostbackTemplateAction(
                        label='經典司康',
                        text='經典司康',
                        data='action=經典司康'
                    ),
                    PostbackTemplateAction(
                        label='派式司康',
                        text='派式司康',
                        data='action=派式司康'
                    ),
                    PostbackTemplateAction(
                        label='夾醬司康',
                        text='夾醬司康',
                        data='action=夾醬司康'
                    )

                ]
            )

        )
        line_bot_api.reply_message(event.reply_token, message)

    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='不'))


def sendRECEIPT(event):
    try:
        messageA = []
        uu = event.source.user_id
        # with open("user_profile_bill.json", "r") as f:
        #     a = f.readlines()[0].strip()
        #     p = eval(a)["uid"]

        with open("user_profile_bill_"+uu+".json", "r") as f:
            j = len(f.readlines())

        # text1 = "您的訂購如下："
        foodA = ""
        priceA = ""
        amountA = ""
        final_total = 0
        m = 0

        for g in range(j):  # 巡迴在1~資訊總數
            if g == 0:  # 當此筆資料的id為c時拿取以下資料，此為第一筆資訊
                with open("user_profile_bill_"+uu+".json", "r") as f:
                    bill_list = eval(f.readlines()[g].strip())
                # if bill_list["uid"] == uu:
                foodA += "\n" + bill_list["food"]
                amountA += "\n" + bill_list["amount"]
                priceA += "\n" + bill_list["price"]

                total = int(bill_list["price"]) * int(bill_list["amount"])  # 算出總價

                m += int(bill_list["amount"])

                final_total += total

            else:
                with open("user_profile_bill_"+uu+".json", "r") as f:
                    bill_list = eval(f.readlines()[g].strip())
                # if bill_list["uid"] == uu:
                foodA += "\n" + bill_list["food"]
                amountA += "\n" + bill_list["amount"]
                priceA += "\n" + bill_list["price"]

                m += int(bill_list["amount"])

                total = int(bill_list["price"]) * int(bill_list["amount"])  # 算出總價

                final_total += total

        bubble = BubbleContainer(
                direction='ltr',
                header = BoxComponent(
                    layout='vertical',
                    contents=[

                        TextComponent(
                            text = "結帳 RECEIPT",
                            color = "#CCAE8F",
                            size="md",
                            weight="bold",
                            ),
                        TextComponent(
                            text = "司康販賣所",
                            # = "#1DB446",
                            size="35px",
                            weight="bold",
                            wrap=True,
                            margin="md"
                            ),
                        TextComponent(
                            text = "好吃的司康能讓您開心一整天!",
                            # = "#1DB446",
                            size="xs",
                            weight="bold",
                            color="#C8BCC3",
                            ),
                        SeparatorComponent(
                            color="#C8BCC3",
                            margin="xxl"
                            ),
                        BoxComponent(
                            layout="vertical",
                            margin="xxl",
                            spacing="sm",
                            contents=[
                                BoxComponent(
                                    layout="horizontal",
                                    contents=[
                                        TextComponent(
                                            text = '品項' ,
                                            color="#4B8F8C",
                                            flex=4,
                                            size="sm",
                                            wrap=True
                                            ),

                                        TextComponent(
                                            text =  '個' ,
                                            color="#4B8F8C",
                                            align="end",
                                            size="sm",
                                            wrap=True
                                            ),

                                        TextComponent(
                                            text =  '單價' ,
                                            color="#4B8F8C",
                                            align="end",
                                            size="sm",
                                            wrap=True
                                            ),
                                        ]
                                    ),
                                BoxComponent(
                                    layout="horizontal",
                                    contents=[
                                        TextComponent(
                                            text = foodA ,
                                            color="#555555",
                                            flex=4,
                                            wrap=True
                                            ),

                                        TextComponent(
                                            text =  amountA ,
                                            color="#111111",
                                            align="end",
                                            wrap=True
                                            ),
                                        TextComponent(
                                            text =  priceA ,
                                            color="#C171BD",
                                            align="end",
                                            wrap=True
                                            ),
                                        ]
                                    )
                                ]
                            ),
                        SeparatorComponent(
                            color="#C8BCC3",
                            margin="xxl"
                            ),
                        BoxComponent(
                            layout="vertical",
                            margin="xxl",
                            spacing="sm",
                            contents=[
                                BoxComponent(
                                    layout="horizontal",
                                    contents=[
                                        TextComponent(
                                            text = "司康總數" ,
                                            color="#555555",
                                            flex=0,
                                            wrap=True
                                            ),
                                        TextComponent(
                                            text =  str(m),
                                            color="#111111",
                                            align="end",
                                            wrap=True
                                            ),
                                        ]
                                    ),
                                BoxComponent(
                                    layout="horizontal",
                                    margin="xl",
                                    contents=[
                                        TextComponent(
                                            text = "總價" ,
                                            color="#C171BD",
                                            flex=0,
                                            size="xl",
                                            wrap=True
                                            ),
                                        TextComponent(
                                            text =  "$" + str(final_total),
                                            color="#C171BD",
                                            align="end",
                                            size="xl",
                                            wrap=True
                                            ),
                                        ]
                                    )
                                ]
                            ),

                        ]
                    ),



                )

        messageA.append(FlexSendMessage(alt_text="結帳",contents=bubble))
        messageA.append(TextSendMessage(text="我們會盡快幫您準備司康，請您稍等片刻~"))
        line_bot_api.reply_message(event.reply_token, messageA)

        with open("user_profile_bill_"+uu+".json", "w") as file:
            file.truncate(0)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='結帳錯誤'))


def sendback_location(event):
    try:
        flex_message = FlexSendMessage(
                alt_text='店家地址',
                contents={
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://i.pinimg.com/564x/54/a4/f6/54a4f6da1b417594b5c51addf7620cd2.jpg",
                    "size": "full",
                    "aspectRatio": "20:13",
                    "aspectMode": "cover"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                {
                    "type": "text",
                    "text": "司康販賣所 Scon📍",
                    "weight": "bold",
                    "size": "xl"
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "margin": "md",
                    "contents": [
                    {
                        "type": "icon",
                        "size": "sm",
                        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                    },
                    {
                        "type": "icon",
                        "size": "sm",
                        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                    },
                    {
                        "type": "icon",
                        "size": "sm",
                        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                    },
                    {
                        "type": "icon",
                        "size": "sm",
                        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                    },
                    {
                        "type": "icon",
                        "size": "sm",
                        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png"
                    },
                    {
                        "type": "text",
                        "text": "4.0",
                        "size": "sm",
                        "color": "#999999",
                        "margin": "md",
                        "flex": 0
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "baseline",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "text",
                            "text": "Place",
                            "color": "#aaaaaa",
                            "size": "sm",
                            "flex": 1
                        },
                        {
                            "type": "text",
                            "text": "No. XX號, Datong Rd, East District, Hsinchu City, 300",
                            "wrap": True,
                            "color": "#666666",
                            "size": "sm",
                            "flex": 5
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "text",
                            "text": "Time",
                            "color": "#aaaaaa",
                            "size": "sm",
                            "flex": 1
                        },
                        {
                            "type": "text",
                            "text": "14:30 - 19:00",
                            "wrap": True,
                            "color": "#666666",
                            "size": "sm",
                            "flex": 5
                        }
                        ]
                    }
                    ]
                }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                    "type": "uri",
                    "label": "LOCATION",
                    "uri": "https://goo.gl/maps/Lxz6W11bZBPQnm556"
                    }
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [],
                    "margin": "sm"
                }
                ],
                "flex": 0
            }
            }
            )

        line_bot_api.reply_message(event.reply_token, flex_message)

    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='不'))


def sendback_item(event):
    try:
        items_quick_reply = QuickReply(
            items=[
                QuickReplyButton(action=MessageAction(label="經典奶油司康", text="@經典奶油司康")),
                QuickReplyButton(action=MessageAction(label="伯爵茶司康", text="@伯爵茶司康")),
                QuickReplyButton(action=MessageAction(label="黑糖麻糬司康", text="@黑糖麻糬司康")),
                QuickReplyButton(action=MessageAction(label="烤布丁司康", text="@烤布丁司康")),
                QuickReplyButton(action=MessageAction(label="糖皮厚奶油芋頭", text="@糖皮厚奶油芋頭")),
                QuickReplyButton(action=MessageAction(label="香橙乳酪", text="@香橙乳酪")),
                QuickReplyButton(action=MessageAction(label="可可綠葡萄卡士達", text="@可可綠葡萄卡士達")),
                QuickReplyButton(action=MessageAction(label="濃濃香蕉可可", text="@濃濃香蕉可可"))
            ]
        )
        reply_message = TextSendMessage(text="嗨嗨👋是不是對我們的司康很好奇😎~\n您可以點選下方司康品項，或是直接上傳圖片，我們可以直接幫您辨識品項並給您相關的介紹！", quick_reply=items_quick_reply)
        line_bot_api.reply_message(event.reply_token, reply_message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='不買'))
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):


    message_text = event.message.text


    if message_text == '100kg':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='今天特別多'))
    elif message_text == '10kg':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='今天特別少!'))
    elif message_text == 'hi':
        message = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url='https://images.squarespace-cdn.com/content/v1/552eefd1e4b0c6b6fbd179cb/1610519910081-99MNAH3AFPQL6RE913IJ/Brown+and+Orange+Neutral+Delicate+Organic+Fashion+Marketing+Presentation.png',
            title='回報專區',
            text='請選擇',
            actions=[
                PostbackTemplateAction(
                    label='生乳量',
                    text='請問生乳含量是多少',
                    data='action=buy&itemid=1'
                ),
                MessageTemplateAction(
                    label='通知領取',
                    text='已通知物流來領取'
                ),
                URITemplateAction(
                    label='官網',
                    uri='https://www.bettermilk.com.tw/'
                )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message) 
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Please input valid keyword!'))


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

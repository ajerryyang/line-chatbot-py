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

    if message_text == '回報':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='This is keyword for @status!'))
    elif message_text == '@location':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='This is keyword for @location!'))
    elif message_text == '@register':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='This is keyword for @register!'))
    elif message_text == 'hi':
        line_bot_api.push_message('你的 user ID', TemplateSendMessage(
        alt_text='ConfirmTemplate',
        template=ConfirmTemplate(
                text='你好嗎？',
                actions=[
                    MessageAction(
                        label='好喔',
                        text='好喔'
                    ),
                    MessageAction(
                        label='好喔',
                        text='不好喔'
                    )
                ]
            )
        ))
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Please input valid keyword!'))


    

    
   

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

from flask import Flask, request, abort
import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


app = Flask(__name__)

USER_ID = os.environ["LINE_USER_ID"]
line_bot_api = LineBotApi(os.environ["LINE_ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["LINE_CHANNEL_SECRET"])

@app.route("/")
def hello_world():
    return "hello world!"

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

@handler.add(FollowEvent)
def main():
    pushText = TextSendMessage(text="勤怠を登録しますか？")
    line_bot_api.push_message(USER_ID, messages=pushText)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))            # Heroku側が空いたポートを探してくれる 固定ポートにするとアプリ落ちる
    app.run(host="0.0.0.0", port=port)
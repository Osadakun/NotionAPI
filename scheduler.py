from flask import Flask, request, abort
import os
import config

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = config.LINE_ACCESS_TOKEN
LINE_CHANNEL_SECRET = config.LINE_CHANNEL_SECRET
USER_ID = config.LINE_USER_ID
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

def main():
    pushText = TextSendMessage(text="勤怠を登録しますか？")
    line_bot_api.push_message(USER_ID, messages=pushText)

if __name__ == "__main__":
    main()
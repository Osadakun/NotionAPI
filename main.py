#!/usr/bin/env python3
# coding: utf-8
from linebot.models import *

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
import requests
import json
import os
from datetime import datetime as dt
import datetime
from flask import Flask, render_template, g, request, abort

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

url = "https://api.notion.com/v1/databases/%s/query" %os.environ["NOTION_DATABASE_ID"]
headers = {
  'Authorization': 'Bearer ' + os.environ["NOTION_ACCESS_TOKEN"],
  'Notion-Version': '2021-08-16',
  'Content-Type': 'application/json',
}
req = requests.post(url, headers=headers)
tasks = ""

USER_ID = os.environ["LINE_USER_ID"]
line_bot_api = LineBotApi(os.environ["LINE_ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["LINE_CHANNEL_SECRET"])

def slicer(item):                 # 文字列変換＋スライス(時間で必要なのが前10個分だから)
  item = str(item)[:10]
  item = item.replace("-", "")
  return item

today_now = str(dt.now() + datetime.timedelta(days=1))
today_now = slicer(today_now)

def notion(today_task):                     # Notionから情報を持ってくる
  for i in range(len(req.json()["results"])):
    try:
      quantity = req.json()['results'][i]['properties']['日付']['date']['start']
    except:
      line_bot_api.push_message(USER_ID, messages="バグ起きてるので確認してください！")
    else:
      pass
    times = quantity[11:16]
    t_date = slicer(quantity)
    if t_date == today_now:
      name = req.json()['results'][i]['properties']['名前']['title'][0]['plain_text']
      today_task[name] = times
    else:
      continue
  l = sorted(today_task.items(), key=lambda x: x[1])
  # l = sorted(today_task.items())
  today_task.clear()
  today_task.update(l)
  return today_task

def crate_task_list(task):
  today_task = {}
  inf = notion(today_task)                  # 今日のタスクが入る
  if inf == {}:
    return "明日のタスクはありません"
  for k, v in inf.items():
    task += v + "から" + k + "\n"
  task += "です！"
  return task

def main(text):
  pushText = TextSendMessage(text=text)
  line_bot_api.push_message(USER_ID, messages=pushText)

if __name__ == "__main__":
    main(crate_task_list("明日のタスクは\n"))
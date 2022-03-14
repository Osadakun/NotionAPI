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
from pprint import pprint
import json
import os
from datetime import datetime as dt
from flask import Flask, render_template, g, request, abort

app = Flask(__name__)

url = "https://api.notion.com/v1/databases/%s/query" %os.environ["LINE_ACCESS_TOKENNOTION_DATABASE_ID"]
headers = {
  'Authorization': 'Bearer ' + os.environ["LINE_ACCESS_TOKENNOTION_ACCESS_TOKEN"],
  'Notion-Version': '2021-08-16',
  'Content-Type': 'application/json',
}
r = requests.post(url, headers=headers)
today_task = {}                   # タスクが入る，辞書型で管理
today_task_time = {}              # タスクの開始時間が入る，辞書型で管理
tasks = ""

USER_ID = os.environ["LINE_USER_ID"]
line_bot_api = LineBotApi(os.environ["LINE_ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["LINE_CHANNEL_SECRET"])

def slicer(item):                 # 文字列変換＋スライス(時間で必要なのが前10個分だから)
  item = str(item)[:10]
  return item

today_now = str(dt.now())
today_now = slicer(today_now)

def notion(num):                     # Notionから情報を持ってくる
  for i in range(len(r.json()["results"])):
    name = r.json()['results'][i]['properties']['名前']['title'][0]['plain_text']
    quantity = r.json()['results'][i]['properties']['日付']['date']['start']
    times = quantity[11:16]
    quantity = slicer(quantity)      # 年月日だけ欲しいからスライス
    t_date = dt.strptime(quantity, "%Y-%m-%d")  # 取得した項目の日付
    t_date = slicer(t_date)
    if t_date == today_now:
      today_task[num] = name
      today_task_time[num] = times
      num += 1
  return today_task

def w_txt(tasks):
  inf = notion(1)                  # 今日のタスクが入る
  inf_count = len(inf)             # 何個あるか調べる
  if inf_count == 0:
    return "今日のタスクはありません"
  for i in range(1,inf_count+1):
    if i == inf_count:
      tasks += today_task_time[i] + "から" + today_task[i] + "\n" + "です！"
    else:
      tasks += today_task_time[i] + "から" + today_task[i] + "\n"
  return tasks

def main(text):
  pushText = TextSendMessage(text=text)
  line_bot_api.push_message(USER_ID, messages=pushText)

if __name__ == "__main__":
    main(w_txt("今日のタスクは\n"))
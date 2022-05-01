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
import config
from pprint import pprint
import json
from datetime import datetime as dt
import datetime
from flask import Flask, render_template, g, request, abort
import sys

app = Flask(__name__)

url = "https://api.notion.com/v1/databases/%s/query" %config.NOTION_DATABASE_ID
headers = {
  'Authorization': 'Bearer ' + config.NOTION_ACCESS_TOKEN,
  'Notion-Version': '2021-08-16',
  'Content-Type': 'application/json',
}
req = requests.post(url, headers=headers)
tasks = ""

USER_ID = config.LINE_USER_ID
line_bot_api = LineBotApi(config.LINE_ACCESS_TOKEN)
handler = WebhookHandler(config.LINE_CHANNEL_SECRET)

def slicer(item):                 # 文字列変換＋スライス(時間で必要なのが前10個分だから)
  item = str(item)[:10]
  item = item.replace("-", "")
  return item

today_now = str(dt.now() + datetime.timedelta(days=1))
today_now = slicer(today_now)

def notion(today_task):                     # Notionから情報を持ってくる
  for i in range(len(req.json()["results"])):
  # for i in range(3):
    for _ in range(3):  # 最大3回実行
      try:
        quantity = req.json()['results'][i]['properties']['日付']['date']['start']  # 失敗しそうな処理
        # print(req.json()['results'][i])
      except Exception as e:
        pass  # 必要であれば失敗時の処理
      else:
        break  # 失敗しなかった時はループを抜ける
    else:
      # pass
      print(req.json()['results'][i]['properties']['名前'])
      print(req.json()['results'][i])
      print(i)
      # pushText = TextSendMessage(text="明日の予定は自分で確認してね")
      # line_bot_api.push_message(USER_ID, messages=pushText)       # リトライが全部失敗した時の処理
      # sys.exit()
    # try:
    #   quantity = req.json()['results'][i]['properties']['日付']['date']['start']
    # except TypeError:
    #   pass
    # else:
    #   pass
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
  print("")
  # pushText = TextSendMessage(text=text)
  # line_bot_api.push_message(USER_ID, messages=pushText)

if __name__ == "__main__":
    main(crate_task_list("明日のタスクは\n"))
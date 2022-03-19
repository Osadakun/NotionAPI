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
import os
from datetime import datetime as dt
import datetime
from flask import Flask, render_template, g, request, abort

app = Flask(__name__)

url = "https://api.notion.com/v1/databases/%s/query" %config.NOTION_DATABASE_ID
headers = {
  'Authorization': 'Bearer ' + config.NOTION_ACCESS_TOKEN,
  'Notion-Version': '2021-08-16',
  'Content-Type': 'application/json',
}
req = requests.post(url, headers=headers)
# today_task = {}                   # タスクが入る，辞書型で管理
# today_task_time = {}              # タスクの開始時間が入る，辞書型で管理
# today_match_task = {}
tasks = ""

USER_ID = config.LINE_USER_ID
line_bot_api = LineBotApi(config.LINE_ACCESS_TOKEN)
handler = WebhookHandler(config.LINE_CHANNEL_SECRET)

def slicer(item):                 # 文字列変換＋スライス(時間で必要なのが前10個分だから)
  item = str(item)[:10]
  item = item.replace("-", "")
  return item

# def matching(num):                # タスク内容と時間で辞書を作り直す関数
#   for i in range(1,num+1):
#     task = today_task[i]
#     time = today_task_time[i]
#     today_match_task[time] = task
#   today_match_task = sorted(today_match_task.items())
#   return today_match_task

today_now = str(dt.now() + datetime.timedelta(days=1))
today_now = slicer(today_now)

def notion(today_task):                     # Notionから情報を持ってくる
  for i in range(len(req.json()["results"])):
    quantity = req.json()['results'][i]['properties']['日付']['date']['start']
    times = quantity[11:16]
    t_date = slicer(quantity)
    if t_date == today_now:
      name = req.json()['results'][i]['properties']['名前']['title'][0]['plain_text']
      today_task[times] = name
    else:
      continue
    today_task = sorted(today_task.items())
    return today_task
  #   name = req.json()['results'][i]['properties']['名前']['title'][0]['plain_text']
  #   quantity = slicer(quantity)      # 年月日だけ欲しいからスライス
  #   t_date = dt.strptime(quantity, "%Y-%m-%d")  # 取得した項目の日付
  #   t_date = slicer(t_date)
  #   print(t_date)
  #   if t_date == today_now:
  #     today_task[num] = name
  #     today_task_time[num] = times
  #     num += 1
  # return today_task

def crate_task_list(task):
  today_task = {}
  inf = notion(today_task)                  # 今日のタスクが入る
  print(inf)
  if inf == {}:
    return "明日のタスクはありません"
  # inf_count = len(inf)             # 何個あるか調べる
  # for k, v in inf.items():
  #   task += k + "から" + v + "\n"
  # return task
  # for i in range(1,inf_count+1):
  #   if i == inf_count:
  #     tasks += today_task_time[i] + "から" + today_task[i] + "\n" + "です！"
  #   else:
  #     tasks += today_task_time[i] + "から" + today_task[i] + "\n"
  # return tasks

def main(text):
  pushText = TextSendMessage(text=text)
  line_bot_api.push_message(USER_ID, messages=pushText)

if __name__ == "__main__":
    # print(main(crate_task_list("今日のタスクは\n")))
    main(crate_task_list("明日のタスクは\n"))
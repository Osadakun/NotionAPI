#!/usr/bin/env python3
# coding: utf-8
import requests
import config
from pprint import pprint
import json
from datetime import datetime as dt

url = "https://api.notion.com/v1/databases/%s/query" %config.NOTION_DATABASE_ID
headers = {
  'Authorization': 'Bearer ' + config.NOTION_ACCESS_TOKEN,
  'Notion-Version': '2021-08-16',
  'Content-Type': 'application/json',
}
r = requests.post(url, headers=headers)
today_task = {}                   # タスクが入る，辞書型で管理
tasks = ""
tasks_number = 1

def slicer(item):                 # 文字列変換＋スライス(時間で必要なのが前10個分だから)
  item = str(item)[:10]
  return item

today_now = str(dt.now())
today_now = slicer(today_now)

def notion():                     # Notionから情報を持ってくる
  for i in range(len(r.json()["results"])):
    name = r.json()['results'][i]['properties']['名前']['title'][0]['plain_text']
    quantity = r.json()['results'][i]['properties']['日付']['date']['start']
    quantity = slicer(quantity)      # 年月日だけ欲しいからスライス
    t_date = dt.strptime(quantity, "%Y-%m-%d")  # 取得した項目の日付
    t_date = slicer(t_date)
    if t_date == today_now:
      today_task[tasks_number] = name
      tasks_number += 1
  return today_task

def w_txt():
  inf = notion()                  # 今日のタスクが入る
  inf_count = len(inf)            # 何個あるか調べる
  if inf_count == 0:
    return "今日のタスクはありません"
  for i in range(1,inf_count+1):
    if i == inf_count:
      tasks += today_task + "です！"
    else:
      tasks += today_task[i] + "と"
  return tasks

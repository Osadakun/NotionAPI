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


def slicer(item):                 # 文字列変換＋スライス(時間で必要なのが前10個分だから)
  item = str(item)[:10]
  return item

today_date = str(dt.now())
today_date = slicer(today_date)

def notion():                     # Notionから情報を持ってくる
  for i in range(len(r.json()["results"])):
    name = r.json()['results'][i]['properties']['名前']['title'][0]['plain_text']
    quantity = r.json()['results'][i]['properties']['日付']['date']['start']
    quantity = slicer(quantity)      # 年月日だけ欲しいからスライス
    tdate = dt.strptime(quantity, "%Y-%m-%d")
    tdate = slicer(tdate)
    if tdate == today_date:
      today_task[name] = tdate
  return today_task
  # return today_task
  # print(today_task)
print(notion())
def w_txt():
  # f = open("memo.txt", "w", encoding="UTF-8")
  inf = notion()
  today_now = str(dt.now())       # datetime型ではスライス使えない
  today_now = today_now[:10]      # 年月日だけ欲しいからスライス
  today_now = dt.strptime(today_now, "%Y-%m-%d")
  x = today_task.get(today_now)   # 今日にタスクあるかどうか確認
  # f.write(x)
  # f.close()
  # print(inf)
  # print(("--------------"))
  # print(today_now)
  # print(("--------------"))
  # print(x)
  # print(("--------------"))

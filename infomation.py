#!/usr/bin/env python
# coding: utf-8
import requests
import config
from pprint import pprint
import json
from datetime import datetime

url = "https://api.notion.com/v1/databases/%s/query" %config.NOTION_DATABASE_ID
headers = {
  'Authorization': 'Bearer ' + config.NOTION_ACCESS_TOKEN,
  'Notion-Version': '2021-08-16',
  'Content-Type': 'application/json',
}
r = requests.post(url, headers=headers)
today_task = {}

def notion():
  for i in range(len(r.json()["results"])):
    name = r.json()['results'][i]['properties']['名前']['title'][0]['plain_text']
    quantity = r.json()['results'][i]['properties']['日付']['date']['start']
    quantity = quantity[:10]
    tdate = datetime.strptime(quantity, "%Y-%m-%d")
    today_task[tdate] = name
  return today_task

def w_txt():
  f = open("memo.txt", "w", encoding="UTF-8")
  inf = notion()
  today_now = datetime.datetime.now()
  x = today_task.get(today_now)
  f.writelines(x)
  f.close()
#!/usr/bin/env python3
# coding: utf-8
import schedule
from time import sleep
import main

def task():       # 定期実行
  print(main.w_txt("今日の予定は"))

schedule.every(3).seconds.do(task)

while True:
  schedule.run_pending()
  sleep(1)
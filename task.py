import schedule
from time import sleep
import information

def task():
  information.w_txt()

schedule.every(3).seconds.do(task)

while True:
  schedule.run_pending()
  sleep(1)
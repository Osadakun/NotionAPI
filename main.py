import requests
import config
from pprint import pprint
import json

url = "https://api.notion.com/v1/databases/%s/query" %config.NOTION_DATABASE_ID
headers = {
  'Authorization': 'Bearer ' + config.NOTION_ACCESS_TOKEN,
  'Notion-Version': '2021-08-16',
  'Content-Type': 'application/json',
}
r = requests.post(url, headers=headers)
for i in range(len(r.json()["results"])+1):
  name = r.json()['results'][i]['properties']['名前']['title'][0]['plain_text']
  quantity = r.json()['results'][i]['properties']['日付']['date']['start']
  quantity = quantity[:10]
  print('%s: %s' %(name, quantity))
# pprint(r.json(), sort_dicts=False)
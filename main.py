import requests
import config

url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"
headers = {
  'Authorization': 'Bearer ' + NOTION_ACCESS_TOKEN,
  'Notion-Version': '2021-05-13',
  'Content-Type': 'application/json',
}
r = requests.post(url, headers=headers)
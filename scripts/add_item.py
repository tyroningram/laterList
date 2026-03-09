import requests

API_URL = "http://127.0.0.1:8000/items"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImlkIjoxLCJleHAiOjE3NzMwODcwNjd9.y4ka4ZAlj1ZHNR4g8wXy84bEdSM41Mgmqfxrmdtle08"

title: str = input("Title: ")
media_type = input("Type: ")
notes: str = input("Any notes: ")


{
  "title": "string",
  "media_type": "movie",
  "status": "planned",
  "notes": "string",
  "rating": 0,
  "priority": 0
}


payload = {
    "title": title,
    "media_type": media_type,
    "status": "planned",
    "notes": notes,
    "rating": 0,
    "priority": 0
}

headers = {
    "Authorization": f"Bearer {TOKEN}"
}

response = requests.post(API_URL, json=payload, headers=headers)

print(f"Status code: {response.status_code}")

if response.ok:
    print("Item added!")
else:
    print("Error:")
    print(response.text)
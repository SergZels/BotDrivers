import requests
import json
URL = 'http://127.0.0.1:8000/dr/'
id=852

x = requests.get(f"{URL}codidbycode", params={"cod":id}).json()
if len(x)>0 :
    print(x[0]['id'])

#x = requests.post(f"http://127.0.0.1:8000/dr/driveridbytelid", json={"telegramId": "159"})
#data = x.json()  # Парсинг JSON-відповіді
# driver_id = data["id"]  # Отримання значення "id"



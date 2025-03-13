import requests

API_KEY = "ТВОЙ_API_KEY"
url = "https://api.deutschebahn.com/freeplan/v1/location.name"
params = {"input": "Berlin"}

headers = {"Authorization": f"Bearer {API_KEY}"}

response = requests.get(url, params=params, headers=headers)

if response.status_code == 200:
    print(response.json())  # Выведет список станций с кодами
else:
    print(f"Ошибка: {response.status_code} - {response.text}")
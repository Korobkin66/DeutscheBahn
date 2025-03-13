import requests

# Конфигурация
CLIENT_ID = '7b61ee043a945260d2fefbcf867ee8c0'
CLIENT_SECRET = '8f4ad462350ee13f932a3aa4a42663b8'
# USERNAME = "MY_LOGIN"
# PASSWORD = "MY_PASSWORD"
TOKEN_URL = 'https://api.deutschebahn.com/freeplan/v1/oauth/token'

# Запрос токена
response = requests.post(
    TOKEN_URL,
    data={'grant_type': 'client_credentials'},
    auth=(CLIENT_ID, CLIENT_SECRET)
)

# Проверка ответа
if response.status_code == 200:
    token_info = response.json()
    access_token = token_info['access_token']
    print(f"Access Token: {access_token}")
else:
    print(f"Ошибка получения токена: {response.status_code}")
    print(response.text)



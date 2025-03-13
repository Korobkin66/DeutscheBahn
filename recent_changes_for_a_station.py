import requests

url = "https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1/rchg/REPLACE_EVANO"

headers = {
    "DB-Client-Id": "7b61ee043a945260d2fefbcf867ee8c0",
    "DB-Api-Key": "8f4ad462350ee13f932a3aa4a42663b8",
    "accept": "application/xml"
}

response = requests.get(url, headers=headers)

print(response.text)
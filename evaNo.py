# Returns all known changes for a station


import requests
from datetime import datetime

import sqlite3

# url = "https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1/fchg/8000226"
url = "https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1/fchg/"

headers = {
    "DB-Client-Id": "7b61ee043a945260d2fefbcf867ee8c0",
    "DB-Api-Key": "8f4ad462350ee13f932a3aa4a42663b8",
    "accept": "application/xml"
}

conn = sqlite3.connect('DB.db')
cursor = conn.cursor()
cursor.execute('''
SELECT eva
FROM stations
''')

station_number = [row[0] for row in cursor.fetchall()]
# station_number = cursor.fetchall()
conn.close()
# print(station_number)

for station in station_number:

    response = requests.get(url+station, headers=headers)
    folder = 'known_changes_folder'
    dt = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

    with open(f'{folder}/{station}_{dt}.xml', 'wb') as foutput:
        foutput.write(response.content)

# print(response.text)

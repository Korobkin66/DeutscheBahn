import requests
from datetime import datetime

import sqlite3

# url = "https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1/plan/REPLACE_EVANO/REPLACE_DATE/REPLACE_HOUR"
url = "https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1/plan/"

headers = {
    "DB-Client-Id": "7b61ee043a945260d2fefbcf867ee8c0",
    "DB-Api-Key": "8f4ad462350ee13f932a3aa4a42663b8",
    "accept": "application/xml"
}

conn = sqlite3.connect('/opt/airflow/DB.db')
cursor = conn.cursor()
cursor.execute('''
SELECT eva
FROM stations
''')

station_number = [row[0] for row in cursor.fetchall()]
# station_number = cursor.fetchall()
conn.close()

for station in station_number:

    dt_plan = datetime.today().strftime('%y%m%d/%H')
    response = requests.get(f'{url}/{station}/{dt_plan}', headers=headers)
    folder = '/opt/airflow/plan_data_folder'
    dt = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

    with open(f'{folder}/plan_d-{station}_{dt}.xml', 'wb') as foutput:
        foutput.write(response.content)


# response = requests.get(url, headers=headers)

# print(response.text)
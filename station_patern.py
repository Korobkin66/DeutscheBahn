import requests
import sqlite3
import xml.etree.ElementTree as ET


class StationDatabase:
    def __init__(self, db_name="DB.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS stations (
                meta TEXT,
                name TEXT,
                eva TEXT,
                ds100 TEXT,
                db TEXT,
                creationts TEXT
            )
        ''')
        self.conn.commit()

    def insert_station(self, station):
        self.cursor.execute('''
            INSERT INTO stations VALUES (?, ?, ?, ?, ?, ?)
        ''', station)
        self.conn.commit()

    def close(self):
        self.conn.close()


def fetch_stations():
    url = "https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1/station/HWOB"
    headers = {
        "DB-Client-Id": "7b61ee043a945260d2fefbcf867ee8c0",
        "DB-Api-Key": "8f4ad462350ee13f932a3aa4a42663b8",
        "accept": "application/xml"
    }
    response = requests.get(url, headers=headers)
    return response.text if response.status_code == 200 else None


def parse_stations(xml_data):
    root = ET.fromstring(xml_data)
    for station in root.findall("station"):
        yield (
            station.get("meta"), station.get("name"), station.get("eva"),
            station.get("ds100"), station.get("db"), station.get("creationts")
        )


if __name__ == "__main__":
    db = StationDatabase()
    xml_data = fetch_stations()
    if xml_data:
        for station in parse_stations(xml_data):
            db.insert_station(station)
        print("Данные сохранены в БД.")
    db.close()


# # Returns information about stations matching the given pattern


# import requests

# url = "https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1/station/HWOB"

# headers = {
#     "DB-Client-Id": "7b61ee043a945260d2fefbcf867ee8c0",
#     "DB-Api-Key": "8f4ad462350ee13f932a3aa4a42663b8",
#     "accept": "application/xml"
# }

# response = requests.get(url, headers=headers)

# print(response.text)


# # HH HB AHS HWOB

# # import xml.etree.ElementTree as ET
# # import csv

# # # Разбор XML
# # root = ET.fromstring(response.text)

# # # Открываем CSV-файл для записи
# # with open("stations.csv", mode="w", newline="", encoding="utf-8") as file:
# #     writer = csv.writer(file)
# #     writer.writerow(["meta", "name", "eva", "ds100", "db", "creationts"])  # Заголовки

# #     for station in root.findall("station"):
# #         writer.writerow([
# #             station.get("meta"),
# #             station.get("name"),
# #             station.get("eva"),
# #             station.get("ds100"),
# #             station.get("db"),
# #             station.get("creationts")
# #         ])

# # print("Данные сохранены в stations.csv")
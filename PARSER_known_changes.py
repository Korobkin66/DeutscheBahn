import os
import xml.etree.ElementTree as ET
import sqlite3

# Посмотреть изменились ли properties в описании!!!

 
class KC_TrainSchedule:
    def __init__(self, db_name="DB.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS kc_schedule (
                id TEXT,
                station TEXT,
                category TEXT,
                number INT,
                ar_time DATETIME,
                ar_platform TEXT,
                ar_route TEXT,
                dp_time DATETIME,
                dp_platform TEXT,
                dp_route TEXT
            )
        ''')  # number text ???
        self.conn.commit()

    def insert_kc_schedule(self, plan_schedule):
        self.cursor.execute('''
            INSERT INTO kc_schedule VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', plan_schedule)
        self.conn.commit()

    def close(self):
        self.conn.close()


class TrainScheduleParser:
    def __init__(self, xml_file):
        self.tree = ET.parse(xml_file)
        self.root = self.tree.getroot()

    def parse(self):
        station_name = self.root.get("station")
        schedule = []

        for train in self.root.findall("s"):
            train_data = {"id": train.get("id"), "details": {}}

            tl = train.find("tl")
            if tl is not None:
                if tl.get("c") in ["ICE", "IC"]:
                    train_data["details"] = {
                        "station": station_name,
                        "category": tl.get("c"),
                        "number": tl.get("n"),
                    }

                    ar = train.find("ar")
                    if ar is not None:
                        train_data["arrival"] = {
                            "time": ar.get("pt"),
                            "platform": ar.get("pp"),
                            "route": ar.get("ppth")
                        }

                    dp = train.find("dp")
                    if dp is not None:
                        train_data["departure"] = {
                            "time": dp.get("pt"),
                            "platform": dp.get("pp"),
                            "route": dp.get("ppth")
                        }

                    schedule.append(train_data)

        return schedule


def parse_plan_data(schedule):
    for train in schedule:
        yield (
            train['id'], train["details"]["station"], train["details"]["category"], 
            train["details"]["number"], train["arrival"]["time"], train["arrival"]["platform"],
            train["arrival"]["route"], train["departure"]["time"], train["departure"]["platform"],
            train["departure"]["route"]
        )


if __name__ == "__main__":
    folder_path = "known_changes_folder"
    db = KC_TrainSchedule()

    for filename in os.listdir(folder_path):
        if filename.endswith(".xml"):  
            file_path = os.path.join(folder_path, filename)

            parser = TrainScheduleParser(file_path)
            parsed_data = parser.parse()
            for station in parse_plan_data(parsed_data):
                db.insert_kc_schedule(station)
            print("Данные сохранены в БД.")
            db.close()


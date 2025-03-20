import os
import xml.etree.ElementTree as ET  # посмотреть

folder = 'plan_data_folder'

# walk()

for root, _, files in os.walk(folder):
    for file in files:
        if file.endswith(".xml"):
            file_path = os.path.join(root, file)
            tree = ET.parse(file_path)
            root_element = tree.getroot()  # timetable
            print(f"Файл: {file_path}, Корневой элемент: {root_element.tag}")

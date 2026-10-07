from pathlib import Path
import shutil

import requests
import json
import csv

all_data = []

for _ in range(3):
    api_response = requests.get("https://api.adviceslip.com/advice")

    res_dict = json.loads(api_response.content)
    data = [
        res_dict['slip']['id'],
        res_dict['slip']['advice'],
    ]
    print(f"현재 데이터: {data}")
    all_data.append(data)

print(f"전체 데이터: {all_data}")

export_file = "export_file.csv"

with open(export_file, 'w') as fp:
    csv_writer = csv.writer(fp, delimiter='|')
    csv_writer.writerows(all_data)

file = "json_file.csv"

destination = Path("chapter4/data") / file
shutil.copy2(export_file, destination)
print("완료")

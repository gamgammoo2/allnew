import pandas as pd
import json

csv_data = pd.read_csv("월별_발생건수_20230525121327.csv", sep = ",")
data_dict = csv_data.to_dict(orient="records")
final_dict = {"fire": data_dict}

#기존의 파일을 읽고 나서 데이터를 병합해야함.
with open("../json_server.json", "r",encoding="utf-8") as json_file:
    existing_data=json.load(json_file)

existing_data.update(final_dict)

with open("../json_server.json", "w",encoding="utf-8") as json_file:
    json.dump(existing_data,json_file,ensure_ascii=False)

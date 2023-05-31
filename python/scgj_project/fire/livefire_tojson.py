import pandas as pd
import json

#이상한 외계어로 나와서 인코딩을 시li줌
csv_data = pd.read_csv("sanbul.csv", sep = ",", encoding="utf-8")
csv_data = csv_data.dropna()
data_dict = csv_data.to_dict(orient="records")
final_dict = {"sanbul": data_dict}

with open("../json_server.json", "w",encoding="utf-8") as json_file:
    json.dump(final_dict, json_file, ensure_ascii=False)
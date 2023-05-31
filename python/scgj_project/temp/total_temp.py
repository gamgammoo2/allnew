import pandas as pd
import json

csv_data = pd.read_csv("2018_2023_temp.csv", sep = ",",encoding="utf-8")
csv_data = csv_data.fillna("")
data_dict = csv_data.to_dict(orient="records")
final_dict = {"totaltemp": data_dict}

with open("../json_server2.json", "w",encoding="utf-8") as json_file:
    json.dump(final_dict,json_file,ensure_ascii=False)

import pandas as pd
import json

csv_data = pd.read_csv("월별_발생건수_20230525121327.csv", sep = ",")
data_dict = csv_data.to_dict(orient="records")
final_dict = {"fire": data_dict}

with open("../fire.json", "w") as json_file:
    json.dump(final_dict, json_file, ensure_ascii=False)

import pandas as pd
import json

with open('patcpp113_40.4.json', encoding='utf-8') as f:
    data = json.loads(f.read())

    jsonBody = pd.json_normalize(data)

    csvBody = jsonBody.to_csv("patcpp113_40.4.csv")
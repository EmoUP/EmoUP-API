import pandas as pd
import requests
import json 

df = pd.read_csv('./Batch Upload/input.csv')
df['mobile'].fillna(0, inplace = True)
df.fillna('Not Given', inplace = True)
for i in range(len(df)):
    data = {
        "name": df['fullname'][i],
        "gender": df['gender'][i],
        "mobile": int(df['mobile'][i]),
        "degree": df['degree'][i],
        "consultation_place": df['consultation_place'][i],
        "about_doctor": df['about_doctor'][i],
        "services_provided": df['services_provided'][i],
        "address": df['address'][i],
        "latitude": df['latitude'][i],
        "longitude": df['longitude'][i],
        "ratings": int(df['ratings'][i])
    }
    url = 'http://localhost:5000/doctors'

    x = requests.post(url, data = json.dumps(data))
    print(x.status_code)
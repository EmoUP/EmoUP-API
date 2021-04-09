import pandas as pd
import requests
import json

df = pd.read_csv('./Batch Upload/final_music.csv')
print(df)

for i in range(len(df)):
    data = {
        'spotify_id': df['id'][i],
        'name': df['name'][i],
        'cluster': int(df['Cluster'][i]),
        'number_of_likes': int(df['popularity'][i])
    }

    x = requests.post('http://localhost:5000/musics', data = json.dumps(data))
    print(x.status_code)
    
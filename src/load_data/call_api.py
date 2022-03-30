import os
from dotenv import load_dotenv

import pandas as pd
import requests
from datetime import datetime, timedelta


load_dotenv()

SNCF_KEY = os.getenv("SNCF_API_KEY")

URL_BASE = "https://ressources.data.sncf.com//api/records/1.0/search/?dataset=tgvmax"
PARAMS = {'Authentification':SNCF_KEY}

def retrieve_tgvmax_at_date(PARAMS, URL_BASE, query_date):
    QUERY = f"&rows=-1&refine.date={query_date}"

    r = requests.get(url = URL_BASE + QUERY, params = PARAMS)
    data_json = r.json()
    
    try:
        if data_json['nhits'] >= 10000:
            print('more results availables')
        return pd.DataFrame([record['fields'] for record in data_json['records']])

    except Exception as exc:
        print(exc)
        return pd.DataFrame()

def main():
    MAX_DAY_AHEAD = 2

    today = datetime.utcnow().date()
    dfs = []
    data_json_empty = False

    for day_ahead in range(MAX_DAY_AHEAD+1):
        query_date = today + timedelta(day_ahead)
        print(query_date)
        df = retrieve_tgvmax_at_date(PARAMS, URL_BASE, query_date)

        if df.empty:
            pass
        else:
            dfs.append(df)

    data = pd.concat(dfs)

    data.to_csv(f'data/load_{datetime.utcnow()}.csv') 

if __name__ == '__main__':
    main()

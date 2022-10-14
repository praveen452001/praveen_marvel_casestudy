import json
import requests
import hashlib
import datetime
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from pprint import pprint as pp
import os

load_dotenv()
pub_key=os.getenv('pub_key')
priv_key=os.getenv('priv_key')
ts= '2'

def hash_params():
    temp=f'{ts}{priv_key}{pub_key}'
    hash_md5 = hashlib.md5()
    hash_md5.update(temp.encode('utf-8'))
    hashed_params = hash_md5.hexdigest()

    return hashed_params

temp_dict= {'character_name':[], 'character_id':[], 'number of event appearances/availability':[], 'number of series appearances/availability':[], 'number of stories appearances/availability':[], 'number of comics appearances/availability':[]}
for i in range(3):
    params = {'ts': '2', 'apikey': pub_key, 'hash': hash_params(), 'limit': '100', 'offset': 100*i}
    headers= {'Content-Type': 'application/json'}
    res = requests.get('https://gateway.marvel.com:443/v1/public/characters', params=params, headers=headers, verify=False)
    res.raise_for_status()
    results = res.json()
    for j in results['data']['results']:
        temp_dict['character_id'].append(j['id'])
        temp_dict['character_name'].append(j['name'])
        temp_dict['number of comics appearances/availability'].append(j['comics']['available'])
        temp_dict['number of series appearances/availability'].append(j['series']['available'])
        temp_dict['number of event appearances/availability'].append(j['events']['available'])
        temp_dict['number of stories appearances/availability'].append(j['stories']['available'])
    
df=pd.DataFrame(temp_dict)
print(df)

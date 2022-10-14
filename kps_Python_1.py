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

params = {'ts': '2', 'apikey': pub_key, 'hash': hash_params(), 'nameStartsWith': "S", 'limit': '100'}
headers= {'Content-Type': 'application/json'}
res = requests.get('https://gateway.marvel.com:443/v1/public/characters',
                   params=params, headers=headers, verify=False)

results = res.json()
pp(results['data']['count'])
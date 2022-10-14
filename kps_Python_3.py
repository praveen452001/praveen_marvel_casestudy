#Import Necessary Libraries
#Ensure all the libraries are present in the virtual env
import json
import requests
import hashlib
import datetime
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from pprint import pprint as pp
import os

#take the public key, private key and time stamp. We can also encode the keys and call it using os.getenv()
load_dotenv()
pub_key=os.getenv('pub_key')
priv_key=os.getenv('priv_key')
ts= '2'

#function to generate hash params
def hash_params():
    temp=f'{ts}{priv_key}{pub_key}'
    hash_md5 = hashlib.md5()
    hash_md5.update(temp.encode('utf-8'))
    hashed_params = hash_md5.hexdigest()

    return hashed_params

temp_dict= {'character_name':[], 'character_id':[], 'number of event appearances/availability':[], 'number of series appearances/availability':[], 'number of stories appearances/availability':[], 'number of comics appearances/availability':[]}

#function to print the required columns in the dataframe
def activity_3(api, hash_fun, n_char):
    ''' The function will return an error for missing api and hash parameter. For every character present in the 
    list of characters we can loop it using a for loop and we must also take care that all the records are present in the dataframe wherever the match us found'''
    try:
        if(hash_fun==''):
            raise(hash_error(''))
        elif(api==''):
            raise(api_error(''))
        for i in n_char:
            temp_offset_count=0
            true_count=100
            while(true_count==100):
                params = {'ts': '2', 'apikey': api, 'hash': hash_fun, 'limit': 100,'offset': 100*(temp_offset_count), 'nameStartsWith':i}
                headers= {'Content-Type': 'application/json'}
                res = requests.get('https://gateway.marvel.com:443/v1/public/characters', params=params, headers=headers, verify=False)
                res.raise_for_status()
                results = res.json()
                true_count=results['data']['count']
                temp_offset_count+=1
                if results['data']['count']>0:
                    for j in results['data']['results']:
                        temp_dict['character_id'].append(j['id'])
                        temp_dict['character_name'].append(j['name'])
                        temp_dict['number of comics appearances/availability'].append(j['comics']['available'])
                        temp_dict['number of series appearances/availability'].append(j['series']['available'])
                        temp_dict['number of event appearances/availability'].append(j['events']['available'])
                        temp_dict['number of stories appearances/availability'].append(j['stories']['available'])
        df=pd.DataFrame(temp_dict)
        print(df)
    #We print the equivalent error statements here
    except hash_error as error:
        print("Hash param null error")
    except api_error as error:
        print("API param null error")
        
class hash_error(Exception):
    def __init__(self,value):
        self.value=value
    def __str__(self):
        return(repr(self.value))
class api_error(Exception):
    def __init__(self,value):
        self.value=value
    def __str__(self):
        return(repr(self.value))

result_df=activity_3(pub_key,hash_params(),["S", "a"])


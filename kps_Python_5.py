#Import Necessary Libraries
#Ensure all the libraries are present in the virtual env
import requests #to request an api call
import hashlib #to generate hash keys
import datetime #if we want to generate a dynamic ts
import pandas as pd #for creating dataframe
from dotenv import load_dotenv #for securing our public and private keys
from pprint import pprint as pp #for printing results
import os
#the below listed functions are the created functions encapsulated in a package named mypackage
from mypackage.hash_func import hash_params
from mypackage.filter_data import activity_3
from mypackage.filter_rows import input_filter
from mypackage.filter_data_condition import filter_data
import argparse

#take the public key, private key and time stamp. We can also encode the keys and call it using os.getenv()
'''load_dotenv()
pub_key=os.getenv('pub_key')
priv_key=os.getenv('priv_key')'''

#Here we are dynamically trying to input the public and private keys from the user to connect to the api
ts= '2'
parser= argparse.ArgumentParser(description="Enter Keys")
parser.add_argument('pub_key', type=str, help='Enter Public Key')
parser.add_argument('priv_key', type=str, help='Enter Private Key')
args=parser.parse_args()
pub_key= getattr(args, 'pub_key', 'Public Key Not Entered')
priv_key=getattr(args, 'priv_key', 'Private Key Not Entered')

api_key=pub_key

#We have declared the list of columns in out dataframe using an dictionary 
temp_dict= {'character_name':[], 'character_id':[], 'number_of_event_appearances':[], 'number_of_series_appearances':[], 'number_of_stories_appearances':[], 'number_of_comics_appearances':[]}

#Enter the filter data conditions
#print("Enter no of characters you want to look for based on character starting letter")
#n= int(input())
#lst=[]
#print("Enter the characters one by one")
#for i in range(0, n):
#    ele = str(input())
#    lst.append(ele)

#This function return the hash value
hash_parameters= hash_params(ts,priv_key,pub_key)

lst=filter_data()
#This function returns the filtered dataframe
result_df=activity_3(temp_dict,api_key, hash_parameters, lst)

#This function returns a further column filtered dataframe based on the filtered data in the previous step
final_df= input_filter(result_df)

#Resultant df
print(final_df)
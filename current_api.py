import pandas as pd
import requests
import json
import pickle
from datetime import datetime
import schedule
import time


print("Type the API Key below")

while(True):
    API_key = input()
    test = requests.get("http://api.openweathermap.org/data/2.5/weather?q=%s&appid=%s"%('Mumbai',API_key))
    if test.status_code == 200:
        print("API key accepted. Extracting Data")
        break
    else:
        print("API Key doesn't work. Enter it again")

cities = ['Bangalore','Mumbai','New York','Dubai','London','Mexico']

try:
    df_current = pd.read_csv('current.csv')
except:
    df_current = pd.DataFrame(columns =['city','dt','temp_c','temp_f','visibility','wind_deg','wind_speed','wind_gust','clouds'])

def current(city):
    url = "http://api.openweathermap.org/data/2.5/weather?q=%s&appid=%s"%(city,API_key)
    r = requests.get(url).json()
    d = {'visibility':r['visibility'], 'city':city, 'dt':datetime.fromtimestamp(r['dt']), 'clouds':r['clouds']['all'],
    'temp_c':r['main']['temp']-273, 'temp_f':(r['main']['temp']-273)*9/5+32}
    d.update({"wind_"+k:v for k,v in r['wind'].items()})
    return d

def update_data(df_current):
    temp = pd.DataFrame(columns =['city','dt','temp_c','temp_f','visibility','wind_deg','wind_speed','wind_gust','clouds'])
    
    for city in cities:
        d = current(city)
        temp = temp.append(d, ignore_index=True)

    df_current = df_current.append(temp,ignore_index=True)
    df_current.to_csv('current.csv',index=False)
    print("API called. Database updated!")


schedule.every(5).minutes.do(update_data,df_current)
# i = 0
while True:
	schedule.run_pending()
	# print('Iteration:', i+1)
	# i+=1
	time.sleep(1)
	
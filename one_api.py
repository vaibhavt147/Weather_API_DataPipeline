import pandas as pd
import requests
import json
import pickle
from datetime import datetime

print("Type the API Key below")

while(True):
    API_key = input()
    test = requests.get("http://api.openweathermap.org/data/2.5/weather?q=%s&appid=%s"%('Mumbai',API_key))
    if test.status_code == 200:
        print("API key accepted. Extracting Data")
        break
    else:
        print("API Key doesn't work. Enter it again")

def get_coord(cities):
    d = {}
    for city in cities:
        url2 = "http://api.openweathermap.org/data/2.5/weather?q=%s&appid=%s"%(city,API_key)
        r2 = requests.get(url2)
        d[city] = r2.json()['coord']
    return d


cities = ['Bangalore','Mumbai','New York','Dubai','London','Mexico']

try:
    city_coord = pickle.load(open('city_coord.pkl','rb'))

except:
    city_coord = get_coord(cities)
    a_file = open('city_coord.pkl','wb')
    pickle.dump(city_coord, a_file)
    a_file.close()

try:
    df_one_call = pd.read_csv('one_call.csv')
except:
    df_one_call = pd.DataFrame(columns =['city','dt','temp_c','temp_f','pressure','humidity','wind_deg','wind_speed','wind_gust'])

def one_call(lat,lon):
    url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&exclude=hourly,minutely,daily&appid=%s"%(lat,lon,API_key)
    r = requests.get(url).json()
    current = r['current']
    required_keys = ['dt','pressure','humidity','wind_deg','wind_gust','wind_speed']
    d = {k:v for k,v in current.items() if k in required_keys}
    d['dt'] = datetime.fromtimestamp(d['dt'])
    d['temp_c'] = current['temp']-273
    d['temp_f'] = (current['temp']-273)*9/5 + 32
    return d

def extract_data():
    new_df = pd.DataFrame(columns =['city','dt','temp_c','temp_f','pressure','humidity','wind_deg','wind_speed','wind_gust'])
    for city in city_coord:
        d = one_call(city_coord[city]['lat'], city_coord[city]['lon'])
        d['city']=city
        new_df = new_df.append(d, ignore_index=True)
    return new_df

df_one_call = df_one_call.append( extract_data(),ignore_index=True )
df_one_call.to_csv('one_call.csv',index=False)

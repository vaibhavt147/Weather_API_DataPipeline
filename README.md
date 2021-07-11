# Weather_Data_API
This project tries to use "One Call API" &amp; "Current Weather API" from https://openweathermap.org/ to get weather data for 6 different cities

Weather metrices:
1. Wind degree, Wind Speed, Wind Gust
2. Temperature
3. Humidity
4. Pressure

Cities:
1. Dubai
2. Mumbai
3. Bangalore
4. London
5. New York
6. Mexico

Goals:
1. One call API - Get all weather metrices for each city only once a day
2. Current Weather - Call the API after every five minutes and extract the data for a whole day for each city

Data Flow Pipeline Steps:
1. Create empty Dataframe using pandas module in python. Next time when the script is executed again, the same file will be used to append new data
2. Use request module from python to get data aquried by calling api in json format
3. Extract required data from json file and convert it into dictionary
4. Append the dictionary into Daframe above
5. Repeat the same thing using for loop for each city

For Current Weather API:
Note - Use the above pipeline and use schedular from python to run the entire process after every 5 mins

How to Run?
* At the start of each day, run every_day.sh. You need to enter API key through terminal itself.

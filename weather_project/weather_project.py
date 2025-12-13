# -*- coding: utf-8 -*-
"""
Created on Tue Sep 23 22:03:45 2025

@author: fatemeh hosseininasab
"""
#this project is about getting weather information from openweather.com and using its api key for current weather for any country
#and then connect and saving to postsql database
import requests
import math
from datetime import datetime
import psycopg2

get_city_name=input("enter the city you want to see the current weather information:\n")
city=get_city_name.capitalize()
app_id="8e9b3bf909514a2eab73f0d39c151181"
URL=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=8e9b3bf909514a2eab73f0d39c151181"
r=requests.get(url=URL)
data=r.json()

temp_k=data['main']['temp']
temp_k_min=data['main']['temp_min']
temp_k_max=data['main']['temp_max']
temp_feels_k=data['main']['feels_like']
humidity=data['main']['humidity']
time=data['dt']
wind_speed=round(data['wind']['speed'],2)

def kelvin_to_celsius(k):
    return round(k - 273.15, 3)

def kelvin_to_fahrenheit(k):
    return round((k - 273.15) * 9/5 + 32, 3)

temp_c=round(kelvin_to_celsius(temp_k),3)
temp_f=round(kelvin_to_fahrenheit(temp_k),3)

temp_c_min=round(kelvin_to_celsius(temp_k_min),3)
temp_f_min=round(kelvin_to_fahrenheit(temp_k_min),3)

temp_c_max=round(kelvin_to_celsius(temp_k_max),3)
temp_f_max=round(kelvin_to_fahrenheit(temp_k_max),3)

temp_feels_c=round(kelvin_to_celsius(temp_feels_k),3)
temp_feels_f=round(kelvin_to_fahrenheit(temp_feels_k),3)

date_time=datetime.fromtimestamp(time)

print("Current Temperature:")
print(f"{temp_k} K | {temp_c} °C | {temp_f} °F")
print("-------------------------------------------------------------")
print("Minimum Temperature:")
print(f"{temp_k_min} K | {temp_c_min} °C | {temp_f_min} °F")
print("-------------------------------------------------------------")
print("Maximum Temperature:")
print(f"{temp_k_max} K | {temp_c_max} °C | {temp_f_max} °F")
print("-------------------------------------------------------------")
print("Feeling Temperature:")
print(f"{temp_feels_k} K | {temp_feels_c} °C | {temp_feels_f} °F")
print("-------------------------------------------------------------")
print("Humidity:")
print(f"{humidity}%")
print("-------------------------------------------------------------")
print("Wind Speed:")
print(f"{wind_speed} m/s")
print("-------------------------------------------------------------")
print("datetime:")
print(date_time.strftime("%A, %d %B %Y at %I:%M:%S %p"))

conn=psycopg2.connect(dbname="weather_project",user="postgres",password="asal1234@",host="localhost",port="5432")

cur = conn.cursor()
cur.execute("""
    INSERT INTO weather_data (
        timestamp,temp_k,temp_c,temp_f,temp_min_k,temp_min_c,temp_min_f,
        temp_max_k,temp_max_c,temp_max_f,temp_feels_k,temp_feels_c,temp_feels_f,
        humidity, wind_speed,name_of_city) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"""
    ,(date_time,temp_k,temp_c,temp_f,temp_k_min,temp_c_min,temp_f_min,
    temp_k_max,temp_c_max,temp_f_max,temp_feels_k,temp_feels_c,temp_feels_f,
    humidity,wind_speed,city))

conn.commit()
cur.close()
conn.close()

print("Weather data saved to database.")
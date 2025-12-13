# -*- coding: utf-8 -*-
"""
Created on Tue Sep 23 23:23:12 2025

@author: fatemeh
"""
from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
engine = create_engine('postgresql+psycopg2://postgres:asal1234%40@localhost:5432/weather_project')
city=input("enter the city name you want to see its information(you will see the information in celcius): ").capitalize()
query = f"""
SELECT name_of_city,timestamp,temp_c
FROM weather_data
WHERE name_of_city='{city}'
ORDER BY timestamp;
"""
df=pd.read_sql(query,engine)
if df.empty:
    print("No data found for",city)
else:
    plt.figure(figsize=(10, 5))
    plt.plot(df['timestamp'],df['temp_c'], marker='o', color='green',linewidth=2)
    plt.title("temperature Trend in")
    plt.xlabel("date")
    plt.ylabel("temperature(°C)")
    plt.tight_layout()
    plt.show()

query1=f"""
SELECT name_of_city,timestamp,temp_min_c
FROM weather_data
WHERE name_of_city='{city}'
ORDER BY timestamp;
"""
df=pd.read_sql(query1,engine)
if df.empty:
    print("No data found for",city)
else:
    plt.figure(figsize=(10, 5))
    plt.plot(df['timestamp'],df['temp_min_c'], marker='o', color='blue',linewidth=2)
    plt.title("temperature Trend in")
    plt.xlabel("date")
    plt.ylabel("minimum temperature(°C)")
    plt.tight_layout()
    plt.show()
    
query2=f"""
SELECT name_of_city,timestamp,temp_max_c
FROM weather_data
WHERE name_of_city='{city}'
ORDER BY timestamp;
"""
df=pd.read_sql(query2,engine)
if df.empty:
    print("No data found for",city)
else:
    plt.figure(figsize=(10, 5))
    plt.plot(df['timestamp'],df['temp_max_c'], marker='o', color='red',linewidth=2)
    plt.title("temperature Trend in")
    plt.xlabel("date")
    plt.ylabel("maximum temperature(°C)")
    plt.tight_layout()
    plt.show()
    
query3=f"""
SELECT name_of_city,timestamp,temp_feels_c
FROM weather_data
WHERE name_of_city='{city}'
ORDER BY timestamp;
"""
df=pd.read_sql(query3,engine)
if df.empty:
    print("No data found for",city)
else:
    plt.figure(figsize=(10, 5))
    plt.plot(df['timestamp'],df['temp_feels_c'], marker='o', color='pink',linewidth=2)
    plt.title("temperature Trend in")
    plt.xlabel("date")
    plt.ylabel("feeling temperature(°C)")
    plt.tight_layout()
    plt.show()
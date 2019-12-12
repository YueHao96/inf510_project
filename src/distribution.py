import folium
import pandas as pd
import sqlite3
from folium import plugins
from folium.plugins import HeatMap
import numpy as np
import webbrowser
import os

def house_distribution(sql1,sql2):

    LA_COORDINATES = (34.05, -118.24)

    conn = sqlite3.connect(r'..\data\final_project.db')
    cur = conn.cursor()

    value_data = pd.read_sql(sql1, conn)
    value=np.array(value_data["value"][0:len(value_data)])
    lat = np.array(value_data["latitude"][0:len(value_data)])
    lon = np.array(value_data["longitude"][0:len(value_data)])

    value_map= folium.Map(location=LA_COORDINATES,zoom_start=10)
    for i in range(50):
        folium.Marker(location=[lat[i],lon[i]],popup=f"Value:${value[i]}",icon=folium.Icon(color="red", icon='home')).add_to(value_map)

    value_data = pd.read_sql(sql2, conn)
    value=np.array(value_data["value"][0:len(value_data)])
    lat = np.array(value_data["latitude"][0:len(value_data)])
    lon = np.array(value_data["longitude"][0:len(value_data)])
    for i in range(50):
        folium.Marker(location=[lat[i],lon[i]],popup=f"Value:${value[i]}",icon=folium.Icon(color="blue", icon='home')).add_to(value_map)

    path=os.getcwd()
    file_path = f"{path}\spatial distribution.html"
    value_map.save(file_path)
    webbrowser.open(file_path)
    conn.close()

def run_distribution():
    sql1="select value,latitude,longitude,zip_code from \
    Value join Zipcode on Value.zipcode_id==Zipcode.id\
    where value!=-1 order by value DESC limit 50"
    sql2="select value,latitude,longitude,zip_code from \
    Value join Zipcode on Value.zipcode_id==Zipcode.id \
    where value!=-1 order by value ASC limit 50"
    house_distribution(sql1,sql2)

if __name__=="__main__":
    run_distribution()

#!/usr/bin/env python
# coding: utf-8
import csv
import requests
import json
import re
from bs4 import BeautifulSoup
#import sqlite3
import sql
zws_id="X1-ZWz1hgvbaoqsy3_3tnpx"
key="3eeaa7fc9f4a7ea97878520335caf746"


def get_cities():
    """The function is used to scrape city names in LA county from wikipedia.

    Returns:
        cities:A list of cities.

    """
    la_county=[]
    cities=[]

    try:
        request=requests.get("https://en.wikipedia.org/wiki/List_of_cities_in_Los_Angeles_County,_California")
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(e)
    else:
        soup = BeautifulSoup(request.content, 'lxml')
        main_table = soup.find('table')
        main_body = main_table.find('tbody')
        info = soup.find_all('tr')
        for city in info:
            if (len(city.find_all('td')) > 0):
                name1 = city.find('a').text.split()
                split_city="".join(name1).lower()
                la_county.append(split_city)
                name2 = city.find('a').text
                cities.append(name2.lower())
    cities=cities[:-6]
    return(cities)


def get_value(cities):
    """Use city name to contrust url in order to get housing value, longitude and latitude.
    Store data into csv file.
    Args:
        cities:A list of city names.

    Raises:
        HTTPError: An error occurred when doing GET request.

    Returns:
        value_list: A list.Including zipcode of the place and its longitude and latitude value.

    """
    value_list=[]
    for city in cities:
        url=(f"http://www.zillow.com/webservice/GetRegionChildren.htm?zws-id={zws_id}&state=ca&city={city}&childtype=zipcode")
        try:
            response=requests.get(url)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(e)
        else:
            soup = BeautifulSoup(response.content, 'xml')
        try:
            info = soup.find("list")
            contents=info.find_all("region")
        except:
            print(f"{url} does not work")
        else:

            if len(contents)!=0:
                for content in contents:
                    if content.find("name")==None:
                        zip_code="-1"
                    else:
                        zip_code=content.find("name").text

                    if content.find("zindex")==None:
                        value="-1"
                    else:
                        value=content.find("zindex").text

                    if content.find("latitude")==None:
                        lat="N/A"
                    else:
                        lat=content.find("latitude").text

                    if content.find("longitude")==None:
                        lon="N/A"
                    else:
                        lon=content.find("longitude").text

                    value_list.append((value,zip_code,lat,lon))
    try:
        f= open('housing value.csv','w',encoding='utf-8')

    except IOError as err:
        print(f"File error: {err}.")
    else:
        f.write("{},{},{},{}\n".format("housing value","zip code","latitude","longitude"))
        for value,zip_code,lat,lon in value_list:
            f.write("{},{},{},{}\n".format(value,zip_code,lat,lon))
        f.close()

    return value_list
def get_walk_score(zip_code,lat,lon):
    """Store walk score data into vsc file.

    Args:
        zip_code: A 5 digit unique zip code.
        lat: Latitude of the recorded place.
        lon: Longitude of the recorded place.

    Raises:
        HTTPError: Error occurred when doing GET request.

    Returns:
        A tuple.With area zipcode and its walk score.

    """

    walk_url=(f"http://api.walkscore.com/score?format=json&address=%20CA&lat={lat}&lon={lon}&wsapikey={key}")
    try:
        response=requests.get(walk_url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(e)
    else:
        content=response.json()
        #print(content)
        try:
            walk_score=content["walkscore"]
        except:
            walk_score=-1

        #walk_score_list.append((city,zip_code,walk_score))
    return (zip_code,walk_score)

def store_walk_score():
    """Store walk score data into database.

    Args:
        walk_score_list: A list contains area zipcode and the walk score.

    """
    try:
        with open("walk score.csv","r") as csvfile:
            file=csvfile.readlines()
    except:
        print("error")
    else:
        info_list=[]
        for row in file:
            row=row.strip()
            row=row.split(",")
            info_list.append(row)

    sql.create_walk_score_table()

    for r in range(1,len(info_list)):
        walk_score=info_list[r][1]
        walk_score=float(walk_score)
        zip_code=info_list[r][0]
        zip_code=str(zip_code)
        zipcode_id=sql.get_zipcode_id(zip_code)

        sql.insert_walk_score(walk_score,zipcode_id)


def store_house_value():
    """Store hosing value data into database.

    Args:
        value_list: Return value from get_value() function.A list with area zipcode, hosing value and coordinates.

    """
    try:
        with open("housing value.csv","r") as csvfile:
            file=csvfile.readlines()
    except:
        print("error")
    else:
        info_list=[]
        for row in file:
            row=row.strip()
            row=row.split(",")
            info_list.append(row)

    sql.create_housing_value_talble()

    for r in range(1,len(info_list)):
        value=info_list[r][0]
        if value!="-1":
            value=int(value)
        else:
            value=-1
        latitude=info_list[r][2]
        latitude=float(latitude)
        longitude=info_list[r][3]
        longitude=float(longitude)
        zip_code=info_list[r][1]
        zip_code=str(zip_code)

        zipcode_id=sql.get_zipcode_id(zip_code)

        sql.insert_housing_value(value,latitude,longitude,zipcode_id)

def run_housing():
    """Run functions.
    Firsltly, scrape city names from Wikipedia.
    Secondly,using city names as API parameter to get housing value, longitude and latitude.
    Thirdly, using longitude and latitude as API parameter to get walk score value.
    Lastly, storing housing value data and walk score data into database.
    """
    cities=get_cities()
    value_list = get_value(cities)
    walk_score_list = []
    for i in range (len(set(value_list))):
        (zip_code,lat,lon)=value_list[i][1:]

        if (zip_code,lat,lon)!=("N/A","N/A","N/A","N/A"):
            walk_score_list.append(
                    get_walk_score(zip_code,lat,lon))
        else:
            walk_score_list.append((zip_code,-1))
    try:
        f= open('walk score.csv','w',encoding='utf-8')

    except IOError as err:
        print(f"File error: {err}.")
    else:
        f.write("{},{}\n".format("zip code","walk score"))
        for zip_code,walk_score in walk_score_list:
            f.write("{},{}\n".format(zip_code,walk_score))
        f.close()

    store_walk_score()
    store_house_value()

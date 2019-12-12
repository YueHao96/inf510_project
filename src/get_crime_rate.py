#!/usr/bin/env python
# coding: utf-8

import requests
import re
import csv
from bs4 import BeautifulSoup

def simple_get():
    """Using zipcode as parameter to get HTTP response.

    Raises:
        HTTPError: An error occurred when accesing GET request.

    Returns:
        crime_info: A list of tuples. With zipcode and HTTP response.

    """
    crime_info=[]
    zip_code=90001

    while zip_code<93599:
        for zip_code in range(zip_code,zip_code+100):
            try:
                request = requests.get(f'https://www.bestplaces.net/crime/zip-code/california/florence-graham/{zip_code}')
                request.raise_for_status()
            except requests.exceptions.HTTPError as e:
                print(e)
                print(f"Failed at {zip_code}.")
                break
            else:
                crime_info.append((request,zip_code))
        print(f"Got 100 recordes from {zip_code-99} to {zip_code} successfully.")
        zip_code+=1
    return crime_info

def get_crime_rate(crime_info):

    """Scrape crime rates in Los Angeles County by zip code.

    Aargs:
        response:Responses of get requests.
        zip_code:5 digits zip codes between 90001 to 93599

    Raises:
        value error:If the crime rate is none, record it -1.
        IOError:An error occurred when accessing the csv file.
    """
    crime_rate_list=[]
    for i in range (len(crime_info)):
        response=crime_info[i][0]
        zip_code=crime_info[i][1]

        soup = BeautifulSoup(response.content, 'lxml')
        info = soup.find_all('h5')[1].text.split()

        try:
            crime_rate=info[-6][:-1]
            crime_rate=float(crime_rate)
        except:
            crime_rate=-1

        crime_rate_list.append((zip_code, crime_rate))

    try:
        f= open(r'..\data\crime rate.csv','w',encoding='utf-8')

    except IOError as err:
        print(f"File error: {err}.")
    else:
        f.write("{},{}\n".format("zip code","crime rate"))
        for zip_code,crime_rate in crime_rate_list:
            f.write("{},{}\n".format(zip_code,crime_rate))
        f.close()

def run_get_crime_rate():
    """Run all the functions.
    """
    crime_info=simple_get()
    get_crime_rate(crime_info)

if __name__=="__main__":
    run_get_crime_rate()

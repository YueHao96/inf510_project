#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
import requests
import re
import csv
#import sqlite3
import sql

def store_crime_rate():

    """Read the downloaded crime rate data file. Store the data in dictionary.

    Raises:
        IOError: An error occurred accessing the crime rate.csv file.
    """

    try:
        f=open("crime rate.csv","r")
    except IOError as err:
        print(f"File error: {err}.")
    else:
        file=csv.reader(f)
        keys=next(file)
        data={}
        for key in keys:
            data[key]=[]
        for row in file:
            for i,entry in enumerate(row):
                data[keys[i]].append(entry)
        f.close()

    sql.create_crime_rate_table()
    for r in range(0, len(data["crime rate"])):
        crime_rate=data["crime rate"][r]
        crime_rate=float(crime_rate)
        zip_code=data["zip code"][r]
        zip_code=str(zip_code)

        zipcode_id=sql.get_zipcode_id(zip_code)
        sql.insert_crime_rate(crime_rate,zipcode_id)

    #sql.close_database()
#store_crime_rate()

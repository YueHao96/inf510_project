#!/usr/bin/env python
# coding: utf-8

import re
import csv
import sqlite3
import sql

def store_urban_data():
    """Read urbanicity data from local csv file.Store the data into database.

    Raises:
        IOError: An error occurred accessing the crime rate.csv file.

    """
    try:
        f=open(r"..\data\zip_urban_rural_ca.csv","r")
    except IOError as err:
        print(f"File error: {err}.")
    else:
        file=csv.reader(f)
        keys=next(file)
        urban_dict={}
        for key in keys:
            urban_dict[key]=[]
        for row in file:
            for i,entry in enumerate(row):
                urban_dict[keys[i]].append(entry)
        f.close()

        length=len(urban_dict['zip code'])
        sql.create_urban_table()
        for r in range(0, length):
            urban_units=urban_dict["housing units urban"][r]
            urban_units=str(urban_units)
            rural_units=urban_dict["housing units rural"][r]
            rural_units=str(rural_units)
            density=float(urban_dict["population density"][r])
            zip_code=urban_dict["zip code"][r]
            zip_code=str(zip_code)

            zipcode_id=sql.get_zipcode_id(zip_code)
            sql.insert_urbanicity(urban_units,rural_units,density,zipcode_id)

if __name__=="__main__":
    store_urban_data()

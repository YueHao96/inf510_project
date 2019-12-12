#!/usr/bin/env python
# coding: utf-8

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import sql
import csv

def simple_get():
    """Attempts to get the medeian house hold income by making an GET request.

    Raises:
        HTTPError:If the GET request fails, return the exception information.

    Returns:
        The resoponse from GET requests.
     """
    try:
        request = requests.get("http://www.laalmanac.com/employment/em12c.php")
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(e)
    else:
        return request

def get_income(response):
    """Parse the resource and get the incme data.Store data into csv file.

    Args:
        response: Returned from simple_get() fuction. A HTTP response.

    Returns:
        income_dict:A dictionary.Stores income data by zipcode.

    """
    income_list=[]

    soup = BeautifulSoup(response.content, 'lxml')
    main_body = soup.find('table')
    main_body = main_body.find('tbody')

    for row in main_body.find_all('tr'):
        if (len(row.find_all('td')) > 0):
            zip_code = row.find_all('td')[0].text
            income=row.find_all("td")[2].text
            income=income[1:].split(",")
            income=int("".join(income))
            income_list.append((zip_code, income))

    try:
        f= open(r'..\data\income.csv','w',encoding='utf-8')

    except IOError as err:
        print(f"File error: {err}.")
    else:
        f.write("{},{}\n".format("zip code","income"))
        for zip_code,income in income_list:
            f.write("{},{}\n".format(zip_code,income))
        f.close()

def store_income():
    """Store income data into database.

    """
    sql.create_income_table()

    try:
        f=open(r"..\data\income.csv","r")
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

        for r in range(0, len(data["income"])):
            income=data["income"][r]
            income=int(income)
            zip_code=data["zip code"][r]
            zip_code=str(zip_code)

            zipcode_id=sql.get_zipcode_id(zip_code)
            sql.insert_income(income,zipcode_id)

        f.close()

def run_income():
    """Run all the functions.
    """
    response=simple_get()
    income_dict=get_income(response)
    store_income()

if __name__=="__main__":
    run_income()

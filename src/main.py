#!/usr/bin/env python
# coding: utf-8

import zipcode
import community
import crime_rate
import income
import urbanicity
import housing_value_n_walkscore
import argparse
import sql

parser = argparse.ArgumentParser()
parser.add_argument("source",help="choose where to obtain the data from, remote or local")

if __name__=="__main__":
    args = parser.parse_args()
    source = args.source
    sql.create_zipcode_table()
    sql.insert_zipcode()

    if source =="remote":
        community.run_community()
        income.run_income()
        housing_value_n_walkscore.run_housing()

    elif source == "local":
        urbanicity.store_urban_data()
        crime_rate.store_crime_rate()
        income.store_income()
        community.store_community()
        housing_value_n_walkscore.store_walk_score()
        housing_value_n_walkscore.store_house_value()

    sql.close_database()

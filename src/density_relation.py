import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import os

def density_relation():
    conn=sqlite3.connect(r"..\data\final_project.db")
    cur=conn.cursor()

    sql='SELECT walk_score,income,density,crime_rate FROM \
        Income join Walk_score Join Crime_rate Join Urban on \
        Income.zipcode_id=Urban.zipcode_id and \
        Walk_score.zipcode_id=Urban.zipcode_id and \
        Crime_rate.zipcode_id=Urban.zipcode_id \
        where crime_rate!=-1 '
    cur.execute(sql)
    info_list=cur.fetchall()

    scores = []
    incomes=[]
    popu_density=[]
    crime_rates=[]
    for info in info_list:
        score=info[0]
        scores.append(score)
        income=info[1]
        incomes.append(income/100)
        density=info[2]
        popu_density.append(density)
        crime_rate=info[3]
        crime_rates.append(crime_rate)

    plt.figure(num=3, figsize=(15, 15))
    cm="summer_r"

    sc=plt.scatter(popu_density,scores
                    ,s=incomes
                    ,c=crime_rates
                    ,vmin=0, vmax=70,cmap=cm
                    ,label='income'
                    ,alpha=0.5)

    plt.title("Correlation between pupulation density,income level,crime rates and walk score")
    plt.xlabel("Population Density")
    plt.ylabel("Walk Score")

    cb=plt.colorbar()
    cb.set_label("Crime rate")
    plt.legend()
    plt.savefig(f"Density and other factors.png", dpi=80,bbox_inches='tight')
    plt.show()

    conn.close()

def run_density_relation():
    density_relation()

if __name__=="__main__":
    run_density_relation()

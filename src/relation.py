import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import os

def correlation_matrix():
    conn = sqlite3.connect('final_project.db')
    cur = conn.cursor()
    sql="SELECT value,walk_score,density,crime_rate,income \
        FROM Walk_score join Value Join Crime_rate Join Urban join Income on \
        Walk_score.zipcode_id=Value.zipcode_id and \
        Value.zipcode_id=Crime_rate.zipcode_id \
        and Value.zipcode_id=Urban.zipcode_id and \
        Value.zipcode_id=Income.zipcode_id \
        where value!=-1"
    data = pd.read_sql(sql, conn)

    plt.figure(figsize=(6,5),dpi=100)
    columns=["Housing value","Walk score","Populaiton density","Crime rate","Household median income"]
    sns.heatmap(data.corr()
                ,xticklabels=columns
                ,yticklabels=columns
                ,cmap="RdYlGn"
                ,center=0
                ,annot=True
               )

    plt.xticks(rotation=45,horizontalalignment="right")
    plt.savefig("correlation matrix.png", bbox_inches='tight')
    plt.show()

def income_correlation(sql,cm,name):
    conn=sqlite3.connect("final_project.db")
    cur=conn.cursor()
    cur.execute(sql)
    #cur.execute('SELECT value,income,density,crime_rate FROM Income join Value Join Crime_rate Join Urban on Income.zipcode_id=Value.zipcode_id and Value.zipcode_id=Crime_rate.zipcode_id and Value.zipcode_id=Urban.zipcode_id where value!=-1 and crime_rate!=-1 ORDER BY value ASC limit 30')
    info_list=cur.fetchall()
    communities=[]
    for info in info_list:
        value=info[0]
        cur.execute('SELECT zipcode_id FROM Value WHERE value=?', (value,))
        zipcode_id=cur.fetchone()
        cur.execute('SELECT community FROM Community WHERE zipcode_id=?', zipcode_id)
        community=cur.fetchone()[0]
        i=str(info_list.index(info)+1)
        community=i+"."+community
        communities.append(community)
    values = []
    incomes=[]
    popu_density=[]
    crime_rates=[]
    for info in info_list:
        value=info[0]
        values.append(value)
        income=info[1]
        incomes.append(income)
        density=info[2]
        popu_density.append(density/10)
        crime_rate=info[3]
        crime_rates.append(crime_rate)
    #画图
    plt.figure(num=3, figsize=(15, 15))

    sc=plt.scatter(incomes,values
                    ,s=popu_density
                    ,c=crime_rates
                    ,vmin=0,vmax=70,cmap=cm
                    ,label='density'
                    ,alpha=0.5)
    if name!="All data":
        for i in range(len(communities)):
            plt.text(incomes[i],values[i]
                    ,s=communities[i]
                    ,horizontalalignment="center")

    plt.title("Correlation between income,hosing value and other factors")
    plt.xlabel("Household median income(USD)")
    plt.ylabel("Housing value(USD,estimated by Zillow")

    cb=plt.colorbar()
    cb.set_label("Crime rate")
    plt.legend()
    plt.savefig(f"{name}.png", dpi=100,bbox_inches='tight')
    plt.show()

    conn.close()
def density_correlation():
    conn=sqlite3.connect("final_project.db")
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
def run_relation():
    correlation_matrix()
    sqls=['SELECT value,income,density,crime_rate \
         FROM Value Join Crime_rate Join Urban join Income on \
         Value.zipcode_id=Crime_rate.zipcode_id \
         and Value.zipcode_id=Urban.zipcode_id and \
         Value.zipcode_id=Income.zipcode_id\
         where value!=-1',
         'SELECT value,income,density,crime_rate FROM \
         Income join Value Join Crime_rate Join Urban on \
         Income.zipcode_id=Value.zipcode_id and \
         Value.zipcode_id=Crime_rate.zipcode_id and \
         Value.zipcode_id=Urban.zipcode_id \
         where value!=-1 and crime_rate!=-1 ORDER BY value ASC limit 20',
         'SELECT value,income,density,crime_rate FROM \
         Income join Value Join Crime_rate Join Urban on \
         Income.zipcode_id=Value.zipcode_id and \
         Value.zipcode_id=Crime_rate.zipcode_id and \
         Value.zipcode_id=Urban.zipcode_id \
         where value!=-1 and crime_rate!=-1 ORDER BY value DESC limit 20']
    cms=["Reds","winter_r","autumn_r"]
    names=["All data","lowest20","highest20"]
    for i in range(3):
        income_correlation(sqls[i],cms[i],names[i])

    density_correlation()

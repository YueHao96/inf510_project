import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import os

def correlation_matrix():
    conn = sqlite3.connect(r'..\data\final_project.db')
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
    sns.heatmap(data.corr(),xticklabels=columns,yticklabels=columns,cmap="RdYlGn",center=0,annot=True)

    plt.xticks(rotation=45,horizontalalignment="right")
    path=os.getcwd()
    #plt.savefig(f"{path}\correlation matrix.png", bbox_inches='tight')
    plt.show()

def run_correlation_matrix():
    correlation_matrix()

if __name__=="__main__":
    run_correlation_matrix()


import csv
from bs4 import BeautifulSoup
import requests
import sql

def simple_get():
    """Attempts to get the community name each zip code stands for by making an GET request.

    Raises:
        HTTPError: An error occurred when getting requests.
    """
    try:
        request = requests.get("http://www.laalmanac.com/communications/cm02_communities.php")
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(e)
    else:
        return(request)

def get_name(response):
    """Get commnity names by zip code and store it into csv file.

    Args:
        response: A response from GET request.

    Returns:
        name_dict: A dictionaty with community names and accoring zip codes.

    """
    community_list=[]

    soup = BeautifulSoup(response.content, 'lxml')
    main_body = soup.find('table')
    main_body = main_body.find('tbody')

    for row in main_body.find_all('tr'):
        if (len(row.find_all('td')) > 0):
            community = row.find_all('td')[0].text
            zip_codes = row.find_all('td')[1].text.split(", ")

            for zip_code in zip_codes:
                if len(zip_code)!=5:
                    community_list.append((zip_code[:5], community))
                else:
                    community_list.append((zip_code, community))

    try:
        f= open('community.csv','w',encoding='utf-8')

    except IOError as err:
        print(f"File error: {err}.")
    else:
        f.write("{},{}\n".format("zip code","community name"))
        for zip_code,community in community_list:
            f.write("{},{}\n".format(zip_code,community))
        f.close()

def store_community():
    """Store the community data into database.

    """

    try:
        with open("community.csv","r") as csvfile:
            file=csvfile.readlines()
    except:
        print("error")
    else:
        info_list=[]
        for row in file:
            row=row.strip()
            row=row.split(",")
            info_list.append(row)

    sql.create_community_table()
    for r in range(1,len(info_list)):
        name=info_list[r][1]
        name=str(name)
        zip_code=info_list[r][0]
        zip_code=str(zip_code)

        zipcode_id=sql.get_zipcode_id(zip_code)
        sql.insert_community(zipcode_id,name)

def run_community():
    """Run the three funcions.
    """
    response=simple_get()
    name_dict=get_name(response)
    store_community()

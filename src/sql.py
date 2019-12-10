import sqlite3

conn=sqlite3.connect("final_project.db")
cur=conn.cursor()


def create_zipcode_table():
    """Create zipcode table.
    """
    cur.execute('DROP TABLE IF EXISTS Zipcode ')
    cur.execute("CREATE TABLE Zipcode (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,zip_code TEXT)")

def insert_zipcode():
    for i in range(90001,93600):
        zip_code=i
        cur.execute('INSERT INTO Zipcode (zip_code) VALUES (?)', (zip_code,))
        conn.commit()

def get_zipcode_id(zip_code):
    cur.execute("SELECT id FROM Zipcode WHERE zip_code=?",(zip_code,))
    zipcode_id=int(cur.fetchone()[0])
    return zipcode_id

def create_urban_table():
    cur.execute('DROP TABLE IF EXISTS Urban ')

    cur.execute("""CREATE TABLE Urban (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            urban_units INTEGER,
            rural_units INTEGER,
            density REAL,
            zipcode_id INTEGER)""")

def insert_urbanicity(urban_units,rural_units,density,zipcode_id):

    cur.execute('SELECT * FROM Urban WHERE (urban_units=? and rural_units=? and density=? and zipcode_id=?)', (urban_units,rural_units,density,zipcode_id,))
    entry = cur.fetchone()

    if entry is None:
        cur.execute('INSERT INTO Urban (urban_units,rural_units,density,zipcode_id) VALUES (?,?,?,?)', (urban_units,rural_units,density,zipcode_id,))
        conn.commit()
        print ('New urbanicity data inserted.')
    else:
        print ('Entry found')

def create_crime_rate_table():
    cur.execute('DROP TABLE IF EXISTS Crime_rate ')

    cur.execute("""CREATE TABLE Crime_rate (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            crime_rate FLOAT,
            zipcode_id INTEGER)""")

def insert_crime_rate(crime_rate,zipcode_id):
    cur.execute('SELECT * FROM Crime_rate WHERE (crime_rate=? and zipcode_id=?)', (crime_rate,zipcode_id,))
    entry = cur.fetchone()

    if entry is None:
        cur.execute('INSERT INTO Crime_rate (crime_rate,zipcode_id) VALUES (?,?)', (crime_rate,zipcode_id,))
        conn.commit()
        print ('New crime rate data inserted.')
    else:
        print ('Entry found')

def create_income_table():
    cur.execute('DROP TABLE IF EXISTS Income ')

    cur.execute("CREATE TABLE Income (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,income INTEGER,zipcode_id INTEGER)")

def insert_income(income,zipcode_id):
    cur.execute('SELECT * FROM Income WHERE (income=?)', (income,))
    entry = cur.fetchone()

    if entry is None:
        cur.execute('INSERT INTO Income (income,zipcode_id) VALUES (?,?)', (income,zipcode_id,))
        conn.commit()
        print ('New income data inserted.')
    else:
        print ('Entry found')

def create_community_table():
    cur.execute('DROP TABLE IF EXISTS Community ')
    cur.execute("CREATE TABLE Community (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,community TEXT,zipcode_id INTEGER)")

def insert_community(zipcode_id,name):

    cur.execute('SELECT * FROM Community WHERE (zipcode_id=? and community=?)', (zipcode_id,name,))
    entry = cur.fetchone()

    if entry is None:
        cur.execute('INSERT INTO Community (zipcode_id,community) VALUES (?,?)', (zipcode_id,name,))
        conn.commit()
        print ('New community name inserted.')
    else:
        print ('Entry found')

def create_walk_score_table():
    cur.execute('DROP TABLE IF EXISTS Walk_score ')
    cur.execute("CREATE TABLE Walk_score (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, walk_score INTEGER,zipcode_id INTEGER)")

def insert_walk_score( walk_score,zipcode_id):
    cur.execute('SELECT * FROM Walk_score WHERE (walk_score=? and zipcode_id=?)', ( walk_score,zipcode_id,))
    entry = cur.fetchone()

    if entry is None:
        cur.execute('INSERT INTO Walk_score (walk_score,zipcode_id) VALUES (?,?)', (walk_score,zipcode_id,))
        conn.commit()
        print ('New walk score data inseted.')
    else:
        print ('Entry found')


def create_housing_value_talble():
    cur.execute('DROP TABLE IF EXISTS Value ')

    cur.execute("CREATE TABLE Value (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, value INTEGER,latitude REAL,longitude REAL,zipcode_id INTEGER)")

def insert_housing_value(value,latitude,longitude,zipcode_id):
    cur.execute('SELECT * FROM Value WHERE (value=? and latitude=? and longitude=? and zipcode_id=?)', (value,latitude,longitude,zipcode_id,))
    entry = cur.fetchone()

    if entry is None:
        cur.execute('INSERT INTO Value (value,latitude,longitude,zipcode_id) VALUES (?,?,?,?)', (value,latitude,longitude,zipcode_id,))
        conn.commit()
        print ('New value data inserted.')
    else:
        print ('Entry found')


def close_database():
    print("Database is closed")
    conn.close()

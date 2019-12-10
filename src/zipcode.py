import sqlite3

def create_zipcode_table():
    """Create zipcode table.
    """

    conn=sqlite3.connect("final_project.db")
    cur=conn.cursor()
    cur.execute('DROP TABLE IF EXISTS Zipcode ')

    cur.execute("CREATE TABLE Zipcode (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,zip_code TEXT)")
    for i in range(90001,93600):
        zip_code=i
        cur.execute('INSERT OR IGNORE INTO Zipcode (zip_code) VALUES (?)', (zip_code,))
        """cur.execute('SELECT * FROM Zipcode WHERE (zip_code=?)', (zip_code,))
        entry = cur.fetchone()

        if entry is None:
            cur.execute('INSERT INTO Zipcode (zip_code) VALUES (?)', (zip_code,))
            conn.commit()
            print ('New zip code inserted')
        else:
            print ('Entry found')"""

    conn.close()

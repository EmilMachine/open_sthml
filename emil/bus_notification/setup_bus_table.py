import sqlite3

### SETup database
conn = sqlite3.connect('bus_raw_1.db')
c = conn.cursor()
c.execute('DROP TABLE IF EXISTS busraw;')
c.execute('''--
    CREATE TABLE busraw
    (request_time DATETIME, name TEXT, siteid INT,raw TEXT);
    ''')
conn.commit()
conn.close()
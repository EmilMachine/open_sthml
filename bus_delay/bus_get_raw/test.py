import urllib2
import time
import sqlite3
### SIMPLE READ
link = 'http://data.stockholm.se/set/Befolkning/Flyttningar/?apikey=S8O2CD27J2K4EE55CED0L0J5H81A1902'

f = urllib2.urlopen(link)
raw = f.read()

file_in = 'tmp_raw.txt'
with open(file_in,'r') as f:
    raw = f.read()

    print(raw)


call_time = time.strftime("%Y-%m-%M %H:%M:%S", time.localtime())
conn = sqlite3.connect('bus_raw_1.db')
c = conn.cursor()

c.execute('DROP TABLE IF EXISTS test;')
c.execute('''--
    CREATE TABLE test
    (request_time DATETIME, name TEXT, siteid INT,raw TEXT);
    ''')

qq = ''' --
    INSERT INTO test
    (request_time, name, siteid, raw)
    VALUES ('%s', '%s', %i, '%s');
    ''' % (call_time,'Slussen',42,raw)

c.execute(qq)

conn.commit()
conn.close()
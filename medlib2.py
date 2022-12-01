import sqlite3

conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Counts')

cur.execute('''
CREATE TABLE Counts (email TEXT, count INTEGER)''')

fname = input('Enter file name: ')
if (len(fname) < 1): fname = 'mbox.txt'
fh = open(fname)
count=0
D = {}
for line in fh:
#************saakin lang ito a *start***********************
    line = line.strip()
    if not line.startswith('From:'):continue
    line1 = line.split('@')
    line2 = line1[1]
    line3 = line2.split('.')
    line4 = line3[0]
    D[line4]=D.get(line4,0)+1
    #     line2 = line[1]
    # wheredotis = line2.find('.')
    # # pieces = pieces[0]
    # pieces = pieces.split('.org')
    # organization = pieces[0]
    count +=1
    print(line)

print('************************************')
for k,v in D.items():
    print(k,v)





# sortbyvalue = {k:v for k,v in sorted(D.items(), key = lambda v:v[1])}
# print(sortbyvalue)
#************saakin lang ito a *end***********************
    email = line4[1]
    cur.execute('SELECT count FROM Counts WHERE email = ? ', (email,))
    row = cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO Counts (email, count)
                VALUES (?, 1)''', (email,))
    else:
        cur.execute('UPDATE Counts SET count = count + 1 WHERE email = ?',
                    (email,))

conn.commit()
# https://www.sqlite.org/lang_select.html
sqlstr = 'SELECT email, count FROM Counts ORDER BY count DESC LIMIT 10'

for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])

cur.close()

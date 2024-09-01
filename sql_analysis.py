import sqlite3

conn = sqlite3.connect('output.db')

cursor = conn.cursor()

cursor.execute("SELECT * FROM person")

rows = cursor.fetchall()

for row in rows:
    print(row)

cursor.close()
conn.close()
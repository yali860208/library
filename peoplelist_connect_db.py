import csv
import sqlite3


with open('peoplelist.csv', newline='',encoding = 'utf8') as f:
    #csv_reader = csv.DictReader(f)
    csv_reader = csv.reader(f)
    members = [(row[0], row[1], row[2], row[3])for row in csv_reader]


with open('create_peoplelist_db.sql') as f:
	create_peoplelist_db_sql = f.read()

db = sqlite3.connect('peoplelist.db')

with db:
	db.executescript(create_peoplelist_db_sql)

with db:
    db.executemany('INSERT INTO  peoplelist (people_id, people_class, people_number, people_name) VALUES (?, ?, ?, ?)',members)
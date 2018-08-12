import csv
import sqlite3


with open('booklist.csv', newline='',encoding = 'utf8') as f:
    #csv_reader = csv.DictReader(f)
    csv_reader = csv.reader(f)
    members = [(row[0], row[1])for row in csv_reader]


with open('create_booklist_db.sql') as f:
	create_booklist_db_sql = f.read()

db = sqlite3.connect('booklist.db')

with db:
	db.executescript(create_booklist_db_sql)

with db:
    db.executemany('INSERT INTO  booklist (book_id, book_name) VALUES (?, ?)',members)
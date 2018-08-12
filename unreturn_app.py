from flask import Flask, g
from flask import render_template, flash, redirect,session, request
#from search_forms import MyForm
from flask_wtf import FlaskForm
import csv
import sqlite3
from wtforms import StringField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY']='my-son-slowlyslowly'

SQLITE_BOOK_DB_PATH = 'booklist.db'
SQLITE_BOOK_DB_SCHEMA = 'create_booklist_db.sql'
BOOK_CSV_PATH = 'booklist.csv'

SQLITE_PEOPLE_DB_PATH = 'peoplelist.db'
SQLITE_PEOPLE_DB_SCHEMA = 'create_peoplelist_db.sql'
PEOPLE_CSV_PATH = 'peoplelist.csv'

#conn_peo_db = sqlite3.connect('peoplelist.db')
#peo_db = conn_peo_db.cursor()

#def get_people_db():
#    db = getattr(g, '_people_database', None)
#    if db is None:
#        db = g._people_database = sqlite3.connect(SQLITE_PEOPLE_DB_PATH)
#        # Enable foreign key check
#        db.execute("PRAGMA foreign_keys = ON")
#    return db

#conn_book_db = sqlite3.connect('booklist.db')
#book_db = conn_book_db.cursor()

#def get_book_db():
#    db = getattr(g, '_book_database', None)
#    if db is None:
#        db = g._book_database = sqlite3.connect(SQLITE_BOOK_DB_PATH)
#        # Enable foreign key check
#        db.execute("PRAGMA foreign_keys = ON")
#    return db

@app.route('/unreturn', methods=['POST'])
def unreturn():
	#book_db = get_book_db()
	#peo_db = get_people_db()

	conn_book_db = sqlite3.connect('booklist.db')
	book_db = conn_book_db.cursor()

	conn_peo_db = sqlite3.connect('peoplelist.db')
	peo_db = conn_peo_db.cursor()


	#顯示資料，確認有無上傳成功
	#test = book_db.execute('SELECT * FROM booklist')
	#test_cursor = [row[3] for row in test]
	#print(test_cursor)

	#for row in book_db.execute("SELECT * FROM booklist"):
	#		print(row)

	unreturn_book_sql = "SELECT book_name, if_borrow FROM booklist WHERE book_id = '{bookid}'".format(bookid=borrow_book_id, )
	
	select_borrowbook_name,select_borrowbook_ifborrow = book_db.execute(borrow_book_sql).fetchone()
	select_borrowpeo_name, borrowdetail_peo_cursor = peo_db.execute(borrow_peo_sql).fetchone()
	#ifborrow_book_cursor = book_db.execute(ifborrow_book_sql)
	#update_book_cursor = update_book_db.execute(borrow_book_sql)

	#select_borrowbook_name = borrow_book_cursor #row[2]=book_name
	#select_borrowpeo_name = borrow_peo_cursor #row[5]=people_name
	select_borrowbook_detail = [borrowdetail_peo_cursor]
	#select_borrowbook_ifborrow = [ifborrow_book_cursor] #row[3]=if_borrow
	print(select_borrowbook_detail)

	i = 0
	for row in select_borrowbook_detail:
		if(row==None):
			break
		else:
			for m in row:
				if(m==','):
					i = i+1
			print(row)
	print('i=',i)

	[select_borrowbook_detail] = select_borrowbook_detail
	print('2',select_borrowbook_detail)

	if (select_borrowbook_name==[]):
		err_msg = "<p>We can\'t find \'{s}\'</p>".format(s=borrow_book_id)
		return err_msg, 404

	elif (select_borrowpeo_name==[]):
		err_msg = "<p>We can\'t find \'{s}\'</p>".format(s=borrow_peo_id)
		return err_msg, 404

	elif (select_borrowbook_ifborrow=='已借出'):
		err_msg = "<p>\'{s}\'已被借出</p>".format(s=borrow_book_id)
		return err_msg, 404

	elif (i>=1):
		err_msg = "<p>\'{s}\'已達借書上限</p>".format(s=borrow_peo_id)
		return err_msg, 404

	else:
		update_borrow_book = "UPDATE booklist SET if_borrow='已借出' WHERE book_id='{bookid}'".format(bookid=borrow_book_id, )
		book_db.execute(update_borrow_book)
		conn_book_db.commit()

		if (select_borrowbook_detail==None):
			select_borrowbook_detail = select_borrowbook_name
			print('if,',select_borrowbook_detail)

		else:
			select_borrowbook_detail=select_borrowbook_detail+','+select_borrowbook_name
			print('borrowdetail=',select_borrowbook_detail)

		update_borrow_peo = "UPDATE peoplelist SET borrow_book='{borrowdetail}' WHERE people_id='{peopleid}'".format(borrowdetail=select_borrowbook_detail, peopleid=borrow_peo_id)
		peo_db.execute(update_borrow_peo)
		conn_peo_db.commit()

		#return '<p>借書成功！姓名：%s, 書名：%s</p>' % (select_borrowpeo_name, select_borrowbook_name)
		return render_template('borrow_solution.html',peoplename=select_borrowpeo_name,bookname=select_borrowbook_name,borrowbook=select_borrowbook_detail)

	conn_book_db.close()
	conn_peo_db.close()





#@app.teardown_appcontext
#def close_connection(exception):
#    db = getattr(g, '_book_database', None)
#    if db is not None:
#        db.close()

#@app.teardown_appcontext
#def close_connection(exception):
#    db = getattr(g, '_people_database', None)
#    if db is not None:
#        db.close()



if __name__ == "__main__":
    app.run(debug=True)



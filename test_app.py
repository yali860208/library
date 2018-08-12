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


class BorrowForm(FlaskForm):
	people_word = StringField('People_word',validators=[DataRequired()])
	book_word = StringField('Book_word',validators=[DataRequired()])




@app.route('/borrow', methods = ['GET', 'POST'])
def borrow():
    form = BorrowForm()
    return render_template('borrow_input.html',form=form)


@app.route('/borrow_solution', methods=['POST'])
def borrow_solution():
	#book_db = get_book_db()
	#peo_db = get_people_db()

	conn_book_db = sqlite3.connect('booklist.db')
	book_db = conn_book_db.cursor()

	conn_peo_db = sqlite3.connect('peoplelist.db')
	peo_db = conn_peo_db.cursor()


	borrow_book_id = request.form.get('book_word')
	borrow_peo_id = request.form.get('people_word')

	#顯示資料，確認有無上傳成功
	#test = book_db.execute('SELECT * FROM booklist')
	#test_cursor = [row[3] for row in test]
	#print(test_cursor)

	#for row in book_db.execute("SELECT * FROM booklist"):
	#		print(row)

	borrow_book_sql = "SELECT book_name, if_borrow FROM booklist WHERE book_id = '{bookid}'".format(bookid=borrow_book_id, )
	borrow_peo_sql = "SELECT people_name, borrow_book FROM peoplelist WHERE people_id = '{peopleid}'".format(peopleid=borrow_peo_id, )
	
	a = book_db.execute(borrow_book_sql).fetchone()
	b = peo_db.execute(borrow_peo_sql).fetchone()

	print(a)
	print(b)

	if (a==None):
		err_msg = "<p>書目條碼輸入錯誤</p>"
		return err_msg, 404

	elif(b==None):
		err_msg = "<p>成員條碼輸入錯誤</p>"
		return err_msg, 404


	else:
		select_borrowbook_name,select_borrowbook_ifborrow = book_db.execute(borrow_book_sql).fetchone()
		select_borrowpeo_name, select_borrowbook_detail = peo_db.execute(borrow_peo_sql).fetchone()
		#ifborrow_book_cursor = book_db.execute(ifborrow_book_sql)
		#update_book_cursor = update_book_db.execute(borrow_book_sql)

		#select_borrowbook_name = borrow_book_cursor #row[2]=book_name
		#select_borrowpeo_name = borrow_peo_cursor #row[5]=people_name
		#select_borrowbook_detail = [borrowdetail_peo_cursor]
		#select_borrowbook_ifborrow = [ifborrow_book_cursor] #row[3]=if_borrow
		print(select_borrowbook_detail)

		i=0

		if (select_borrowbook_detail==None):
			pass
		else:
			select_borrowbook_detail=select_borrowbook_detail.split(',')
			i=len(select_borrowbook_detail)
			print(i)

		#[select_borrowbook_detail] = select_borrowbook_detail
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

		elif (i>=2):
			err_msg = "<p>\'{s}\'已達借書上限</p>".format(s=borrow_peo_id)
			return err_msg, 404

		else:
			update_borrow_book = "UPDATE booklist SET if_borrow='已借出' WHERE book_id='{bookid}'".format(bookid=borrow_book_id, )
			book_db.execute(update_borrow_book)
			conn_book_db.commit()

			if (select_borrowbook_detail==None):
				last_borrowbook_detail = select_borrowbook_name
				print('if,',last_borrowbook_detail)

			else:
				last_borrowbook_detail = ''
				for m in select_borrowbook_detail:
					last_borrowbook_detail+=m+','
				last_borrowbook_detail+=select_borrowbook_name
				print('borrowdetail=',last_borrowbook_detail)

			update_borrow_peo = "UPDATE peoplelist SET borrow_book='{borrowdetail}' WHERE people_id='{peopleid}'".format(borrowdetail=last_borrowbook_detail, peopleid=borrow_peo_id)
			peo_db.execute(update_borrow_peo)
			conn_peo_db.commit()

			#return '<p>借書成功！姓名：%s, 書名：%s</p>' % (select_borrowpeo_name, select_borrowbook_name)
			return render_template('borrow_solution.html',peoplename=select_borrowpeo_name,bookname=select_borrowbook_name,borrowbook=last_borrowbook_detail)

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



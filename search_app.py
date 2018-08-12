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

#def get_db():
#    db = getattr(g, '_database', None)
#    if db is None:
#        db = g._database = sqlite3.connect(SQLITE_BOOK_DB_PATH)
        # Enable foreign key check
#        db.execute("PRAGMA foreign_keys = ON")
#    return db


class SearchForm(FlaskForm):
	key_word = StringField('KeyWord',validators=[DataRequired()])


@app.route('/search', methods = ['GET', 'POST'])
def search():
    form = SearchForm()
    return render_template('search_input.html',form=form)


@app.route('/search_solution', methods=['POST'])
def search_solution():
	conn_book_db = sqlite3.connect('booklist.db')
	book_db = conn_book_db.cursor()

	conn_peo_db = sqlite3.connect('peoplelist.db')
	peo_db = conn_peo_db.cursor()

	key_word = request.form.get('key_word')
	print(key_word)

	#顯示資料，確認有無上傳成功
	#test = db.execute('SELECT * FROM members')
	#test_cursor = [row[2] for row in test]
	#print(test_cursor)

	search_book_sql = "SELECT id FROM booklist WHERE book_name LIKE '%{keyword}%' OR book_id LIKE '%{key}%'".format(keyword=key_word,key=key_word )
	#allword_members_sql = 'SELECT id FROM members '
	#allword_members_sql += 'WHERE book_name LIKE \'%&key_word%\''
	search_book_cursor = book_db.execute(search_book_sql)
	#select_member_names = ['SELECT book_name FROM cursor']
	select_book_ids = [row[0] for row in search_book_cursor]
	print(select_book_ids)

    #if not select_member_names:
	if (select_book_ids==[]):
    	#err_msg = f'We cannot find {key_word}'
         err_msg = "<p>We can\'t find \'{s}\'</p>".format(s=key_word)

         return err_msg, 404



	last_book_id = []
	last_book_name = []
	for i in select_book_ids:
		search_book_id, search_book_name = book_db.execute('SELECT book_id, book_name FROM booklist WHERE id = {id}'.format(id=i, )).fetchone()
		last_book_id.append(search_book_id)
		last_book_name.append(search_book_name)

	return render_template(
        'search_solution.html',
        bookid=last_book_id,
        bookname=last_book_name,
    )

	conn_book_db.close()
	conn_peo_db.close()


#SELECT id FROM members WHERE * LIKE %%


#@app.teardown_appcontext
#def close_connection(exception):
#    db = getattr(g, '_database', None)
#    if db is not None:
#        db.close()



if __name__ == "__main__":
    app.run(debug=True)



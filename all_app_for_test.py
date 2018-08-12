from flask import Flask, g
from flask import render_template, flash, redirect,session, request
#from search_forms import MyForm
from flask_wtf import FlaskForm
import csv
import psycopg2
from wtforms import StringField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY']='my-son-slowlyslowly'

SQLITE_BOOK_DB_PATH = 'booklist.db'
BOOK_CSV_PATH = 'booklist.csv'

SQLITE_PEOPLE_DB_PATH = 'peoplelist.db'
PEOPLE_CSV_PATH = 'peoplelist_include_status.csv'



@app.route('/library')
def index():
    return render_template('homebase.html', title='Library')

#----------------------------------------------------------
#Search

class SearchForm(FlaskForm):
	key_word = StringField('KeyWord',validators=[DataRequired()])


@app.route('/search', methods = ['GET', 'POST'])
def search():
    form = SearchForm()
    return render_template('search_input.html',title = 'Search',form=form)


@app.route('/search_solution', methods=['POST'])
def search_solution():

	conn_book_db = psycopg2.connect(database="booklist", user="stella", password="Janeslowly", host="127.0.0.1", port="5432")
	book_db = conn_book_db.cursor()

	conn_peo_db = psycopg2.connect(database="peoplelist", user="stella", password="Janeslowly", host="127.0.0.1", port="5432")
	peo_db = conn_peo_db.cursor()

	key_word = request.form.get('key_word')

	#顯示資料，確認有無上傳成功
	#test = "SELECT * FROM booklist;"
	#book_db.execute(test)
	#a=book_db.fetchall()
	#print(a)

	book_db.execute("SELECT id FROM booklist WHERE book_name LIKE '%{keyword}%' OR book_id LIKE '%{key}%'".format(keyword=key_word,key=key_word ))
	#search_book_sql = "SELECT id FROM booklist WHERE book_name LIKE '%{keyword}%' OR book_id LIKE '%{key}%'".format(keyword=key_word,key=key_word )
	#book_db.execute(search_book_sql)

	a = book_db.fetchone()
	if (a==None):
		err_msg = "<p>書目條碼輸入錯誤</p>"
		return err_msg, 404

	#allword_members_sql = 'SELECT id FROM members '
	#allword_members_sql += 'WHERE book_name LIKE \'%&key_word%\''
	book_db.execute("SELECT id FROM booklist WHERE book_name LIKE '%{keyword}%' OR book_id LIKE '%{key}%'".format(keyword=key_word,key=key_word ))
	search_book_cursor = book_db.fetchall()
	#select_member_names = ['SELECT book_name FROM cursor']
	select_book_ids = [row[0] for row in search_book_cursor]
	print(select_book_ids)

    #if not select_member_names:
	if (select_book_ids==[]):
		#err_msg = f'We cannot find {key_word}'
		err_msg = "<p>We can\'t find \'{s}\'</p>".format(s=key_word)
		return err_msg, 404

	else:
		pass


	last_book_id = []
	last_book_name = []
	for i in select_book_ids:
		book_db.execute('SELECT book_id, book_name FROM booklist WHERE id = {id}'.format(id=i, ))
		search_book_id, search_book_name = book_db.fetchone()
		last_book_id.append(search_book_id)
		last_book_name.append(search_book_name)

	return render_template(
        'search_solution.html',
        bookid=last_book_id,
        bookname=last_book_name,
    )

	conn_book_db.close()
	conn_peo_db.close()

#------------------------------------------------------


if __name__ == "__main__":
    app.run(debug=True)



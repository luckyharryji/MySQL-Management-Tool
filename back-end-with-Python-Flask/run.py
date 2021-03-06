# all the imports
import sqlite3
from flask import Flask, make_response, request, current_app, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
from mysqlClient import MySqlClient
from datetime import timedelta
from functools import update_wrapper
from cross_domain import crossdomain


# create our little application :)
app = Flask(__name__)
app.config.from_envvar('FLASKR_SETTINGS')


mysql_service = MySqlClient('localhost', 3306, 'root', '19930801')


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/people/list')
def get_all_people_info():
    return mysql_service.get_all_people_info()


@app.route('/databases')
@crossdomain(origin='*')
def get_all_databases():
    return mysql_service.get_database_names()


@app.route('/add/database/<database_name>')
def add_new_database(database_name):
    return mysql_service.create_new_database(database_name)


@app.route('/delete/database/<database_name>')
def delete_database(database_name):
    return mysql_service.delete_database(database_name)

@app.route('/table/list')
def get_all_tables():
    return mysql_service.get_tables_name()


@app.route('/')
def show_entries():
    cur = g.db.execute('select title,text from entries order by id DESC ')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


init_db()

if __name__ == '__main__':
    app.run()
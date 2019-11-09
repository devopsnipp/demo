# all the imports
import sqlite3
import config

from flask import (
    Flask, request, session, g, redirect, url_for,
    abort, render_template, flash
)


DEFAULT_VIEW = 'show_courses'

app = Flask(__name__)
app.config.from_object(config)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
def show_courses():
    cur = g.db.execute('select name, instructor from courses order by id desc')
    courses = [dict(name=row[0], instructor=row[1]) for row in cur.fetchall()]
    return render_template('show_courses.html', courses=courses)


@app.route('/add', methods=['POST'])
def add_course():
    if not session.get('logged_in'):
        abort(401)
    name = request.form['name']
    instructor = request.form['instructor']
    description = request.form['description']
    if not all([name, instructor]):
        flash('ERROR. Missing data.', 'error')
    else:
        g.db.execute(
            'insert into courses (name, instructor, description) values (?, ?, ?)',
            [name, instructor, description])
        g.db.commit()
        flash('New entry was successfully posted')
    return redirect(url_for(DEFAULT_VIEW))


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
            return redirect(url_for(DEFAULT_VIEW))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for(DEFAULT_VIEW))


if __name__ == '__main__':
    # create our little application :)
    app.run()

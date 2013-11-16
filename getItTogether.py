'''
Get It Together:

Because program managers don't know what they are doing
'''


from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy

# TODO: move user creation
GOOD_USERNAME='nufootball'
GOOD_PASSWORD='sucks'
BAD_PASSWORD='rocks'

# create our little application :)
app = Flask(__name__)

# Load config.py
app.config.from_object('config')

db = SQLAlchemy(app)

import models

def verify_user(username, password):
    """Checks if user is registered"""
    res = models.User.query.filter(models.User.username == username, models.User.password == password).first()
    # print res
    return res

@app.route('/add', methods=['POST'])
def add_feedback():
    if not session.get('logged_in'):
        abort(401)
    # This is a hack until we integrate flask-login
    p = models.Post (title=request.form['title'], text=request.form['text'], \
        points=0, userId=0)
    db.session.add(p)
    db.session.commit()
    flash('New feedback was successfully posted')
    return redirect(url_for('show_feedback'))
        
@app.route('/')
def show_feedback():
    feedback = models.Post.query.all()
    return render_template('show_feedback.html', feedback=feedback)
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if not verify_user(request.form['username'], request.form['password']):
            error = 'Invalid username or password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_feedback'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_feedback'))    
        
if __name__ == '__main__':
    if not models.User.query.all():
        u = models.User(username = GOOD_USERNAME, password = GOOD_PASSWORD, \
            email = 'nufootballsucks@northwestern.edu', role = 0)
        db.session.add(u)
        db.session.commit()
    app.run()
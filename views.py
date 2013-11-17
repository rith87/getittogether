from flask import render_template, flash, redirect, request, session, \
    g, url_for, abort
from getItTogether import app, db
from models import User, Post

def verify_user(username, password):
    """Checks if user is registered"""
    res = User.query.filter(User.username == username, User.password == password).first()
    # print res
    return res

@app.route('/add', methods=['POST'])
def add_feedback():
    if not session.get('logged_in'):
        abort(401)
    # This is a hack until we integrate flask-login
    p = Post (title=request.form['title'], text=request.form['text'], \
        points=0, userId=0)
    db.session.add(p)
    db.session.commit()
    flash('New feedback was successfully posted')
    return redirect(url_for('show_feedback'))
        
@app.route('/')
def show_feedback():
    feedback = Post.query.all()
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
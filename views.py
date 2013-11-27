from flask import render_template, flash, redirect, request, session, \
    g, url_for, abort
from flask.ext.login import login_user, logout_user, current_user, login_required
from getItTogether import app, db, lm
from models import User, Post
from forms import LoginForm

'''
Bugs/pending issues:
1. Add user registration functionality
2. User profile page
3. Use jquery to dynamically update the points
4. Some weird bug with user logged in but cannot post message until logout_user is called
'''

def find_user(username, password):
    """Checks if user is registered"""
    user = User.query.filter(User.username == username, User.password == password).first()
    # print res
    return user

# Flask-login related decorated functions    
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))    
    
# App related decorated functions    
@app.route('/add', methods=['POST'])
@login_required
def add_feedback():
    user = g.user
    # print user
    if user.is_anonymous() and not session.get('logged_in'):
        abort(401)
    p = Post (title=request.form['title'], text=request.form['text'], \
        points=0, userId=user.id)
    db.session.add(p)
    db.session.commit()
    flash('New feedback was successfully posted')
    return redirect(url_for('show_feedback'))
        
@app.route('/', methods=['GET', 'POST'])
def show_feedback():
    flash('Help software companies stop sucking!')
    feedback = Post.query.all()
    # users = []
    refinedFeedback = []
    if request.method == 'POST':
        # print request.form
        if 'upvote' in request.form.keys():
            flash('Thanks for your upvote!')
        elif 'downvote' in request.form.keys():
            flash('Thanks for your downvote!')
    for item in feedback:
        # users.append(User.query.get(item.userId))
        refinedFeedback.append((item, User.query.get(item.userId)))
    # return render_template('show_feedback.html', feedback=feedback, users=users)
    return render_template('show_feedback.html', feedback=refinedFeedback)    
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm()
    if g.user is not None and g.user.is_authenticated():
        print 'Redirecting...'
        return redirect(url_for('show_feedback'))
    if request.method == 'POST':
        user = find_user(request.form['username'], request.form['password'])
        if not user:
            error = 'Invalid username or password'
        else:
            # Always remember user
            login_user(user, remember = True)
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_feedback'))
    return render_template('login.html', error=error, form=form)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    logout_user()
    flash('You were logged out')
    return redirect(url_for('show_feedback')) 
    
@app.before_request
def before_request():
    g.user = current_user
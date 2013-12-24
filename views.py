from flask import render_template, flash, redirect, request, \
    g, url_for, abort
from flask.ext.login import login_user, logout_user, current_user, login_required
from getItTogether import app, db, lm, screenshots
from models import User, Post, Screenshot
from forms import LoginForm, RegistrationForm

'''
Bugs/pending issues:
1. Move user registration to open id?
5. Need to build some comments tree for comments on feedback
9. Current user information is stored in year long cookie??
10. Need to implement logging for errors/warnings/info
12. Need admin account
13. Posts should have time stamps because we want to sort by time/points
14. How to handle multiple pages of feedback?
'''

def find_user(username, password):
    """Checks if user is registered"""
    user = User.query.filter(User.username == username, User.password == password).first()
    # print res
    return user

def handle_vote(form):
    # print form
    vote = ''
    if 'upvote' in form.keys():
        vote = 'upvote'
    elif 'downvote' in form.keys():
        vote = 'downvote'
    else:
        print 'No vote?'
        return    
    flash('Thanks for your %s!' % vote)
    post = Post.query.get(request.form[vote])
    post.points += 1 if vote == 'upvote' else -1
    db.session.commit()
    
def handle_screenshot_upload(postId):
    if request.method == 'POST' and 'screenshot' in request.files:
        filename = screenshots.save(request.files['screenshot'])
        ss = Screenshot(filename=filename, postId=postId)
        db.session.add(ss)
        db.session.commit()
        flash("Screenshot saved.")    
    
def find_screenshot_from_post(postId):
    # check for screenshot
    ssUrl = None
    ssTitle = None
    ss = Screenshot.query.filter(Screenshot.postId == postId).first() 
    if ss:
        ssUrl = screenshots.url(ss.filename)
        ssTitle = ss.filename
    return (ssUrl, ssTitle)
    
# Flask-login related decorated functions    
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))    
    
# App related decorated functions    
@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_feedback():
    user = g.user
    # print user
    # print request.form
    # print request.files
    if user.is_anonymous():
        abort(401)
    if request.method == 'GET':
        return render_template('add_feedback.html')
    if 'test' in request.form.keys() and request.form['test']:
        flash('Staging feedback')
        filename = None
        ssUrl = None
        if 'screenshot' in request.files:
            filename = screenshots.save(request.files['screenshot'])
            ssUrl = screenshots.url(filename)
        return render_template('show.html', title=request.form['title'], \
            text=request.form['text'], url=ssUrl, filename=filename)
    p = Post (title=request.form['title'], text=request.form['text'], \
        points=0, userId=user.id)
    db.session.add(p)
    db.session.commit()
    flash('New feedback was successfully posted')
    handle_screenshot_upload(p.id)
    return redirect(url_for('show_feedback'))

@app.route('/', methods=['GET', 'POST'])
def show_feedback():
    flash('Help software companies stop sucking!')
    feedback = Post.query.order_by(Post.points.desc()).limit(10).all()
    # users = []
    refinedFeedback = []
    if request.method == 'POST':
        handle_vote(request.form)
    for item in feedback:
        (ssUrl, ssTitle) = find_screenshot_from_post(item.id)
        refinedFeedback.append((item, User.query.get(item.userId), ssUrl, ssTitle))
    return render_template('show_feedback.html', feedback=refinedFeedback)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return redirect(url_for('show_feedback'))
    (ssUrl, ssTitle) = find_screenshot_from_post(post_id)
    return render_template('show.html', title=post.title, text=post.text, \
        url=ssUrl, filename=ssTitle)

@app.route('/profile')
@login_required
def show_profile():
    # user must be valid
    user = g.user
    posts = Post.query.filter_by(userId=user.id).all()
    points = 0
    for post in posts:
        points += post.points
    return render_template('show_profile.html', user=user, points=points)
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        flash('Thanks for registering!')
        user = User(username = request.form['username'], 
            password = request.form['password'],
            email = request.form['email'])
        db.session.add(user)
        db.session.commit()
    return render_template('register.html', form=form)
    
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
            flash('You were logged in')
            return redirect(url_for('show_feedback'))
    return render_template('login.html', error=error, form=form)
    
@app.route('/logout')
def logout():
    logout_user()
    flash('You were logged out')
    return redirect(url_for('show_feedback')) 
    
@app.before_request
def before_request():
    g.user = current_user
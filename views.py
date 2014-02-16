from flask import render_template, flash, redirect, request, \
    g, url_for, abort, make_response, session
from flask.ext.login import login_user, logout_user, current_user, login_required
from getItTogether import app, db, lm, screenshots, oid
from models import User, Post, Screenshot, Note, Comment
from forms import LoginForm, RegistrationForm
from config import UPLOADED_SCREENSHOTS_DEST, POSTS_PER_PAGE
from base64 import b64decode
from sqlalchemy.sql import func
import inspect
import datetime
import time

'''
Bugs/pending issues:
1. Move user registration to open id <-- partially moved, need tests
5. Need to build some comments tree for comments on feedback <-- not critical
12. Need admin account
16. Why is input sanitized only in some scenarios?
17. Server hangs when gg.jpg is uploaded?
18. delete feedback needs to delete screenshots/notes linked to feedback
19. Refactor find_*_from_post
20. Sort feedback by companies
22. Upvote/downvote buttons could be fancier
23. Delete in profile page should redirect to profile page
26. Upload and annotate pages should be combined
28. Next
'''

def handle_request_error(error):
    app.logger.error('[%d] Request.form: %s' % (error, request.form))
    abort(error)

def find_user(username, password):
    """Checks if user is registered"""
    user = User.query.filter(User.username == username, User.password == password).first()
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
    
def handle_screenshot_upload(postId, filename):
    if request.method == 'POST' and filename:
        # print 'Uploading screenshot'
        ss = Screenshot(filename=filename, postId=postId)
        db.session.add(ss)
        db.session.commit()
        flash("Screenshot saved.")    
    
def handle_notes_upload(postId):
    # TODO: Validate if post ID exists!
    note = request.form.get('notes')
    if note:
        n = Note (note=note, postId=postId)
        db.session.add(n)
        db.session.commit()
        app.logger.debug('Uploading notes: Post Id=%d, Note=%s' % (n.postId, n.note))
    return redirect(url_for('show_post', post_id=postId))    
    
def find_screenshot_from_post(postId):
    # check for screenshot
    ssUrl = None
    ssTitle = None
    ss = Screenshot.query.filter(Screenshot.postId == postId).first() 
    if ss:
        ssUrl = screenshots.url(ss.filename)
        ssTitle = ss.filename
    return (ssUrl, ssTitle)
    
def find_comments_from_post(postId):
    return Comment.query.filter(Comment.postId==postId).all() 
    
def find_notes_from_post(postId):
    notes = Note.query.filter(Note.postId==postId).first()
    notesResponse = ''
    if notes:
        notesResponse = notes.note
    app.logger.debug('Retrieving notes: Post Id=%s, Note=%s' % (postId, notesResponse))
    return make_response(notesResponse)

# find_post output is guaranteed to be good
def find_post(form):
    postId = form.get('postId')
    if not postId:
        handle_request_error(400)
    p = Post.query.get(postId)
    if not p:
        handle_request_error(400)
    return p
    
def attach_screenshots_to_feedback(feedback):
    refinedFeedback = []
    for item in feedback:
        (ssUrl, ssTitle) = find_screenshot_from_post(item.id)
        refinedFeedback.append((item, User.query.get(item.userId), ssUrl, ssTitle))    
    return refinedFeedback
    
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
        handle_request_error(401)
    if request.method == 'GET':
        return render_template('add_feedback.html')
    p = Post (title=request.form['title'], text=request.form['text'], \
        timestamp=datetime.datetime.utcnow(), points=0, userId=user.id)
    if request.form.get('test'):
        flash('Staging feedback')
        filename = None
        ssUrl = None
        if 'screenshot' in request.files:
            filename = screenshots.save(request.files['screenshot'])
            ssUrl = screenshots.url(filename)
        if 'screenshotDataUrl' in request.form:
            # May fail if multiple users post in the same microsecond
            dataUrl = request.form['screenshotDataUrl'].split(',')
            decodedScreenshot = b64decode(dataUrl[1])
            filename = '%s.png' % (int(time.time() * 1000000))
            f = open ('%s\\%s' % (UPLOADED_SCREENSHOTS_DEST, filename), 'wb')
            f.write(decodedScreenshot)
            ssUrl = screenshots.url(filename)            
            f.close()
        return render_template('show.html', post=p,
            url=ssUrl, filename=filename)
    db.session.add(p)
    db.session.commit()
    app.logger.debug('Post saved: Post id=%d, Title=%s' % (p.id, p.title))
    flash('New feedback was successfully posted')
    if 'filename' in request.form.keys():
        handle_screenshot_upload(p.id, request.form['filename'])
    # handle_screenshot_upload(p.id, request.form['filename'] if 'filename' in request.form else None)
    handle_notes_upload(p.id)
    return redirect(url_for('show_feedback'))

@app.route('/comment', methods=['POST'])
@login_required
def add_comment():
    p = find_post(request.form)
    comment = request.form.get('comment')
    c = Comment(comment=comment, parent=-1, timestamp=datetime.datetime.utcnow(), \
        postId=p.id, userId=g.user.id)
    db.session.add(c)
    db.session.commit()
    return redirect(url_for('show_post', post_id=p.id))    
    
@app.route('/edit', methods=['POST'])
@login_required
def edit_feedback():
    p = find_post(request.form)
    if g.user.id != p.userId:
        handle_request_error(403)
    newTitle = request.form.get('title')
    if newTitle:
        p.title = newTitle
    newText = request.form.get('text')
    if newText:
        p.text = newText
    n = Note.query.filter(Note.postId==p.id).first()
    if n:
        # TODO: What if this is the first note in post?
        newNote = request.form.get('notes')
        if newNote:
            n.note = newNote
    db.session.commit()
    return redirect(url_for('show_post', post_id=p.id))

@app.route('/delete', methods=['POST'])
@login_required
def delete_feedback():
    p = find_post(request.form)
    if g.user.id != p.userId:
        handle_request_error(403)
    app.logger.debug('Post deleted: Post id=%d' % p.id)
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('show_profile'))
    
@app.route('/notes', methods=['GET', 'POST'])
@login_required
def handle_notes():
    if request.method == 'GET':
        postId = request.args.get('postId')
        print postId
        if not postId:
            handle_request_error(400)
        return find_notes_from_post(postId)    
    else:
        postId = request.form.get('postId')
        notes = request.form.get('notes')
        if not postId or not notes:
            handle_request_error(400)
        app.logger.debug('Handling notes request: Post id=%s; Notes=%s' \
            % (postId, notes))
        return handle_notes_upload(postId)
    
@app.route('/', methods=['GET', 'POST'])
@app.route('/<int:page>', methods=['GET', 'POST'])
def show_feedback(page = 1):
    flash('Help software companies stop sucking!')
    # Note that cast() operator does not work with DATE and sqlite. Use func.DATE() instead
    # http://stackoverflow.com/questions/17333014/convert-selected-datetime-to-date-in-sqlalchemy
    pagedFeedback = Post.query.order_by((func.DATE(Post.timestamp)).desc(), \
                    Post.points.desc()).paginate(page, POSTS_PER_PAGE, False)
    feedback = pagedFeedback.items
    if request.method == 'POST':
        handle_vote(request.form)
    refinedFeedback = attach_screenshots_to_feedback(feedback)
    return render_template('show_feedback.html', page=pagedFeedback, feedback=refinedFeedback)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return redirect(url_for('show_feedback'))
    (ssUrl, ssTitle) = find_screenshot_from_post(post_id)
    comments = find_comments_from_post(post_id)
    return render_template('show.html', post=post, url=ssUrl, filename=ssTitle, comments=comments)

@app.route('/profile')
@login_required
def show_profile():
    # user must be valid
    user = g.user
    posts = Post.query.filter_by(userId=user.id).order_by(Post.points.desc(), Post.timestamp.desc())
    points = 0
    for post in posts:
        points += post.points
    refinedFeedback = attach_screenshots_to_feedback(posts)
    return render_template('show_profile.html', user=user, points=points, feedback=refinedFeedback)
    
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
@oid.loginhandler
def login():
    error = None
    form = LoginForm()
    if g.user is not None and g.user.is_authenticated():
        print 'Redirecting...'
        return redirect(url_for('show_feedback'))
    if request.method == 'POST':
        # return oid.try_login(request.form['username'], ask_for=['email'])
        user = find_user(request.form['username'], request.form['password'])
        if not user:
            error = 'Invalid username or password'
        else:
            # Always remember user
            remember = False
            if request.form.get('remember_me') == 'y':
                remember = True
            login_user(user, remember = remember)
            flash('You were logged in')
            return redirect(url_for('show_feedback'))
    return render_template('login.html', error=error, form=form)
    
@oid.after_login
def after_login(resp):
    print 'email:%s, nickname:%s' % (resp.email, resp.nickname)
    return redirect(url_for('show_feedback'))    
    
@app.route('/logout')
def logout():
    logout_user()
    flash('You were logged out')
    return redirect(url_for('show_feedback')) 
    
@app.before_request
def before_request():
    g.user = current_user
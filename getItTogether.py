'''
Get It Together:

Because program managers don't know what they are doing
'''


from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash

# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE='getItTogether.db',
    DEBUG=True,
    SECRET_KEY='development key'    
))

def init_db():
    """Creates the database tables."""
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def verify_user(username, password):
    """Checks if user is registered"""
    db = get_db()
    cur = db.execute('select * from users where username=? and password=?', \
        [username, password])
    return cur.fetchall()
    
@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/add', methods=['POST'])
def add_feedback():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    # This is a hack until we integrate flask-login
    db.execute('insert into feedback (title, text, userId, points) values (?, ?, ?, ?)',
                 [request.form['title'], request.form['text'], 0, 0])
    db.commit()
    flash('New feedback was successfully posted')
    return redirect(url_for('show_feedback'))
        
@app.route('/')
def show_feedback():
    db = get_db()
    cur = db.execute('select title, text from feedback order by id desc')
    feedback = cur.fetchall()
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
    init_db()
    app.run()
from flask import Flask, url_for, request, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id    
    
# where does request get defined?    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'On log in'
    else:
        return 'Log in'
    
if __name__ == '__main__':
    app.run(debug=True)
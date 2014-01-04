import os
from getItTogether import *
import unittest
import tempfile

from config import basedir
from models import User, Post

GOOD_USERNAME='nufootball'
GOOD_PASSWORD='sucks'
BAD_PASSWORD='rocks'

class getItTogetherTestCase(unittest.TestCase):

    def setUp(self):
        """Before each test, set up a blank database"""
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()
        u = User(username = GOOD_USERNAME, password = GOOD_PASSWORD, \
            email = 'nufootballsucks@northwestern.edu', role = 0)
        db.session.add(u)
        db.session.commit()

    def tearDown(self):
        """Get rid of the database again after each test."""
        db.session.remove()
        db.drop_all()

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)
        
    def get_profile(self):
        return self.app.get('/profile', follow_redirects=True)
        
    def post(self, partial):
        data = {}
        data['title'] = '<Hello>'
        data['text'] = '<strong>HTML</strong> allowed here'
        data['set'] = 'True'
        if partial:
            data['test'] = True
        return self.app.post('/add', data=data, follow_redirects=True)
        
    def vote(self, id, up):
        if up:
            return self.app.post('/', data=dict(
                upvote=id
            ), follow_redirects=True)
        else:
            return self.app.post('/', data=dict(
                downvote=id
            ), follow_redirects=True)

    def set_notes(self, id):
        data = {}
        data['postId'] = id
        data['notes'] = '{text:wtf}'
        data['set'] = True
        self.app.post('/notes', data=data, follow_redirects=True)
        
    def get_notes(self, id):
        data = {}
        data['postId'] = id
        data['notes'] = ''
        data['set'] = False
        return self.app.post('/notes', data=data, follow_redirects=True)        
        
    def test_successful_login_logout(self):
        """Make sure login and logout succeeds"""
        rv = self.login(GOOD_USERNAME, GOOD_PASSWORD)
        # print rv.data
        assert b'You were logged in' in rv.data
        rv = self.logout()
        assert b'You were logged out' in rv.data
        
    def test_fail_login_logout(self):
        """Make sure login fails"""
        rv = self.login(GOOD_USERNAME, BAD_PASSWORD)
        assert b'Invalid username or password' in rv.data

    def test_successful_post(self):
        """Test that messages work"""
        self.login(GOOD_USERNAME, GOOD_PASSWORD)
        rv = self.post(False)
        # print rv.data
        assert b'No entries here so far' not in rv.data
        assert b'&lt;Hello&gt;' in rv.data
        assert b'feedbackBox' in rv.data
        assert b'<strong>HTML</strong> allowed here' in rv.data
        self.logout()
        
    def test_successful_partial_post(self):
        """Test the partial post to staging area"""
        self.login(GOOD_USERNAME, GOOD_PASSWORD)
        rv = self.post(True)
        # print rv.data
        assert b'Staging feedback' in rv.data
        assert b'feedbackBox' not in rv.data
        
    def test_post_annotations(self):
        """Test that annotations can be saved and retrieved"""
        self.login(GOOD_USERNAME, GOOD_PASSWORD)
        rv = self.post(False)
        # print rv.data
        assert b'Staging feedback' not in rv.data
        assert b'feedbackBox' in rv.data
        rv = self.set_notes(0)
        rv = self.get_notes(0)
        # print rv.data
        assert b'wtf' in rv.data
        
    def test_post_without_login(self):
        """Test post message without login"""
        rv = self.post(False)
        # assert b'401 Unauthorized' in rv.data
        assert b'Login' in rv.data
        assert b'Username:' in rv.data
        
    def test_post_author(self):
        """Test that messages have the correct author"""
        self.login(GOOD_USERNAME, GOOD_PASSWORD)
        rv = self.post(False)
        # print rv.data
        assert GOOD_USERNAME in rv.data
        self.logout()
    
    def test_non_post(self):
        rv = self.app.get('/post/1')
        # print rv.data
        assert b'Redirecting' in rv.data
    
    def test_vote(self):
        """Test that any user can vote on an idea"""
        self.login(GOOD_USERNAME, GOOD_PASSWORD)
        rv = self.post(False)
        rv = self.vote(1, True)
        # print rv.data
        assert b'Thanks for your upvote!' in rv.data
        assert b'1 points' in rv.data
        rv = self.vote(1, False)
        # print rv.data
        assert b'Thanks for your downvote!' in rv.data        
        assert b'0 points' in rv.data        
        self.logout()
    
    def test_register_user(self):
        """Test that any user can register and log in"""
        rv = self.app.post('/register', data=dict(
            username='lol',
            password='wtf',
            email='lol@wtf.com'
        ), follow_redirects=True)
        assert b'Thanks for registering!' in rv.data
        rv = self.login('lol', 'wtf')
        assert b'You were logged in' in rv.data
        rv = self.logout()
        assert b'You were logged out' in rv.data        
        
    def test_user_points(self):
        """Test that the users points are tallied correctly"""
        self.login(GOOD_USERNAME, GOOD_PASSWORD)        
        rv = self.post(False)
        rv = self.get_profile()
        assert b'Points: 0' in rv.data
        rv = self.vote(1, True) 
        rv = self.get_profile()
        assert b'Points: 1' in rv.data        
        rv = self.post(False)
        rv = self.vote(1, True) 
        rv = self.get_profile()
        assert b'Points: 2' in rv.data        
        self.logout()
        
if __name__ == '__main__':
    unittest.main()
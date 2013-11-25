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
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here'
        ), follow_redirects=True)
        # print rv.data
        assert b'No entries here so far' not in rv.data
        assert b'&lt;Hello&gt;' in rv.data
        assert b'<strong>HTML</strong> allowed here' in rv.data
        
    def test_post_without_login(self):
        """Test post message without login"""
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='YOU SHOULD NOT SEE THIS'
        ), follow_redirects=True)
        assert b'401 Unauthorized' in rv.data
        
    def test_post_author(self):
        """Test that messages have the correct author"""
        self.login(GOOD_USERNAME, GOOD_PASSWORD)
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here'
        ), follow_redirects=True)
        assert GOOD_USERNAME in rv.data
        
if __name__ == '__main__':
    unittest.main()
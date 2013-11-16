import os
import getItTogether
import unittest
import tempfile

GOOD_USERNAME='nufootball'
GOOD_PASSWORD='sucks'
BAD_PASSWORD='rocks'

class getItTogetherTestCase(unittest.TestCase):

    def setUp(self):
        """Before each test, set up a blank database"""
        self.db_fd, getItTogether.app.config['DATABASE'] = tempfile.mkstemp()
        getItTogether.app.config['TESTING'] = True
        self.app = getItTogether.app.test_client()
        getItTogether.init_db()

    def tearDown(self):
        """Get rid of the database again after each test."""
        os.close(self.db_fd)
        os.unlink(getItTogether.app.config['DATABASE'])

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
        
if __name__ == '__main__':
    unittest.main()
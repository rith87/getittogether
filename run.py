from getItTogether import app, db
import models
import views

# TODO: move user creation
GOOD_USERNAME='nufootball'
GOOD_PASSWORD='sucks'
BAD_PASSWORD='rocks'

if __name__ == '__main__':
    if not models.User.query.all():
        u = models.User(username = GOOD_USERNAME, password = GOOD_PASSWORD, \
            email = 'nufootballsucks@northwestern.edu', role = 0)
        db.session.add(u)
        db.session.commit()
    app.run()
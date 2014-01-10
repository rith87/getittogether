'''
Get It Together:

Because program managers don't know what they are doing
'''


from sqlite3 import dbapi2 as sqlite3
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.uploads import UploadSet, IMAGES, configure_uploads
import logging

# create our little application :)
app = Flask(__name__)

# Load config.py
app.config.from_object('config')

db = SQLAlchemy(app)

# Use flask-login to handle users
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

screenshots = UploadSet('screenshots', IMAGES)
configure_uploads(app, screenshots)

file_handler = logging.FileHandler('getItTogether.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(funcName)s():%(lineno)d]'
))
app.logger.addHandler(file_handler)

import models
import views
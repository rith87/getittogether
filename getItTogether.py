'''
Get It Together:

Because program managers don't know what they are doing
'''


from sqlite3 import dbapi2 as sqlite3
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

# create our little application :)
app = Flask(__name__)

# Load config.py
app.config.from_object('config')

db = SQLAlchemy(app)

# Use flask-login to handle users
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

import models
import views
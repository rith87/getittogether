import os
from datetime import timedelta
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG=True
SECRET_KEY='development key' 

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

UPLOADED_SCREENSHOTS_DEST = 'media'

REMEMBER_COOKIE_DURATION = timedelta(days=7)
from getItTogether import db

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    password = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)    
    
    def __repr__(self):
        return '<User %r>' % (self.username)
        
class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(140))
    text = db.Column(db.String(512))
    points = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.title)        
        
class Screenshot(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    filename = db.Column(db.String(128))
    postId = db.Column(db.Integer, db.ForeignKey('post.id'))
    
    def __repr__(self):
        return '<Screenshot %r>' % (self.id)
        
class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    note = db.Column(db.String(1024))
    postId = db.Column(db.Integer, db.ForeignKey('post.id'))    
    
    def __repr__(self):
        return '<Note %r>' % (self.id)
        
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    comment = db.Column(db.String(1024))
    parent = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)    
    postId = db.Column(db.Integer, db.ForeignKey('post.id'))
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    
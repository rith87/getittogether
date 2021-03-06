from flask.ext.wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import Required

class LoginForm(Form):
    username = TextField('username', validators = [Required()])
    password = TextField('password', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)
    
class RegistrationForm(Form):
    username = TextField('username', validators = [Required()])
    password = TextField('password', validators = [Required()])
    confirm_password = TextField('confirm_password', validators = [Required()])
    email = TextField('email', validators = [Required()])
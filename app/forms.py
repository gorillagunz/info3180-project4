from flask_wtf import Form
from wtforms import TextField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import Required


class LoginForm(Form):
    username = TextField('username', validators=[Required()])
    password = PasswordField('password', [Required()])
    remember_me = BooleanField("remember_me", [Required()])
    
class WishlistForm(Form):
    title = TextField('username', validators=[Required()])
    desc = TextAreaField('desc', [Required()])
    is_private = BooleanField("private", [])
    
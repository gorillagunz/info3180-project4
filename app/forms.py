from flask_wtf import Form
from wtforms import TextField, TextAreaField, PasswordField, BooleanField, SelectField, SubmitField
from wtforms.validators import Required


class LoginForm(Form):
    email = TextField('email', validators=[Required()])
    password = PasswordField('password', [Required()])
    remember_me = BooleanField("remember_me", [])
    submit = SubmitField('submit', [])

class SignUpForm(Form):
    name = TextField('name', validators=[Required()])
    email = TextField('email', validators=[Required()])
    password = PasswordField('password', [Required()])
    remember_me = BooleanField("remember_me", [])

class WishlistForm(Form):
    title = TextField('username', validators=[Required()])
    desc = TextAreaField('desc', [Required()])
    is_private = BooleanField("private", [])
    
class ItemForm(Form):
    url = TextField('title', validators=[Required()])
    title = TextField('title', validators=[Required()])
    desc = TextAreaField('desc', [Required()])
    img = TextField('img', validators=[Required()])
    
    
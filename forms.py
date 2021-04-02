from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired

class UserForm(FlaskForm):
    """User Registration Form"""
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired()])
    firstname = StringField("First Name", validators=[InputRequired()])
    lastname = StringField("Last Name", validators=[InputRequired()])

class LoginForm(FlaskForm):
    """Login Form"""
    username = StringField("Username",validators=[InputRequired()])
    password = PasswordField("Password",validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    """Feedback Form"""
    title = StringField("Title",validators=[InputRequired()])
    content = StringField("Content",validators=[InputRequired()])

class DeleteForm(FlaskForm):
    """Delete Form """

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Optional, Email, Length

class RegistrationForm(FlaskForm):
    '''form for registering'''
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=20,message='Username must be between 1 and 20')])
    password = PasswordField('Password', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email(), Length(min=1, max=50,message='Email must be between 1 and 50')])
    first_name = StringField('First Name', validators=[InputRequired(), Length(min=1, max=20,message='First name must be no longer than 30 characters')])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(min=1, max=20,message='Last name must be no longer than 30 characters')])

class LoginForm(FlaskForm):
    '''form for logging in'''
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=20)],)
    password = PasswordField('Password', validators=[InputRequired(), Length(min=1, max=55)])

class FeedbackForm(FlaskForm):
    '''form for submitting feedback'''
    title = StringField('Feedback Title',validators=[InputRequired(), Length(min=1, max=100)])
    content = StringField('Feedback Content',validators=[InputRequired(), Length(min=1, max=100)])
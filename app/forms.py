from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_repeat = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password')])
    button = SubmitField('Enter')


class PostCreateForm(FlaskForm):
    text = StringField('Username', validators=[DataRequired()])
    button = SubmitField('Enter')


class CommentForm(FlaskForm):
    text = StringField('Comment', validators=[DataRequired()])
    button = SubmitField('Enter')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remebmer Me')
    button = SubmitField('Enter')

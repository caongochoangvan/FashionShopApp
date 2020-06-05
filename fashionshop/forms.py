from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from fashionshop.models import User
from flask_login import current_user
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min = 2, max = 20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('This user is existed. Please change username !')
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('Hey! This email is taken. Please change the email!')
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
class InforForm(FlaskForm):
    name = StringField('Name', validators = [DataRequired()])
    address = StringField('Address', validators = [DataRequired()])
    # country = StringField('Country', validators = [DataRequired()])
    city = StringField('City', validators = [DataRequired()])
    postcode = StringField('Postcode', validators = [DataRequired()])
    phone = StringField('Phone', validators = [DataRequired()])
# class ContactForm(FlaskForm):
#     firstname = StringField('First Name', validators=[DataRequired(), Length(min = 2, max = 20)])
#     lastname = StringField('Last Name', validators=[DataRequired(), Length(min = 2, max = 20)])
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     subject = StringField('Subject', validators=[DataRequired(), Length(min = 2, max = 20)])
#     message = StringField('Message', validators=[DataRequired(), Length(min = 2, max = 100)])
    
#     submit = SubmitField('Send Message')

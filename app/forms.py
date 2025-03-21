from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, FloatField, IntegerField, DateField, TimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models.client import Client

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_email(self, email):
        client = Client.query.filter_by(email=email.data).first()
        if client:
            raise ValidationError('That email is already registered. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class BookingForm(FlaskForm):
    service = SelectField('Service', coerce=int, validators=[DataRequired()])
    stylist = SelectField('Stylist', coerce=int, validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()])
    time = StringField('Time', validators=[DataRequired()])
    notes = TextAreaField('Notes')
    submit = SubmitField('Book Appointment')

class ServiceForm(FlaskForm):
    name = StringField('Service Name', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description')
    price = FloatField('Price', validators=[DataRequired()])
    duration = IntegerField('Duration (minutes)', validators=[DataRequired()])
    submit = SubmitField('Add Service')

class StylistForm(FlaskForm):
    name = StringField('Stylist Name', validators=[DataRequired(), Length(min=2, max=100)])
    bio = TextAreaField('Bio')
    specialization = StringField('Specialization', validators=[Length(max=100)])
    submit = SubmitField('Add Stylist') 
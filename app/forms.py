from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, FloatField, IntegerField, DateField, TimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
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
    experience_years = IntegerField('Years of Experience', validators=[Optional()])
    email = StringField('Email', validators=[Optional(), Email()])
    phone = StringField('Phone', validators=[Optional()])
    instagram = StringField('Instagram Handle', validators=[Optional()])
    is_active = BooleanField('Active', default=True)
    image = FileField('Profile Image', validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Add Stylist')

class AppointmentStatusForm(FlaskForm):
    status = SelectField('Status', choices=[
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no-show', 'No-Show')
    ], validators=[DataRequired()])
    submit = SubmitField('Update Status')

class AppointmentSearchForm(FlaskForm):
    start_date = StringField('Start Date', validators=[DataRequired()])
    end_date = StringField('End Date', validators=[DataRequired()])
    stylist = SelectField('Stylist', coerce=int, validators=[Optional()], default='')
    status = SelectField('Status', choices=[
        ('', 'All Statuses'),
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no-show', 'No-Show')
    ], default='')
    submit = SubmitField('Search') 
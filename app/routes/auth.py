from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from app import db
from app.models.client import Client
from app.forms import RegistrationForm, LoginForm

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            client = Client.create(
                name=form.name.data,
                email=form.email.data,
                password=form.password.data
            )
            flash('Your account has been created! You can now log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')
    
    return render_template('auth/register.html', title='Register', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        client = Client.query.filter_by(email=form.email.data).first()
        if client and client.check_password(form.password.data):
            login_user(client, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    
    return render_template('auth/login.html', title='Login', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home')) 
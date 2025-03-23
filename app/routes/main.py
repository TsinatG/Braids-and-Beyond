from flask import Blueprint, render_template, redirect, url_for

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    return render_template('index.html', title='Home')

@main.route('/about')
def about():
    return render_template('about.html', title='About Us')

@main.route('/services')
def services():
    return redirect(url_for('services.list_services'))

@main.route('/contact')
def contact():
    """Display the contact page"""
    return render_template('contact.html', title='Contact Us')

@main.route('/stylists')
def stylists():
    return redirect(url_for('stylists.list_stylists')) 
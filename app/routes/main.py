from flask import Blueprint, render_template

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
    return render_template('services.html', title='Our Services')

@main.route('/contact')
def contact():
    return render_template('contact.html', title='Contact Us') 
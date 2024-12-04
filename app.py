#comments
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from utils import (
     delete_appointment, delete_service, delete_stylist, read_csv, write_csv, get_available_times, get_services, get_stylists,
    book_appointment, get_appointments, update_appointment,
    add_service, update_service,
    add_stylist, update_stylist
)
import csv


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'fallback_secret_key') # Change this to a secure random key


USER_FILE = os.path.join(os.path.dirname(__file__), 'data', 'users.csv')

def read_users():
    users = {}
    if os.path.exists(USER_FILE):
        with open(USER_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                users[row['email']] = {'username': row['username'], 'password': row['password']}
    return users


def write_user(email, username, password):
    file_exists = os.path.exists(USER_FILE)
    with open(USER_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['email', 'username', 'password'])  # Add headers if file is new
        writer.writerow([email, username, password])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('register'))
        
        users = read_users()
        if email in users:
            flash('User already exists!', 'error')
            return redirect(url_for('register'))
        
        write_user(email, username, password)  # Store plain password
        flash('User registered successfully!', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = read_users()

        # Search by username and verify plain password
        for user_email, user_data in users.items():
            if user_data['username'] == username and user_data['password'] == password:
                session['username'] = username
                flash('Logged in successfully!', 'success')
                return redirect(url_for('index'))

        flash('Invalid credentials!', 'error')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/book', methods=['GET', 'POST'])
def book_appointment_route():
    if 'username' not in session:
        flash('Please log in to book an appointment', 'error')
        return redirect(url_for('login'))
       
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        service_id = request.form['service_id']
        stylist_id = request.form['stylist_id']
        date = request.form['date']
        time = request.form['time']
        
        appointment_id = book_appointment(customer_name, service_id, stylist_id, date, time)
        flash('Appointment booked successfully!', 'success')
        return redirect(url_for('index'))
    services = get_services()
    stylists = get_stylists()
    return render_template('book_appointment.html', services=services, stylists=stylists)

@app.route('/appointments', methods=['GET', 'POST'])
def manage_appointments():

    search_query = request.form.get('search', '')

    appointments = get_appointments()
    services = {service['id']: service['name'] for service in get_services()}
    stylists = {stylist['id']: stylist['name'] for stylist in get_stylists()}

    if search_query:
        appointments = [appt for appt in appointments if search_query.lower() in appt['customer_name'].lower()]

    return render_template('manage_appointments.html', appointments=appointments, services=services, stylists=stylists, search_query=search_query)

@app.route('/appointments/edit/<appointment_id>', methods=['GET', 'POST'])
def edit_appointment(appointment_id):
    
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        service_id = request.form['service_id']
        stylist_id = request.form['stylist_id']
        date = request.form['date']
        time = request.form['time']
        
        update_appointment(appointment_id, customer_name, service_id, stylist_id, date, time)
        flash('Appointment updated successfully!', 'success')
        return redirect(url_for('manage_appointments'))
    
    appointment = next((appt for appt in get_appointments() if appt['id'] == appointment_id), None)
    if not appointment:
        flash('Appointment not found', 'error')
        return redirect(url_for('manage_appointments'))
    
    services = get_services()
    stylists = get_stylists()
    return render_template('edit_appointment.html', appointment=appointment, services=services, stylists=stylists)

@app.route('/appointments/delete/<appointment_id>', methods=['POST'])
def delete_appointment_route(appointment_id):
    
    delete_appointment(appointment_id)
    flash('Appointment deleted successfully!', 'success')
    return redirect(url_for('manage_appointments'))

@app.route('/available_times')
def available_times():
    date = request.args.get('date')
    stylist_id = request.args.get('stylist_id')
    times = get_available_times(date, stylist_id)
    return {'times': times}

@app.route('/services', methods=['GET', 'POST'])
def manage_services():
    
    search_query = request.form.get('search', '')

    if request.method == 'POST' and 'name' in request.form:
        name = request.form['name']
        duration = request.form['duration']
        price = request.form['price']
        add_service(name, duration, price)
        flash('Service added successfully!', 'success')
        return redirect(url_for('manage_services'))
    
    services = get_services()
    if search_query:
        services = [service for service in services if search_query.lower() in service['name'].lower()]
    
    return render_template('manage_services.html', services=services, search_query=search_query)

@app.route('/services/edit/<service_id>', methods=['GET', 'POST'])
def edit_service(service_id):
    
    if request.method == 'POST':
        name = request.form['name']
        duration = request.form['duration']
        price = request.form['price']
        update_service(service_id, name, duration, price)
        flash('Service updated successfully!', 'success')
        return redirect(url_for('manage_services'))
    
    service = next((s for s in get_services() if s['id'] == service_id), None)
    if not service:
        flash('Service not found', 'error')
        return redirect(url_for('manage_services'))
    
    return render_template('edit_service.html', service=service)

@app.route('/services/delete/<service_id>', methods=['POST'])
def delete_service_route(service_id):
    
    delete_service(service_id)
    flash('Service deleted successfully!', 'success')
    return redirect(url_for('manage_services'))


@app.route('/stylists', methods=['GET', 'POST'])
def manage_stylists():
    
    search_query = request.form.get('search', '')

    if request.method == 'POST' and 'name' in request.form:
        name = request.form['name']
        specialization = request.form['specialization']
        add_stylist(name, specialization)
        flash('Stylist added successfully!', 'success')
        return redirect(url_for('manage_stylists'))
    
    stylists = get_stylists()
    if search_query:
        stylists = [stylist for stylist in stylists if search_query.lower() in stylist['name'].lower()]
    
    return render_template('manage_stylists.html', stylists=stylists, search_query=search_query)


@app.route('/stylists/edit/<stylist_id>', methods=['GET', 'POST'])
def edit_stylist(stylist_id):
    
    if request.method == 'POST':
        name = request.form['name']
        specialization = request.form['specialization']
        update_stylist(stylist_id, name, specialization)
        flash('Stylist updated successfully!', 'success')
        return redirect(url_for('manage_stylists'))
    
    stylist = next((s for s in get_stylists() if s['id'] == stylist_id), None)
    if not stylist:
        flash('Stylist not found', 'error')
        return redirect(url_for('manage_stylists'))
    
    return render_template('edit_stylist.html', stylist=stylist)

@app.route('/stylists/delete/<stylist_id>', methods=['POST'])
def delete_stylist_route(stylist_id):
    
    delete_stylist(stylist_id)
    flash('Stylist deleted successfully!', 'success')
    return redirect(url_for('manage_stylists'))

if __name__ == '__main__':
    app.run(debug=True)


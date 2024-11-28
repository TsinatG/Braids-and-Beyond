import os
from flask import Flask, render_template, request, redirect, url_for, flash
from utils import (
    delete_appointment, read_csv, write_csv, get_available_times, get_services, get_stylists, get_available_times, 
    book_appointment, get_appointments, update_appointment,

)
import csv


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'fallback_secret_key') # Change this to a secure random key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/book', methods=['GET', 'POST'])
def book_appointment_route():
       
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

@app.route('/appointments')
def manage_appointments():
    
    appointments = get_appointments()
    services = {service['id']: service['name'] for service in get_services()}
    stylists = {stylist['id']: stylist['name'] for stylist in get_stylists()}
    return render_template('manage_appointments.html', appointments=appointments, services=services, stylists=stylists)

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

if __name__ == '__main__':
    app.run(debug=True)


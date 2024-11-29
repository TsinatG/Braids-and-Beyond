#comments
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from utils import (
    delete_appointment, read_csv, write_csv, get_available_times, get_services, get_stylists, get_available_times, 
    book_appointment, get_appointments, update_appointment, add_service, update_service, delete_service, add_stylist, update_stylist, delete_stylist

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

@app.route('/services', methods=['GET', 'POST'])
def manage_services():
    
    if request.method == 'POST':
        name = request.form['name']
        duration = request.form['duration']
        price = request.form['price']
        add_service(name, duration, price)
        flash('Service added successfully!', 'success')
        return redirect(url_for('manage_services'))
    
    services = get_services()
    return render_template('manage_services.html', services=services)

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
    
    delete_service, add_stylist(service_id)
    flash('Service deleted successfully!', 'success')
    return redirect(url_for('manage_services'))

@app.route('/stylists', methods=['GET', 'POST'])
def manage_stylists():
    
    if request.method == 'POST':
        name = request.form['name']
        specialization = request.form['specialization']
        add_stylist(name, specialization)
        flash('Stylist added successfully!', 'success')
        return redirect(url_for('manage_stylists'))
    
    stylists = get_stylists()
    return render_template('manage_stylists.html', stylists=stylists)

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


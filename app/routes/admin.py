from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user
from app import db
from app.models.appointment import Appointment
from app.models.client import Client
from app.models.service import Service
from app.models.stylist import Stylist
from app.forms import ServiceForm, StylistForm
from datetime import datetime

admin = Blueprint('admin', __name__)

# Admin access decorator
def admin_required(f):
    @login_required
    def decorated_function(*args, **kwargs):
        # For simplicity, we're checking if user ID is 1 (first user is admin)
        # In a real app, you'd have a proper admin role system
        if current_user.id != 1:
            flash('You do not have permission to access this page.', 'error')
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@admin.route('/admin/dashboard')
@admin_required
def dashboard():
    # Get counts for dashboard
    appointment_count = Appointment.query.count()
    client_count = Client.query.count()
    service_count = Service.query.count()
    stylist_count = Stylist.query.count()
    
    # Get upcoming appointments
    upcoming_appointments = Appointment.query.filter(
        Appointment.date >= datetime.now().date()
    ).order_by(Appointment.date, Appointment.time).limit(5).all()
    
    return render_template('admin/dashboard.html', title='Admin Dashboard',
                          appointment_count=appointment_count,
                          client_count=client_count,
                          service_count=service_count,
                          stylist_count=stylist_count,
                          upcoming_appointments=upcoming_appointments)

@admin.route('/admin/appointments')
@admin_required
def appointments():
    appointments = Appointment.query.order_by(Appointment.date.desc()).all()
    return render_template('admin/appointments.html', title='Manage Appointments', 
                          appointments=appointments)

@admin.route('/admin/clients')
@admin_required
def clients():
    clients = Client.query.all()
    return render_template('admin/clients.html', title='Manage Clients', 
                          clients=clients)

@admin.route('/admin/services', methods=['GET', 'POST'])
@admin_required
def services():
    form = ServiceForm()
    if form.validate_on_submit():
        service = Service(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            duration=form.duration.data
        )
        db.session.add(service)
        db.session.commit()
        flash('Service has been added!', 'success')
        return redirect(url_for('admin.services'))
    
    services = Service.query.all()
    return render_template('admin/services.html', title='Manage Services', 
                          services=services, form=form)

@admin.route('/admin/stylists', methods=['GET', 'POST'])
@admin_required
def stylists():
    form = StylistForm()
    if form.validate_on_submit():
        stylist = Stylist(
            name=form.name.data,
            bio=form.bio.data,
            specialization=form.specialization.data
        )
        db.session.add(stylist)
        db.session.commit()
        flash('Stylist has been added!', 'success')
        return redirect(url_for('admin.stylists'))
    
    stylists = Stylist.query.all()
    return render_template('admin/stylists.html', title='Manage Stylists', 
                          stylists=stylists, form=form) 
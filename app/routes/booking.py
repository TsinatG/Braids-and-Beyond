from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user
from app import db
from app.models.appointment import Appointment
from app.models.service import Service
from app.models.stylist import Stylist
from app.forms import BookingForm
from datetime import datetime

booking = Blueprint('booking', __name__)

@booking.route('/booking/calendar')
def calendar():
    stylists = Stylist.query.all()
    services = Service.query.all()
    return render_template('booking/calendar.html', title='Book Appointment', 
                           stylists=stylists, services=services)

@booking.route('/booking/form', methods=['GET', 'POST'])
@login_required
def form():
    form = BookingForm()
    
    # Populate form choices
    form.service.choices = [(s.id, f"{s.name} - ${s.price} ({s.duration} mins)") 
                            for s in Service.query.all()]
    form.stylist.choices = [(s.id, s.name) for s in Stylist.query.all()]
    
    if form.validate_on_submit():
        # Convert form date and time to Python objects
        date_obj = datetime.strptime(form.date.data, '%Y-%m-%d').date()
        time_obj = datetime.strptime(form.time.data, '%H:%M').time()
        
        # Get service duration
        service = Service.query.get(form.service.data)
        
        appointment = Appointment(
            date=date_obj,
            time=time_obj,
            duration=service.duration,
            notes=form.notes.data,
            client_id=current_user.id,
            stylist_id=form.stylist.data,
            service_id=form.service.data
        )
        
        db.session.add(appointment)
        db.session.commit()
        
        flash('Your appointment has been booked!', 'success')
        return redirect(url_for('main.home'))
    
    return render_template('booking/form.html', title='Book Appointment', form=form)

@booking.route('/booking/appointments')
@login_required
def appointments():
    appointments = Appointment.query.filter_by(client_id=current_user.id).order_by(Appointment.date).all()
    return render_template('booking/appointments.html', title='My Appointments', appointments=appointments) 
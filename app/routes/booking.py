from flask import Blueprint, render_template, url_for, flash, redirect, request, jsonify, current_app
from flask_login import login_required, current_user
from app import db
from app.models.appointment import Appointment
from app.models.service import Service
from app.models.stylist import Stylist
from app.models.client import Client
from app.forms import BookingForm, AppointmentStatusForm, AppointmentSearchForm
from datetime import datetime, timedelta, time
import json
import calendar as cal

booking = Blueprint('booking', __name__)

@booking.route('/booking/calendar')
def calendar():
    """Display the booking calendar to select a date"""
    # Get active services and stylists for the booking form
    active_services = Service.get_active_services()
    active_stylists = Stylist.get_active_stylists()
    
    # Create a form for CSRF protection
    form = BookingForm()
    form.service.choices = [(s.id, s.name) for s in active_services]
    form.stylist.choices = [(s.id, s.name) for s in active_stylists]
    
    return render_template('booking/calendar.html', 
                          title='Book Appointment',
                          services=active_services,
                          stylists=active_stylists,
                          form=form)

@booking.route('/booking/availability', methods=['POST'])
def check_availability():
    """AJAX endpoint to check stylist availability for a specific date"""
    data = request.get_json()
    
    if not data or 'date' not in data or 'stylist_id' not in data:
        return jsonify({'error': 'Invalid request data'}), 400
    
    try:
        selected_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        stylist_id = int(data['stylist_id'])
        
        # Get all appointments for this stylist on the selected date
        booked_slots = Appointment.get_stylist_availability(stylist_id, selected_date)
        
        # Convert time objects to strings for JSON serialization
        booked_slots_str = [slot.strftime('%H:%M') for slot in booked_slots]
        
        return jsonify({
            'success': True,
            'booked_slots': booked_slots_str
        })
    except Exception as e:
        current_app.logger.error(f"Error checking availability: {str(e)}")
        return jsonify({'error': 'An error occurred while checking availability'}), 500

@booking.route('/booking/form', methods=['GET', 'POST'])
@login_required
def form():
    """Display and process the booking form"""
    form = BookingForm()
    
    # Populate form choices
    active_services = Service.get_active_services()
    active_stylists = Stylist.get_active_stylists()
    
    form.service.choices = [(s.id, f"{s.name} - ${s.price} ({s.duration} mins)") 
                            for s in active_services]
    form.stylist.choices = [(s.id, s.name) for s in active_stylists]
    
    if form.validate_on_submit():
        try:
            # Convert form date and time to Python objects
            date_obj = datetime.strptime(form.date.data, '%Y-%m-%d').date()
            time_obj = datetime.strptime(form.time.data, '%H:%M').time()
            
            # Get service duration
            service = Service.query.get(form.service.data)
            
            # Check if the appointment time is in the past
            appointment_datetime = datetime.combine(date_obj, time_obj)
            if appointment_datetime < datetime.now():
                flash('Cannot book appointments in the past.', 'danger')
                return render_template('booking/form.html', title='Book Appointment', form=form)
            
            # The current user is the client - use current_user.id directly
            # No need to query for client by user_id since the Client model is the user
            
            # Create new appointment
            new_appointment = Appointment(
                client_id=current_user.id,
                service_id=form.service.data,
                stylist_id=form.stylist.data,
                date=date_obj,
                time=time_obj,
                duration=service.duration,
                notes=form.notes.data
            )
            
            db.session.add(new_appointment)
            db.session.commit()
            
            # Redirect to confirmation page
            return redirect(url_for('booking.confirmation', appointment_id=new_appointment.id))
            
        except Exception as e:
            current_app.logger.error(f"Error booking appointment: {str(e)}")
            flash('An error occurred while booking your appointment. Please try again.', 'danger')
    
    return render_template('booking/form.html', title='Book Appointment', form=form)

@booking.route('/appointments')
@login_required
def appointments():
    """Display the current user's appointments"""
    # The current user is the client
    client_id = current_user.id
    
    # Get upcoming and past appointments
    today = datetime.now().date()
    
    upcoming_appointments = Appointment.query.filter_by(client_id=client_id).filter(
        Appointment.date >= today
    ).order_by(Appointment.date, Appointment.time).all()
    
    past_appointments = Appointment.query.filter_by(client_id=client_id).filter(
        Appointment.date < today
    ).order_by(Appointment.date.desc(), Appointment.time.desc()).limit(5).all()
    
    return render_template('booking/my_appointments.html',
                          title='My Appointments',
                          upcoming_appointments=upcoming_appointments,
                          past_appointments=past_appointments)

@booking.route('/booking/appointments/<int:appointment_id>')
@login_required
def appointment_detail(appointment_id):
    """Display details for a specific appointment"""
    appointment = Appointment.query.get_or_404(appointment_id)
    
    # Check if the appointment belongs to the current user or if user is admin
    if appointment.client_id != current_user.id and current_user.id != 1:
        flash('You do not have permission to view this appointment.', 'danger')
        return redirect(url_for('booking.appointments'))
    
    return render_template('booking/appointment_detail.html', 
                          title='Appointment Details',
                          appointment=appointment)

@booking.route('/booking/appointments/<int:appointment_id>/cancel', methods=['POST'])
@login_required
def cancel_appointment(appointment_id):
    """Cancel a user's appointment"""
    appointment = Appointment.query.get_or_404(appointment_id)
    
    # Check if this appointment belongs to the current user
    if appointment.client_id != current_user.id and current_user.id != 1:
        flash('You do not have permission to cancel this appointment.', 'danger')
        return redirect(url_for('booking.appointments'))
    
    # Check if the appointment is in the future and currently scheduled
    if appointment.is_past:
        flash('Cannot cancel past appointments.', 'danger')
        return redirect(url_for('booking.appointments'))
    
    if appointment.status != 'scheduled':
        flash('This appointment has already been ' + appointment.status + '.', 'warning')
        return redirect(url_for('booking.appointments'))
    
    # Cancel the appointment
    appointment.status = 'cancelled'
    db.session.commit()
    
    flash('Your appointment has been cancelled.', 'success')
    return redirect(url_for('booking.appointments'))

@booking.route('/admin/appointments')
@login_required
def admin_appointments():
    """Admin page to view and manage all appointments"""
    # Check if user is admin
    if current_user.id != 1:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.home'))
    
    form = AppointmentSearchForm()
    
    # Populate stylist choices
    form.stylist.choices = [(0, 'All Stylists')] + [(s.id, s.name) for s in Stylist.query.all()]
    
    # Default to showing today's appointments
    today = datetime.now().date()
    appointments = Appointment.get_appointments_by_date(today)
    
    return render_template('admin/appointments.html', 
                          title='Manage Appointments',
                          appointments=appointments,
                          form=form,
                          current_date=today.strftime('%Y-%m-%d'))

@booking.route('/admin/appointments/search', methods=['POST'])
@login_required
def search_appointments():
    """Search appointments based on criteria"""
    # Check if user is admin
    if current_user.id != 1:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.home'))
    
    form = AppointmentSearchForm()
    
    # Populate stylist choices
    form.stylist.choices = [(0, 'All Stylists')] + [(s.id, s.name) for s in Stylist.query.all()]
    
    if form.validate_on_submit():
        try:
            start_date = datetime.strptime(form.start_date.data, '%Y-%m-%d').date()
            end_date = datetime.strptime(form.end_date.data, '%Y-%m-%d').date()
            
            # Base query
            query = Appointment.query.filter(Appointment.date.between(start_date, end_date))
            
            # Add stylist filter if selected
            if form.stylist.data != 0:
                query = query.filter_by(stylist_id=form.stylist.data)
            
            # Add status filter if selected
            if form.status.data:
                query = query.filter_by(status=form.status.data)
            
            # Order by date and time
            appointments = query.order_by(Appointment.date, Appointment.time).all()
            
            return render_template('admin/appointments.html', 
                                  title='Appointment Search Results',
                                  appointments=appointments,
                                  form=form,
                                  search_mode=True)
        
        except Exception as e:
            current_app.logger.error(f"Error searching appointments: {str(e)}")
            flash('An error occurred while searching appointments. Please try again.', 'danger')
    
    # If form validation fails, show today's appointments
    today = datetime.now().date()
    appointments = Appointment.get_appointments_by_date(today)
    
    return render_template('admin/appointments.html', 
                          title='Manage Appointments',
                          appointments=appointments,
                          form=form,
                          current_date=today.strftime('%Y-%m-%d'))

@booking.route('/admin/appointments/<int:appointment_id>/status', methods=['POST'])
@login_required
def update_appointment_status(appointment_id):
    """Update the status of an appointment"""
    # Check if user is admin
    if current_user.id != 1:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.home'))
    
    appointment = Appointment.query.get_or_404(appointment_id)
    form = AppointmentStatusForm()
    
    if form.validate_on_submit():
        appointment.status = form.status.data
        db.session.commit()
        flash('Appointment status has been updated.', 'success')
    
    return redirect(request.referrer or url_for('booking.admin_appointments'))

@booking.route('/admin/calendar')
@login_required
def admin_calendar():
    """Admin calendar view of all appointments"""
    # Check if user is admin
    if current_user.id != 1:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.home'))
    
    # Get all stylists for filtering
    stylists = Stylist.query.all()
    
    # Get the current month's appointments
    today = datetime.now()
    first_day = datetime(today.year, today.month, 1)
    last_day = datetime(today.year, today.month, cal.monthrange(today.year, today.month)[1])
    
    appointments = Appointment.query.filter(
        Appointment.date.between(first_day.date(), last_day.date())
    ).all()
    
    # Format appointments for the calendar
    calendar_data = []
    for appointment in appointments:
        calendar_data.append({
            'id': appointment.id,
            'title': f"{appointment.client.name} - {appointment.service.name}",
            'start': f"{appointment.date.isoformat()}T{appointment.time.isoformat()}",
            'end': f"{appointment.date.isoformat()}T{appointment.end_time.isoformat()}",
            'stylist': appointment.stylist.name,
            'stylist_id': appointment.stylist.id,
            'status': appointment.status,
            'className': f"appointment-{appointment.status}"
        })
    
    # Create a form for CSRF protection
    form = AppointmentStatusForm()
    
    return render_template('admin/calendar.html', 
                          title='Appointment Calendar',
                          stylists=stylists,
                          form=form,
                          calendar_data=json.dumps(calendar_data))

@booking.route('/admin/appointments/<int:appointment_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_appointment(appointment_id):
    """Edit an existing appointment (admin only)"""
    # Check if user is admin
    if current_user.id != 1:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.home'))
    
    appointment = Appointment.query.get_or_404(appointment_id)
    form = BookingForm()
    
    # Populate form choices
    active_services = Service.get_active_services()
    active_stylists = Stylist.get_active_stylists()
    
    form.service.choices = [(s.id, f"{s.name} - ${s.price} ({s.duration} mins)") 
                            for s in active_services]
    form.stylist.choices = [(s.id, s.name) for s in active_stylists]
    
    if form.validate_on_submit():
        try:
            # Convert form date and time to Python objects
            date_obj = datetime.strptime(form.date.data, '%Y-%m-%d').date()
            time_obj = datetime.strptime(form.time.data, '%H:%M').time()
            
            # Get service duration
            service = Service.query.get(form.service.data)
            
            # Update appointment
            appointment.service_id = form.service.data
            appointment.stylist_id = form.stylist.data
            appointment.date = date_obj
            appointment.time = time_obj
            appointment.duration = service.duration
            appointment.notes = form.notes.data
            
            db.session.commit()
            flash('Appointment has been updated!', 'success')
            return redirect(url_for('booking.admin_appointments'))
            
        except Exception as e:
            current_app.logger.error(f"Error updating appointment: {str(e)}")
            flash('An error occurred while updating the appointment. Please try again.', 'danger')
    
    # Pre-populate form with existing appointment data
    elif request.method == 'GET':
        form.service.data = appointment.service_id
        form.stylist.data = appointment.stylist_id
        form.date.data = appointment.date.strftime('%Y-%m-%d')
        form.time.data = appointment.time.strftime('%H:%M')
        form.notes.data = appointment.notes
    
    return render_template('booking/form.html', 
                          title='Edit Appointment',
                          form=form,
                          edit_mode=True,
                          appointment=appointment)

@booking.route('/admin/appointments/<int:appointment_id>/delete', methods=['POST'])
@login_required
def delete_appointment(appointment_id):
    """Delete an appointment (admin only)"""
    # Check if user is admin
    if current_user.id != 1:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.home'))
    
    appointment = Appointment.query.get_or_404(appointment_id)
    
    db.session.delete(appointment)
    db.session.commit()
    
    flash('Appointment has been deleted!', 'success')
    return redirect(url_for('booking.admin_appointments'))

@booking.route('/booking/confirmation/<int:appointment_id>')
@login_required
def confirmation(appointment_id):
    """Display a confirmation page after successful booking"""
    appointment = Appointment.query.get_or_404(appointment_id)
    
    # Check if this appointment belongs to the current user
    # The current user is the client, so we don't need to query by user_id
    if appointment.client_id != current_user.id:
        flash('You do not have permission to view this confirmation.', 'danger')
        return redirect(url_for('booking.appointments'))
    
    return render_template('booking/confirmation.html',
                          title='Booking Confirmed',
                          appointment=appointment)

@booking.route('/appointments/history')
@login_required
def appointment_history():
    """Display all past appointments for the current user"""
    # The current user is the client, so directly use current_user.id
    
    # Get all past appointments
    today = datetime.now().date()
    
    past_appointments = Appointment.query.filter_by(client_id=current_user.id).filter(
        Appointment.date < today
    ).order_by(Appointment.date.desc(), Appointment.time.desc()).all()
    
    return render_template('booking/history.html',
                          title='Appointment History',
                          past_appointments=past_appointments)

@booking.route('/debug-appointments')
@login_required
def debug_appointments():
    """Debug route to check appointment rendering"""
    # The current user is the client, so directly use current_user.id
    
    # Get upcoming and past appointments
    today = datetime.now().date()
    
    upcoming_appointments = Appointment.query.filter_by(client_id=current_user.id).filter(
        Appointment.date >= today
    ).order_by(Appointment.date, Appointment.time).all()
    
    past_appointments = Appointment.query.filter_by(client_id=current_user.id).filter(
        Appointment.date < today
    ).order_by(Appointment.date.desc(), Appointment.time.desc()).limit(5).all()
    
    # Return debug info
    debug_info = f"""
    <h1>Debug Appointments</h1>
    <p>Client: {current_user.name} (ID: {current_user.id})</p>
    <p>Upcoming Appointments: {len(upcoming_appointments)}</p>
    <p>Past Appointments: {len(past_appointments)}</p>
    <p>Current Template Path: app/templates/booking/appointments.html</p>
    <p>Current Route: booking.appointments</p>
    <hr>
    <h2>Upcoming Appointments:</h2>
    <ul>
    """
    
    for appt in upcoming_appointments:
        debug_info += f"<li>{appt.date} at {appt.time} - {appt.service.name} with {appt.stylist.name}</li>"
    
    debug_info += "</ul>"
    
    return debug_info 
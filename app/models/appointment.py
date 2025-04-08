from datetime import datetime, timedelta
from app import db

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # Duration in minutes
    notes = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='scheduled')  # scheduled, completed, cancelled, no-show
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    stylist_id = db.Column(db.Integer, db.ForeignKey('stylist.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    
    # Relationships
    client = db.relationship('Client', backref=db.backref('appointments', lazy=True))
    stylist = db.relationship('Stylist', backref=db.backref('appointments', lazy=True))
    service = db.relationship('Service', backref=db.backref('appointments', lazy=True))
    
    def __repr__(self):
        return f"Appointment('{self.date}', '{self.time}', '{self.client.name}', '{self.service.name}')"
    
    @property
    def end_time(self):
        """Calculate the end time of the appointment based on duration"""
        start_datetime = datetime.combine(self.date, self.time)
        end_datetime = start_datetime + timedelta(minutes=self.duration)
        return end_datetime.time()
    
    @property
    def is_past(self):
        """Check if the appointment is in the past"""
        now = datetime.now()
        appointment_datetime = datetime.combine(self.date, self.time)
        return appointment_datetime < now
    
    @property
    def is_today(self):
        """Check if the appointment is today"""
        return self.date == datetime.now().date()
    
    @property
    def is_upcoming(self):
        """Check if the appointment is upcoming (today or in the future)"""
        now = datetime.now()
        appointment_datetime = datetime.combine(self.date, self.time)
        return appointment_datetime >= now
    
    @property
    def formatted_date(self):
        """Return a nicely formatted date"""
        return self.date.strftime('%A, %B %d, %Y')
    
    @property
    def formatted_time(self):
        """Return a nicely formatted time"""
        return self.time.strftime('%I:%M %p')
    
    @property
    def formatted_end_time(self):
        """Return a nicely formatted end time"""
        return self.end_time.strftime('%I:%M %p')
    
    @property
    def status_badge_class(self):
        """Return the appropriate CSS class for the status badge"""
        status_classes = {
            'scheduled': 'bg-primary',
            'completed': 'bg-success',
            'cancelled': 'bg-danger',
            'no-show': 'bg-warning text-dark'
        }
        return status_classes.get(self.status, 'bg-secondary')
    
    @staticmethod
    def get_upcoming_appointments():
        """Get all upcoming appointments ordered by date and time"""
        today = datetime.now().date()
        return Appointment.query.filter(Appointment.date >= today).order_by(Appointment.date, Appointment.time).all()
    
    @staticmethod
    def get_appointments_by_date(date):
        """Get all appointments for a specific date"""
        return Appointment.query.filter_by(date=date).order_by(Appointment.time).all()
    
    @staticmethod
    def get_appointments_by_client(client_id):
        """Get all appointments for a specific client"""
        return Appointment.query.filter_by(client_id=client_id).order_by(Appointment.date.desc(), Appointment.time.desc()).all()
    
    @staticmethod
    def get_appointments_by_stylist(stylist_id):
        """Get all appointments for a specific stylist"""
        return Appointment.query.filter_by(stylist_id=stylist_id).order_by(Appointment.date, Appointment.time).all()
    
    @staticmethod
    def get_stylist_availability(stylist_id, date):
        """Get a list of time slots that are already booked for a stylist on a specific date"""
        appointments = Appointment.query.filter_by(stylist_id=stylist_id, date=date).all()
        booked_slots = []
        
        for appointment in appointments:
            start_datetime = datetime.combine(appointment.date, appointment.time)
            end_datetime = start_datetime + timedelta(minutes=appointment.duration)
            
            # Create 15-minute intervals for the duration of the appointment
            current = start_datetime
            while current < end_datetime:
                booked_slots.append(current.time())
                current += timedelta(minutes=15)
        
        return booked_slots 
from datetime import datetime
from app import db

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # Duration in minutes
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign keys
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    stylist_id = db.Column(db.Integer, db.ForeignKey('stylist.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    
    # Relationships
    client = db.relationship('Client', backref=db.backref('appointments', lazy=True))
    stylist = db.relationship('Stylist', backref=db.backref('appointments', lazy=True))
    service = db.relationship('Service', backref=db.backref('appointments', lazy=True))
    
    def __repr__(self):
        return f"Appointment('{self.date}', '{self.time}', Client: '{self.client.name}')" 
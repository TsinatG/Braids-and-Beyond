from app import db
from datetime import datetime

class Stylist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    specialization = db.Column(db.String(200), nullable=True)
    experience_years = db.Column(db.Integer, nullable=True)
    image_file = db.Column(db.String(100), nullable=True, default='default-stylist.jpg')
    email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    instagram = db.Column(db.String(100), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with appointments is defined in the Appointment model
    
    def __repr__(self):
        return f"Stylist('{self.name}', '{self.specialization}')"
    
    @staticmethod
    def get_active_stylists():
        """Return all active stylists ordered by name"""
        return Stylist.query.filter_by(is_active=True).order_by(Stylist.name).all() 
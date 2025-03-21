from app import db
from datetime import datetime

class Stylist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    specialization = db.Column(db.String(100), nullable=True)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with appointments is defined in the Appointment model
    
    def __repr__(self):
        return f"Stylist('{self.name}', '{self.specialization}')" 
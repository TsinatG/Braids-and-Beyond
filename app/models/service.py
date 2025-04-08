from app import db
from datetime import datetime

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # Duration in minutes
    image_file = db.Column(db.String(100), nullable=True, default='default-service.jpg')
    category = db.Column(db.String(50), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with appointments is defined in the Appointment model
    
    def __repr__(self):
        return f"Service('{self.name}', '${self.price}', '{self.duration} mins')"
    
    @staticmethod
    def get_active_services():
        """Return all active services ordered by name"""
        return Service.query.filter_by(is_active=True).order_by(Service.name).all()
    
    @staticmethod
    def get_service_categories():
        """Return all unique service categories"""
        categories = db.session.query(Service.category).distinct().filter(Service.category != None).all()
        return [category[0] for category in categories if category[0]] 
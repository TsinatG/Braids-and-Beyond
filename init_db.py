from app import create_app, db
from app.models.client import Client
from app.models.stylist import Stylist
from app.models.service import Service

app = create_app()

def init_db():
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if we already have data
        if Client.query.count() == 0:
            # Create admin user
            admin = Client.create(
                name="Admin User",
                email="admin@braidsandbeyond.com",
                password="adminpassword"
            )
            print(f"Created admin user: {admin.email}")
        
        if Stylist.query.count() == 0:
            # Create default stylist
            stylist = Stylist(
                name="Tsinat Gezahegne",
                bio="Professional hair stylist with over 7 years of experience specializing in braids and natural hair styling.",
                specialization="Box Braids, Goddess Braids, Faux Locs",
                image_file="stylist.jpg"
            )
            db.session.add(stylist)
            
            print(f"Created stylist: {stylist.name}")
        
        if Service.query.count() == 0:
            # Create default services
            services = [
                Service(name="Box Braids", description="Classic box braids in various sizes.", price=150, duration=180),
                Service(name="Goddess Braids", description="Elegant and sophisticated goddess braids.", price=180, duration=210),
                Service(name="Faux Locs", description="Natural-looking faux locs in various lengths.", price=200, duration=240),
                Service(name="Cornrows", description="Traditional or creative cornrow designs.", price=120, duration=120),
                Service(name="Twist Out", description="Beautiful twist out styles for natural hair.", price=90, duration=90)
            ]
            
            for service in services:
                db.session.add(service)
                print(f"Created service: {service.name}")
        
        # Commit all changes
        db.session.commit()
        print("Database initialized successfully!")

if __name__ == "__main__":
    init_db() 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import Config
import os
from datetime import datetime, timedelta
import sqlite3

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
bcrypt = Bcrypt()

def create_app(config_class=Config):
    app = Flask(__name__, 
                template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'),
                static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'))
    app.config.from_object(config_class)
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    
    # SQLite optimizations and settings
    if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
        def _configure_sqlite(connection, connection_record):
            if isinstance(connection, sqlite3.Connection):
                cursor = connection.cursor()
                # Enable foreign key constraints
                cursor.execute("PRAGMA foreign_keys=ON;")
                
                # Performance optimizations
                cursor.execute("PRAGMA journal_mode=WAL;")  # Write-Ahead Logging for better concurrency
                cursor.execute("PRAGMA synchronous=NORMAL;")  # Reduces disk I/O
                cursor.execute("PRAGMA cache_size=10000;")    # Increase cache size for better performance
                cursor.execute("PRAGMA temp_store=MEMORY;")   # Store temp tables in memory
                cursor.close()
        
        with app.app_context():
            from sqlalchemy import event
            event.listen(db.engine, 'connect', _configure_sqlite)
    
    # Custom Jinja filters
    @app.template_filter('dateadd')
    def dateadd_filter(date, days, unit='days'):
        if isinstance(date, str):
            date = datetime.strptime(date, '%Y-%m-%d').date()
        if unit == 'days':
            return date + timedelta(days=days)
        return date
        
    @app.template_filter('datetime')
    def datetime_filter(date, format='%Y-%m-%d'):
        if isinstance(date, datetime) or hasattr(date, 'strftime'):
            return date.strftime(format)
        return date
    
    # Register blueprints
    from app.routes.main import main
    from app.routes.auth import auth
    from app.routes.booking import booking
    from app.routes.admin import admin
    from app.routes.services import services
    from app.routes.stylists import stylists
    
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(booking)
    app.register_blueprint(admin)
    app.register_blueprint(services)
    app.register_blueprint(stylists)
    
    # Register error handlers
    from app.routes import init_error_handlers
    init_error_handlers(app)
    
    return app

# Import models to ensure they are registered with SQLAlchemy
from app.models import client, stylist, service, appointment 
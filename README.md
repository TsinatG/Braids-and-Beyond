# Braids & Beyond - Hair Styling Website

A web application for a hair salon specializing in braids and natural hair styling, with booking functionality, stylist profiles, and administrative features.

## Features

- **Client-facing features**:
  - Browse salon services and pricing
  - View stylist profiles and specializations
  - Book appointments online
  - Manage existing appointments
  - User registration and authentication

- **Administrative features**:
  - Dashboard with key metrics
  - Appointment management
  - Client management
  - Service management
  - Stylist management

## Technology Stack

- **Backend**: Python, Flask, SQLAlchemy
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Database**: SQLite (lightweight, file-based database)
- **Deployment**: Heroku

## Setup Instructions

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/braids-and-beyond.git
   cd braids-and-beyond
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with the following content:
   ```
   SECRET_KEY=your_secret_key
   FLASK_APP=run.py
   FLASK_ENV=development
   DEBUG=True
   ```

5. Initialize the database:
   ```
   python setup_db.py
   python init_db.py
   ```

6. Run the application:
   ```
   flask run
   ```

7. Access the website at http://localhost:5000

## Database

The application uses SQLite, which stores the database in a single file (`braids_beyond.db`) in the project directory. This makes setup much simpler than a traditional database server:

- No database server installation required
- No user/password configuration needed
- Database file can be easily backed up by copying it
- Perfect for development and small to medium applications

### Database Management

Since SQLite doesn't have a built-in admin panel like phpMyAdmin, we recommend installing DB Browser for SQLite:

#### Installing DB Browser for SQLite:

```bash
# On Ubuntu/Debian
sudo apt-get install sqlitebrowser

# On macOS
brew install --cask db-browser-for-sqlite

# On Windows
# Download from https://sqlitebrowser.org/dl/
```

With DB Browser for SQLite, you can:
- View and edit database tables
- Execute SQL queries
- Create/modify tables and indexes
- Import and export data

### Migrating from MySQL to SQLite

If you are migrating an existing project from MySQL to SQLite, follow these steps:

1. Backup your MySQL database:
   ```
   mysqldump -u username -p braids_beyond_db > backup.sql
   ```

2. Use a tool like [mysql-to-sqlite3](https://github.com/techouse/mysql-to-sqlite3) to convert your data:
   ```
   pip install mysql-to-sqlite3
   mysql2sqlite -f braids_beyond.db -d braids_beyond_db -u username -p password
   ```

3. Alternatively, you can re-initialize the database from scratch using the provided scripts:
   ```
   python setup_db.py
   python init_db.py
   ```

## Admin Access

After initializing the database, you can log in as an admin with:
- Email: admin@braidsandbeyond.com
- Password: adminpassword

## License

This project is licensed under the MIT License.
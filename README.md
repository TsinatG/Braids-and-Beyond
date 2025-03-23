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
- **Database**: MySQL
- **Deployment**: Heroku

## Setup Instructions

### Prerequisites

- Python 3.8+
- MySQL Server
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
   DATABASE_URL=mysql+pymysql://username:password@localhost/braids_beyond_db
   ```
   Replace `username` and `password` with your MySQL credentials.

5. Set up the database:
   ```
   python setup_db.py
   ```

6. Initialize the database with tables and sample data:
   ```
   python init_db.py
   ```

7. Run the application:
   ```
   flask run
   ```

8. Access the website at http://localhost:5000

## Admin Access

After initializing the database, you can log in as an admin with:
- Email: admin@braidsandbeyond.com
- Password: adminpassword

## License

This project is licensed under the MIT License.
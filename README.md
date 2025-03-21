# GLAM Hair Salon Website

A web application for a hair salon with booking functionality, stylist profiles, and administrative features.

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
- **Frontend**: HTML, CSS, JavaScript
- **Database**: MySQL
- **Deployment**: Heroku

## Installation and Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/hair-salon-website.git
   cd hair-salon-website
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Set up environment variables in `.env` file:
   ```
   SECRET_KEY=your_secret_key
   DATABASE_URL=mysql+pymysql://username:password@localhost/hair_salon_db
   FLASK_APP=run.py
   FLASK_ENV=development
   DEBUG=True
   ```

6. Create the MySQL database:
   ```
   mysql -u root -p
   CREATE DATABASE hair_salon_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   CREATE USER 'salon_user'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON hair_salon_db.* TO 'salon_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

7. Initialize the database:
   ```
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

8. Run the application:
   ```
   flask run
   ```

9. Access the application at `http://localhost:5000`

## Project Structure

```
hair_salon_app
├── templates
│   ├── base.html
│   ├── index.html
│   ├── book_appointment.html
│   ├── manage_appointments.html
│   ├── manage_services.html
│   └── manage_stylists.html
├── static
│   └── css
│       └── style.css
├── data
│   ├── appointments.csv
│   ├── services.csv
│   └── stylists.csv
├── app.py
├── utils.py
└── README.md
```

## Unit Tests (optional)
The project includes unit tests to ensure the functionality of the application.

To run the unit tests, navigate to the project directory and execute the following command:
```python
python UnitTest.py
```

This will run all the test cases defined in the `UnitTest.py` file.

## Contributing
Feel free to submit issues or pull requests to improve the application. 

## License
This project is licensed under the MIT License.
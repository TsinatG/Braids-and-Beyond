# Braids and beyond

# GitHub Repository
The source code for this project is available on GitHub: https://github.com/xxyy

## Identification
- **Name:** 
- **P-number:** 
- **Course code:** 

## Declaration of Own Work
I confirm that this assignment is my own work.
Where I have referred to academic sources, I have provided in-text citations and included the sources in the final reference list.

## Introduction
This code represents a simple implementation of a hair salon management system using the Flask library. The application allows users to book appointments, manage services, and view stylists at a hair salon. This project provides a user-friendly interface for both customers and salon staff.

## Installation
To run the application, ensure you have Python installed, and then install the required dependencies from the `requirements.txt` file using the following command:
```bash
pip install -r requirements.txt
```

## How to Use
- Book appointments
- Manage existing appointments
- View and manage services offered by the salon
- View and manage stylists working at the salon

### Running the Application
```python
python app.py
```

### Running Unit Tests
```python
python UnitTest.py
```

## Application Elements
- Appointment booking and management
- Service management
- Stylist management

## Libraries Used
The following libraries are used in this project:
- Flask
- xxyy

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
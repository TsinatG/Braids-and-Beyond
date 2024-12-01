import csv
from datetime import datetime, timedelta

def read_csv(filename):
    with open(f'data/{filename}', 'r') as f:
        return list(csv.DictReader(f))

def write_csv(filename, fieldnames, rows):
    with open(f'data/{filename}', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def get_services():
    return read_csv('services.csv')

def get_stylists():
    stylists = read_csv('stylists.csv')
    for stylist in stylists:
        if 'id' not in stylist:
            stylist['id'] = stylist.get('id', '')  # Use an empty string as default if 'id' is missing
    return stylists

def get_appointments():
    appointments = read_csv('appointments.csv')
    if not appointments:
        print("No appointments found in CSV file.")
    else:
        print(f"Appointments loaded: {appointments}")
    return appointments


def get_available_times(date, stylist_id):
    appointments = get_appointments()
    booked_times = [appt['appointment_time'] for appt in appointments if appt['appointment_date'] == date and appt['stylist_id'] == stylist_id]
    all_times = [f"{hour:02d}:00" for hour in range(9, 18)]
    return [time for time in all_times if time not in booked_times]

def book_appointment(customer_name, service_id, stylist_id, date, time):
    appointments = get_appointments()
    new_id = str(int(max(appt['id'] for appt in appointments)) + 1) if appointments else '1'
    new_appointment = {
        'id': new_id,
        'customer_name': customer_name,
        'service_id': service_id,
        'stylist_id': stylist_id,
        'appointment_date': date,
        'appointment_time': time
    }
    appointments.append(new_appointment)
    write_csv('appointments.csv', new_appointment.keys(), appointments)
    return new_id

def update_appointment(appointment_id, customer_name, service_id, stylist_id, date, time):
    appointments = get_appointments()
    for appt in appointments:
        if appt['id'] == appointment_id:
            appt.update({
                'customer_name': customer_name,
                'service_id': service_id,
                'stylist_id': stylist_id,
                'appointment_date': date,
                'appointment_time': time
            })
            break
    write_csv('appointments.csv', appointments[0].keys(), appointments)

def delete_appointment(appointment_id):
    appointments = get_appointments()
    if not appointments:
        print("Appointments list is empty. Cannot delete.")
        return
    appointments = [appt for appt in appointments if appt['id'] != appointment_id]
    if appointments:
        write_csv('appointments.csv', appointments[0].keys(), appointments)
    else:
        # If no appointments are left, write an empty file with headers
        write_csv('appointments.csv', ['id', 'customer_name', 'service_id', 'stylist_id', 'appointment_date', 'appointment_time'], [])


def add_service(name, duration, price):
    services = get_services()
    new_id = str(int(max(service['id'] for service in services)) + 1) if services else '1'
    new_service = {
        'id': new_id,
        'name': name,
        'duration': duration,
        'price': price
    }
    services.append(new_service)
    write_csv('services.csv', new_service.keys(), services)

def update_service(service_id, name, duration, price):
    services = get_services()
    for service in services:
        if service['id'] == service_id:
            service.update({
                'name': name,
                'duration': duration,
                'price': price
            })
            break
    write_csv('services.csv', services[0].keys(), services)

def delete_service(service_id):
    services = get_services()
    services = [service for service in services if service['id'] != service_id]
    if services:
        write_csv('services.csv', services[0].keys(), services)
    else:
        write_csv('services.csv', ['id', 'name', 'duration', 'price'], [])

def add_stylist(name, specialization):
    stylists = get_stylists()
    new_id = str(int(max(stylist['id'] for stylist in stylists)) + 1) if stylists else '1'
    new_stylist = {
        'id': new_id,
        'name': name,
        'specialization': specialization
    }
    stylists.append(new_stylist)
    write_csv('stylists.csv', new_stylist.keys(), stylists)

def update_stylist(stylist_id, name, specialization):
    stylists = get_stylists()
    for stylist in stylists:
        if stylist['id'] == stylist_id:
            stylist.update({
                'name': name,
                'specialization': specialization
            })
            break
    write_csv('stylists.csv', stylists[0].keys(), stylists)

def delete_stylist(stylist_id):
    stylists = get_stylists()
    stylists = [stylist for stylist in stylists if stylist['id'] != stylist_id]
    if stylists:
        write_csv('stylists.csv', stylists[0].keys(), stylists)
    else:
        write_csv('stylists.csv', ['id', 'name', 'specialization'], [])

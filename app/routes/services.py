from flask import Blueprint, render_template, url_for, flash, redirect, request, current_app
from flask_login import login_required, current_user
from app import db
from app.models.service import Service
from app.forms import ServiceForm
import os
import secrets
from PIL import Image

services = Blueprint('services', __name__)

def save_service_image(form_image):
    """Save the uploaded service image with a random name"""
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    image_filename = random_hex + f_ext
    image_path = os.path.join(current_app.root_path, 'static/img/services', image_filename)
    
    # Resize image to standard size
    output_size = (800, 600)
    i = Image.open(form_image)
    i.thumbnail(output_size)
    i.save(image_path)
    
    return image_filename

@services.route('/services/list')
def list_services():
    """Display all services to customers"""
    categories = Service.get_service_categories()
    services_by_category = {}
    
    for category in categories:
        services_by_category[category] = Service.query.filter_by(
            category=category, is_active=True).order_by(Service.name).all()
    
    # Get services without category
    uncategorized = Service.query.filter_by(
        category=None, is_active=True).order_by(Service.name).all()
    
    if uncategorized:
        services_by_category['Other'] = uncategorized
    
    return render_template('services/list.html', 
                          title='Our Services',
                          categories=categories,
                          services_by_category=services_by_category)

@services.route('/services/<int:service_id>')
def service_detail(service_id):
    """Display details for a specific service"""
    service = Service.query.get_or_404(service_id)
    return render_template('services/detail.html', 
                          title=service.name,
                          service=service)

@services.route('/admin/services', methods=['GET', 'POST'])
@login_required
def manage_services():
    """Admin page to manage services"""
    # Check if user is admin (assuming user with id=1 is admin)
    if current_user.id != 1:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.home'))
    
    form = ServiceForm()
    
    if form.validate_on_submit():
        service = Service(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            duration=form.duration.data,
            category=form.category.data,
            is_active=form.is_active.data
        )
        
        if form.image.data:
            image_file = save_service_image(form.image.data)
            service.image_file = image_file
        
        db.session.add(service)
        db.session.commit()
        flash('Service has been added!', 'success')
        return redirect(url_for('services.manage_services'))
    
    # Get all services for display
    all_services = Service.query.order_by(Service.category, Service.name).all()
    
    return render_template('admin/services.html', 
                          title='Manage Services',
                          form=form,
                          services=all_services)

@services.route('/admin/services/<int:service_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_service(service_id):
    """Edit an existing service"""
    # Check if user is admin
    if current_user.id != 1:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.home'))
    
    service = Service.query.get_or_404(service_id)
    form = ServiceForm()
    
    if form.validate_on_submit():
        service.name = form.name.data
        service.description = form.description.data
        service.price = form.price.data
        service.duration = form.duration.data
        service.category = form.category.data
        service.is_active = form.is_active.data
        
        if form.image.data:
            image_file = save_service_image(form.image.data)
            service.image_file = image_file
        
        db.session.commit()
        flash('Service has been updated!', 'success')
        return redirect(url_for('services.manage_services'))
    
    # Pre-populate form with existing data
    elif request.method == 'GET':
        form.name.data = service.name
        form.description.data = service.description
        form.price.data = service.price
        form.duration.data = service.duration
        form.category.data = service.category or ''
        form.is_active.data = service.is_active
    
    return render_template('admin/edit_service.html', 
                          title='Edit Service',
                          form=form,
                          service=service)

@services.route('/admin/services/<int:service_id>/delete', methods=['POST'])
@login_required
def delete_service(service_id):
    """Delete a service"""
    # Check if user is admin
    if current_user.id != 1:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.home'))
    
    service = Service.query.get_or_404(service_id)
    
    # Check if service has appointments
    if service.appointments and len(service.appointments) > 0:
        flash('Cannot delete service with existing appointments. Mark it as inactive instead.', 'warning')
        return redirect(url_for('services.manage_services'))
    
    db.session.delete(service)
    db.session.commit()
    flash('Service has been deleted!', 'success')
    return redirect(url_for('services.manage_services')) 
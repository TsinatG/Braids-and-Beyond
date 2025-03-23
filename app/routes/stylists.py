from flask import Blueprint, render_template, url_for, flash, redirect, request, current_app
from flask_login import login_required, current_user
from app import db
from app.models.stylist import Stylist
from app.forms import StylistForm
import os
import secrets
from PIL import Image

stylists = Blueprint('stylists', __name__)

def save_stylist_image(form_image):
    """Save the uploaded stylist image with a random name"""
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    image_filename = random_hex + f_ext
    image_path = os.path.join(current_app.root_path, 'static/img/stylists', image_filename)
    
    # Resize image to standard size
    output_size = (500, 500)
    i = Image.open(form_image)
    i.thumbnail(output_size)
    i.save(image_path)
    
    return image_filename

@stylists.route('/stylists')
def list_stylists():
    """Display all stylists to customers"""
    active_stylists = Stylist.get_active_stylists()
    return render_template('stylists/list.html', 
                          title='Our Stylists',
                          stylists=active_stylists)

@stylists.route('/stylists/<int:stylist_id>')
def stylist_detail(stylist_id):
    """Display details for a specific stylist"""
    stylist = Stylist.query.get_or_404(stylist_id)
    return render_template('stylists/detail.html', 
                          title=stylist.name,
                          stylist=stylist)

@stylists.route('/admin/stylists', methods=['GET', 'POST'])
@login_required
def manage_stylists():
    """Admin page to manage stylists"""
    # Check if user is admin (assuming user with id=1 is admin)
    if current_user.id != 1:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.home'))
    
    form = StylistForm()
    
    if form.validate_on_submit():
        stylist = Stylist(
            name=form.name.data,
            bio=form.bio.data,
            specialization=form.specialization.data,
            experience_years=form.experience_years.data,
            email=form.email.data,
            phone=form.phone.data,
            instagram=form.instagram.data,
            is_active=form.is_active.data
        )
        
        if form.image.data:
            image_file = save_stylist_image(form.image.data)
            stylist.image_file = image_file
        
        db.session.add(stylist)
        db.session.commit()
        flash('Stylist has been added!', 'success')
        return redirect(url_for('stylists.manage_stylists'))
    
    # Get all stylists for display
    all_stylists = Stylist.query.order_by(Stylist.name).all()
    
    return render_template('admin/stylists.html', 
                          title='Manage Stylists',
                          form=form,
                          stylists=all_stylists)

@stylists.route('/admin/stylists/<int:stylist_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_stylist(stylist_id):
    """Edit an existing stylist"""
    # Check if user is admin
    if current_user.id != 1:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.home'))
    
    stylist = Stylist.query.get_or_404(stylist_id)
    form = StylistForm()
    
    if form.validate_on_submit():
        stylist.name = form.name.data
        stylist.bio = form.bio.data
        stylist.specialization = form.specialization.data
        stylist.experience_years = form.experience_years.data
        stylist.email = form.email.data
        stylist.phone = form.phone.data
        stylist.instagram = form.instagram.data
        stylist.is_active = form.is_active.data
        
        if form.image.data:
            image_file = save_stylist_image(form.image.data)
            stylist.image_file = image_file
        
        db.session.commit()
        flash('Stylist has been updated!', 'success')
        return redirect(url_for('stylists.manage_stylists'))
    
    # Pre-populate form with existing data
    elif request.method == 'GET':
        form.name.data = stylist.name
        form.bio.data = stylist.bio
        form.specialization.data = stylist.specialization
        form.experience_years.data = stylist.experience_years
        form.email.data = stylist.email
        form.phone.data = stylist.phone
        form.instagram.data = stylist.instagram
        form.is_active.data = stylist.is_active
    
    return render_template('admin/edit_stylist.html', 
                          title='Edit Stylist',
                          form=form,
                          stylist=stylist)

@stylists.route('/admin/stylists/<int:stylist_id>/delete', methods=['POST'])
@login_required
def delete_stylist(stylist_id):
    """Delete a stylist"""
    # Check if user is admin
    if current_user.id != 1:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.home'))
    
    stylist = Stylist.query.get_or_404(stylist_id)
    
    # Check if stylist has appointments
    if stylist.appointments and len(stylist.appointments) > 0:
        flash('Cannot delete stylist with existing appointments. Mark them as inactive instead.', 'warning')
        return redirect(url_for('stylists.manage_stylists'))
    
    db.session.delete(stylist)
    db.session.commit()
    flash('Stylist has been deleted!', 'success')
    return redirect(url_for('stylists.manage_stylists')) 
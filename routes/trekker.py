from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user
from app.extensions import db
from app.models import Trek, Booking, User
from app.decorators import role_required

trekker_bp = Blueprint('trekker', __name__)

@trekker_bp.route('/trekker/dashboard')
@role_required('trekker')
def dashboard():
    search = request.args.get('search', '')
    difficulty = request.args.get('difficulty', '')

    # Trekker can only view approved and open treks
    query = Trek.query.filter(Trek.status == 'Open')

    if search:
        query = query.filter((Trek.name.like(f"%{search}%")) | (Trek.location.like(f"%{search}%")))
    if difficulty:
        query = query.filter(Trek.difficulty == difficulty)

    treks = query.all()
    return render_template('trekker/dashboard.html', treks=treks, search=search, difficulty=difficulty)

@trekker_bp.route('/trekker/book/<int:trek_id>', methods=['POST'])
@role_required('trekker')
def book_trek(trek_id):
    trek = Trek.query.get_or_404(trek_id)

    # Core check: Trek must be Open
    if trek.status != 'Open':
        flash('This trek is not open for booking.', 'danger')
        return redirect(url_for('trekker.dashboard'))

    # Core check: Prevent overbooking beyond available slots
    if trek.available_slots <= 0:
        flash('No available slots remaining for this trek.', 'danger')
        return redirect(url_for('trekker.dashboard'))

    # Prevent double booking
    existing_booking = Booking.query.filter_by(user_id=current_user.id, trek_id=trek.id, status='Booked').first()
    if existing_booking:
        flash('You have already booked this trek.', 'warning')
        return redirect(url_for('trekker.dashboard'))

    # Decrement slots and write booking record
    trek.available_slots -= 1
    booking = Booking(user_id=current_user.id, trek_id=trek.id, status='Booked')
    db.session.add(booking)
    db.session.commit()

    flash(f'Trek {trek.name} booked successfully!', 'success')
    return redirect(url_for('trekker.my_bookings'))

@trekker_bp.route('/trekker/my-bookings')
@role_required('trekker')
def my_bookings():
    from datetime import date
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    return render_template('trekker/my_bookings.html', bookings=bookings, today=date.today())

@trekker_bp.route('/trekker/cancel-booking/<int:booking_id>', methods=['POST'])
@role_required('trekker')
def cancel_booking(booking_id):
    from datetime import date
    booking = Booking.query.filter_by(id=booking_id, user_id=current_user.id).first_or_404()
    
    if booking.status != 'Booked':
        flash('Only active bookings can be cancelled.', 'danger')
        return redirect(url_for('trekker.my_bookings'))
        
    if booking.trek.start_date <= date.today():
        flash('You cannot cancel a booking on or after the trek start date.', 'danger')
        return redirect(url_for('trekker.my_bookings'))
        
    booking.status = 'Cancelled'
    booking.trek.available_slots += 1
    db.session.commit()
    
    flash(f'Booking for trek {booking.trek.name} has been cancelled.', 'success')
    return redirect(url_for('trekker.my_bookings'))

@trekker_bp.route('/trekker/profile', methods=['GET', 'POST'])
@role_required('trekker')
def edit_profile():
    if request.method == 'POST':
        name = request.form.get('name')
        contact = request.form.get('contact')

        import re
        if contact and not re.match(r'^\+91\d{10}$', contact):
            flash('Contact number must start with +91 followed by exactly 10 digits.', 'danger')
            return redirect(url_for('trekker.edit_profile'))

        current_user.name = name
        current_user.contact_details = contact
        db.session.commit()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('trekker.edit_profile'))

    return render_template('trekker/edit_profile.html')

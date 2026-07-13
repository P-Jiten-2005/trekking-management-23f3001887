from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user
from app.extensions import db
from app.models import Trek, Booking
from app.decorators import role_required

staff_bp = Blueprint('staff', __name__)

@staff_bp.route('/staff/dashboard')
@role_required('staff')
def dashboard():
    from datetime import date
    assigned_treks = Trek.query.filter_by(assigned_staff_id=current_user.id).all()
    treks_data = []
    total_hikers = 0
    for trek in assigned_treks:
        booking_count = Booking.query.filter_by(trek_id=trek.id, status='Booked').count()
        total_hikers += booking_count
        treks_data.append({
            'trek': trek,
            'booking_count': booking_count
        })

    # Next departure
    future_assigned = [t for t in assigned_treks if t.start_date >= date.today() and t.status in ['Approved', 'Open']]
    next_departure = None
    if future_assigned:
        next_departure = min(future_assigned, key=lambda t: t.start_date)

    return render_template(
        'staff/dashboard.html',
        treks_data=treks_data,
        total_assigned=len(assigned_treks),
        total_hikers=total_hikers,
        next_departure=next_departure
    )

@staff_bp.route('/staff/trek/<int:trek_id>/edit', methods=['GET', 'POST'])
@role_required('staff')
def edit_trek(trek_id):
    trek = Trek.query.filter_by(id=trek_id, assigned_staff_id=current_user.id).first_or_404()
    bookings_count = Booking.query.filter_by(trek_id=trek.id, status='Booked').count()

    if request.method == 'POST':
        # Verify administrator-controlled states
        if trek.status == 'Pending':
            flash('This trek is awaiting Administrator approval and cannot be modified.', 'danger')
            return redirect(url_for('staff.edit_trek', trek_id=trek.id))
            
        status = request.form.get('status')
        if status in ['Pending', 'Approved']:
            flash('You do not have permission to transition this trek to an Administrator-controlled status.', 'danger')
            return redirect(url_for('staff.edit_trek', trek_id=trek.id))

        try:
            slots = int(request.form.get('available_slots'))
        except (ValueError, TypeError):
            flash('Available slots must be a valid integer.', 'danger')
            return redirect(url_for('staff.edit_trek', trek_id=trek.id))
        
        # Validation: Available slots cannot be negative
        if slots < 0:
            flash('Available slots cannot be negative.', 'danger')
            return redirect(url_for('staff.edit_trek', trek_id=trek.id))

        # Validation: Available slots + current bookings cannot exceed max slots
        if slots + bookings_count > trek.max_slots:
            flash(f'Total slots (Bookings: {bookings_count} + Available: {slots}) cannot exceed maximum capacity ({trek.max_slots}).', 'danger')
            return redirect(url_for('staff.edit_trek', trek_id=trek.id))

        trek.available_slots = slots
        trek.status = status
        if status == 'Completed':
            Booking.query.filter_by(trek_id=trek.id, status='Booked').update({'status': 'Completed'})
        db.session.commit()
        flash('Trek details updated successfully.', 'success')
        return redirect(url_for('staff.dashboard'))

    return render_template('staff/edit_trek.html', trek=trek, bookings_count=bookings_count)

@staff_bp.route('/staff/trek/<int:trek_id>/participants')
@role_required('staff')
def view_participants(trek_id):
    trek = Trek.query.filter_by(id=trek_id, assigned_staff_id=current_user.id).first_or_404()
    bookings = Booking.query.filter_by(trek_id=trek.id).all()
    return render_template('staff/view_participants.html', trek=trek, bookings=bookings)

@staff_bp.route('/staff/create_trek', methods=['POST'])
@role_required('staff')
def create_trek():
    from datetime import datetime
    try:
        name = request.form.get('name')
        location = request.form.get('location')
        difficulty = request.form.get('difficulty')
        duration = int(request.form.get('duration'))
        max_slots = int(request.form.get('max_slots'))
        start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date()
        end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date()
        altitude = request.form.get('altitude')
        length = request.form.get('length')
        safety_equipment = request.form.get('safety_equipment')
        price_val = request.form.get('price')
        price = float(price_val) if price_val else 0.0
        image_url = request.form.get('image_url')
    except (ValueError, TypeError):
        flash('Invalid numeric or date values provided. Please verify your inputs.', 'danger')
        return redirect(url_for('staff.dashboard'))

    if start_date > end_date:
        flash('Start date cannot be after end date.', 'danger')
        return redirect(url_for('staff.dashboard'))
    if duration <= 0 or max_slots <= 0 or price < 0:
        flash('Duration, slots, and price must be positive values.', 'danger')
        return redirect(url_for('staff.dashboard'))

    trek = Trek(
        name=name, location=location, difficulty=difficulty,
        duration=duration, max_slots=max_slots, available_slots=max_slots,
        start_date=start_date, end_date=end_date, assigned_staff_id=current_user.id,
        altitude=altitude, length=length, safety_equipment=safety_equipment,
        price=price, image_url=image_url, status='Pending'
    )
    db.session.add(trek)
    db.session.commit()
    flash('Trek proposal submitted successfully. Awaiting Admin approval.', 'success')
    return redirect(url_for('staff.dashboard'))


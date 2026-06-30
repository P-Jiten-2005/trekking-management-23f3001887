from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user
from extensions import db
from models import Trek, Booking
from decorators import role_required

staff_bp = Blueprint('staff', __name__)

@staff_bp.route('/staff/dashboard')
@role_required('staff')
def dashboard():
    assigned_treks = Trek.query.filter_by(assigned_staff_id=current_user.id).all()
    treks_data = []
    for trek in assigned_treks:
        booking_count = Booking.query.filter_by(trek_id=trek.id, status='Booked').count()
        treks_data.append({
            'trek': trek,
            'booking_count': booking_count
        })
    return render_template('staff/dashboard.html', treks_data=treks_data)

@staff_bp.route('/staff/trek/<int:trek_id>/edit', methods=['GET', 'POST'])
@role_required('staff')
def edit_trek(trek_id):
    trek = Trek.query.filter_by(id=trek_id, assigned_staff_id=current_user.id).first_or_404()
    bookings_count = Booking.query.filter_by(trek_id=trek.id, status='Booked').count()

    if request.method == 'POST':
        slots = int(request.form.get('available_slots'))
        status = request.form.get('status')
        
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

from datetime import date, datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.extensions import db
from app.models import User, Trek, Booking
from app.decorators import role_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/dashboard')
@role_required('admin')
def dashboard():
    total_treks = Trek.query.count()
    total_users = User.query.filter_by(role='trekker').count()
    total_staff = User.query.filter_by(role='staff').count()
    total_bookings = Booking.query.count()

    # Rich metrics context
    recent_bookings = Booking.query.order_by(Booking.booking_date.desc()).limit(5).all()
    pending_staff = User.query.filter_by(role='staff', is_approved=False).all()
    upcoming_treks = Trek.query.filter(Trek.status.in_(['Approved', 'Open']), Trek.start_date >= date.today()).order_by(Trek.start_date.asc()).limit(5).all()

    return render_template(
        'admin/dashboard.html',
        total_treks=total_treks,
        total_users=total_users,
        total_staff=total_staff,
        total_bookings=total_bookings,
        recent_bookings=recent_bookings,
        pending_staff=pending_staff,
        upcoming_treks=upcoming_treks
    )

@admin_bp.route('/admin/treks', methods=['GET', 'POST'])
@role_required('admin')
def manage_treks():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'create':
            try:
                name = request.form.get('name')
                location = request.form.get('location')
                difficulty = request.form.get('difficulty')
                duration = int(request.form.get('duration'))
                max_slots = int(request.form.get('max_slots'))
                start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date()
                end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date()
                staff_id = request.form.get('assigned_staff_id')
                assigned_staff_id = int(staff_id) if staff_id else None
                
                safety_equipment = request.form.get('safety_equipment')
                altitude = request.form.get('altitude')
                length = request.form.get('length')
                price_val = request.form.get('price')
                price = float(price_val) if price_val else 0.0
                image_url = request.form.get('image_url')
            except (ValueError, TypeError):
                flash('Invalid numeric or date values provided. Please verify your inputs.', 'danger')
                return redirect(url_for('admin.manage_treks'))

            if start_date > end_date:
                flash('Start date cannot be after end date.', 'danger')
                return redirect(url_for('admin.manage_treks'))
            if duration <= 0 or max_slots <= 0 or price < 0:
                flash('Duration, slots, and price must be positive values.', 'danger')
                return redirect(url_for('admin.manage_treks'))

            trek = Trek(
                name=name, location=location, difficulty=difficulty,
                duration=duration, max_slots=max_slots, available_slots=max_slots,
                start_date=start_date, end_date=end_date, assigned_staff_id=assigned_staff_id,
                safety_equipment=safety_equipment, altitude=altitude, length=length,
                price=price, image_url=image_url, status='Pending'
            )
            db.session.add(trek)
            db.session.commit()
            flash('Trek created successfully.', 'success')
            return redirect(url_for('admin.manage_treks'))

        elif action == 'assign':
            trek_id = int(request.form.get('trek_id'))
            staff_id = request.form.get('assigned_staff_id')
            trek = Trek.query.get_or_404(trek_id)
            trek.assigned_staff_id = int(staff_id) if staff_id else None
            db.session.commit()
            flash('Staff assigned successfully.', 'success')
            return redirect(url_for('admin.manage_treks'))

        elif action == 'approve':
            trek_id = int(request.form.get('trek_id'))
            trek = Trek.query.get_or_404(trek_id)
            trek.status = 'Approved'
            db.session.commit()
            flash('Trek approved successfully.', 'success')
            return redirect(url_for('admin.manage_treks'))

        elif action == 'delete':
            trek_id = int(request.form.get('trek_id'))
            trek = Trek.query.get_or_404(trek_id)
            # Remove any associated bookings before deleting the trek
            Booking.query.filter_by(trek_id=trek.id).delete()
            db.session.delete(trek)
            db.session.commit()
            flash('Trek deleted successfully.', 'success')
            return redirect(url_for('admin.manage_treks'))

    search = request.args.get('search', '')
    if search:
        treks = Trek.query.filter((Trek.name.like(f"%{search}%")) | (Trek.id == search)).order_by(Trek.start_date.desc()).all()
    else:
        treks = Trek.query.order_by(Trek.start_date.desc()).all()

    staff_members = User.query.filter_by(role='staff', is_approved=True).all()
    return render_template('admin/manage_treks.html', treks=treks, staff_members=staff_members, search=search, today=date.today())

@admin_bp.route('/admin/users', methods=['GET', 'POST'])
@role_required('admin')
def user_management():
    if request.method == 'POST':
        user_id = int(request.form.get('user_id'))
        action = request.form.get('action')
        user = User.query.get_or_404(user_id)

        if action == 'approve_staff':
            user.is_approved = True
            db.session.commit()
            flash(f'Staff {user.name} approved successfully.', 'success')
        elif action == 'promote_to_admin':
            if user.role != 'staff':
                flash('Only staff members can be promoted to Admin.', 'danger')
            else:
                user.role = 'admin'
                user.is_approved = True
                db.session.commit()
                flash(f'Staff member {user.name} has been promoted to Admin.', 'success')
        elif action == 'toggle_blacklist':
            user.is_blacklisted = not user.is_blacklisted
            db.session.commit()
            status = 'blacklisted' if user.is_blacklisted else 'whitelisted'
            flash(f'User {user.name} has been {status}.', 'info')
        return redirect(url_for('admin.user_management'))

    search = request.args.get('search', '')
    if search:
        query = User.query.filter(
            ((User.name.like(f"%{search}%")) | (User.email.like(f"%{search}%")) | (User.id == search)) & (User.role != 'admin')
        )
    else:
        query = User.query.filter(User.role != 'admin')

    users = query.order_by(User.name.asc()).all()

    return render_template('admin/user_management.html', users=users, search=search)

@admin_bp.route('/admin/bookings')
@role_required('admin')
def view_bookings():
    from app.models import Trek
    from datetime import datetime
    
    status_filter = request.args.get('status', '')
    trek_filter = request.args.get('trek_id', '')
    date_filter = request.args.get('date', '')
    
    query = Booking.query
    
    if status_filter:
        query = query.filter(Booking.status == status_filter)
    if trek_filter:
        try:
            trek_id_val = int(trek_filter)
            query = query.filter(Booking.trek_id == trek_id_val)
        except ValueError:
            pass
    if date_filter:
        try:
            target_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            from sqlalchemy import func
            query = query.filter(func.date(Booking.booking_date) == target_date)
        except ValueError:
            pass
            
    bookings = query.all()
    all_treks = Trek.query.order_by(Trek.name.asc()).all()
    
    return render_template(
        'admin/view_bookings.html',
        bookings=bookings,
        all_treks=all_treks,
        status_filter=status_filter,
        trek_filter=trek_filter,
        date_filter=date_filter
    )

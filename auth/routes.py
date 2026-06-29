from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from models import User

auth_bp = Blueprint('auth', __name__, template_folder='../templates/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        elif current_user.role == 'staff':
            if not current_user.is_approved:
                return redirect(url_for('auth.pending_approval'))
            return redirect(url_for('staff.dashboard'))
        else:
            return redirect(url_for('trekker.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('auth.login'))

        if user.is_blacklisted:
            flash('Your account has been blacklisted.', 'danger')
            return redirect(url_for('auth.login'))

        login_user(user)
        if user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        elif user.role == 'staff':
            if not user.is_approved:
                return redirect(url_for('auth.pending_approval'))
            return redirect(url_for('staff.dashboard'))
        else:
            return redirect(url_for('trekker.dashboard'))

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/register/trekker', methods=['GET', 'POST'])
def register_trekker():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        contact = request.form.get('contact')

        if User.query.filter_by(email=email).first():
            flash('Email already exists.', 'danger')
            return redirect(url_for('auth.register_trekker'))

        user = User(email=email, name=name, role='trekker', contact_details=contact, is_approved=True)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register_user.html')

@auth_bp.route('/register/staff', methods=['GET', 'POST'])
def register_staff():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        contact = request.form.get('contact')

        if User.query.filter_by(email=email).first():
            flash('Email already exists.', 'danger')
            return redirect(url_for('auth.register_staff'))

        user = User(email=email, name=name, role='staff', contact_details=contact, is_approved=False)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration submitted. Waiting for admin approval.', 'warning')
        return redirect(url_for('auth.login'))

    return render_template('register_staff.html')

@auth_bp.route('/pending-approval')
def pending_approval():
    if current_user.is_authenticated and current_user.role == 'staff' and current_user.is_approved:
        return redirect(url_for('staff.dashboard'))
    return render_template('pending_approval.html')

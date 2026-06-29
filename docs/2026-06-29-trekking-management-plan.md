# Trekking Management Application Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a modular Trekking Management Application in Flask, utilizing SQLite and Flask-Login, with role-based dashboards for Admin, Trek Staff, and Trekkers.

**Architecture:** A modular Flask application structured with Blueprints (`auth`, `admin`, `staff`, `trekker`), custom role decorators, and server-side validation using Flask-SQLAlchemy.

**Tech Stack:** Python 3.10+, Flask, Flask-SQLAlchemy, Flask-Login, SQLite, Bootstrap 5.

## Global Constraints
- Core workflows must be driven by standard HTTP POST/GET requests and Jinja templates (no core JS).
- Database creation must be programmatically handled.
- Seed a default Admin account (`admin@trek.com` / `admin123`) during DB initialization.
- Prevent booking when a trek is not "Open" or has 0 slots.
- Prevent unapproved/blacklisted users from logging in or using the dashboards.

---

### Task 1: Project Initialization & Dependency Setup

**Files:**
- Create: `requirements.txt`
- Create: `app.py`
- Create: `config.py`

**Interfaces:**
- Produces: Base Flask application factory `create_app()`

- [ ] **Step 1: Create requirements.txt**
Create the `requirements.txt` file listing all required dependencies.
```text
Flask==3.0.2
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Werkzeug==3.0.1
```

- [ ] **Step 2: Create config.py**
Create configuration class for Flask.
```python
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'trekking-secret-key-12345')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///trekking.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

- [ ] **Step 3: Create app.py skeleton**
Create the application factory structure.
```python
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @app.route('/')
    def index():
        return render_template('index.html')

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
```

- [ ] **Step 4: Create templates/index.html**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>TrekManager - Welcome</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <div class="container py-5 text-center">
        <h1 class="display-4 text-success">Welcome to TrekManager</h1>
        <p class="lead">Efficient management for organizers, staff, and trekkers.</p>
        <a href="/login" class="btn btn-primary btn-lg mt-3">Log In</a>
    </div>
</body>
</html>
```

- [ ] **Step 5: Run application locally to verify initialization**
Run: `python app.py`
Expected: Server starts on port 5000 and displays landing page.

---

### Task 2: Database Models & Pre-seeding

**Files:**
- Create: `models.py`
- Modify: `app.py` to import and seed the admin user.

**Interfaces:**
- Produces: Database models `User`, `Trek`, `Booking`.

- [ ] **Step 1: Create models.py**
Define schema.
```python
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin', 'staff', 'trekker'
    name = db.Column(db.String(100), nullable=False)
    contact_details = db.Column(db.String(200), nullable=True)
    is_approved = db.Column(db.Boolean, default=True)  # False for registered staff
    is_blacklisted = db.Column(db.Boolean, default=False)

    assigned_treks = db.relationship('Trek', backref='staff', lazy=True)
    bookings = db.relationship('Booking', backref='trekker', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Trek(db.Model):
    __tablename__ = 'treks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)  # 'Easy', 'Moderate', 'Hard'
    duration = db.Column(db.Integer, nullable=False)
    available_slots = db.Column(db.Integer, nullable=False)
    max_slots = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='Pending')  # 'Pending', 'Approved', 'Open', 'Closed', 'Completed'
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    assigned_staff_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    bookings = db.relationship('Booking', backref='trek', lazy=True)

class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey('treks.id'), nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Booked')  # 'Booked', 'Cancelled', 'Completed'
```

- [ ] **Step 2: Update imports in app.py**
```python
# Replace imports at the top of app.py
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
```
And load models in `app.py`:
```python
# Inside create_app() after login_manager.init_app(app)
    from models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
```
Add Admin seeding in `app.py`:
```python
# In app.py execution block:
if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
        from models import User
        # Seed Admin
        admin = User.query.filter_by(email='admin@trek.com').first()
        if not admin:
            admin = User(
                email='admin@trek.com',
                role='admin',
                name='System Administrator',
                is_approved=True,
                is_blacklisted=False
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Admin user seeded.")
    app.run(debug=True)
```

- [ ] **Step 3: Run app to create database and verify seed**
Run: `python app.py`
Expected: Database `instance/trekking.db` created, output prints "Admin user seeded.".

---

### Task 3: Access Control & Decorators

**Files:**
- Create: `decorators.py`

**Interfaces:**
- Produces: Decorator `role_required(*roles)`

- [ ] **Step 1: Create decorators.py**
```python
from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Please log in to access this page.', 'danger')
                return redirect(url_for('auth.login'))
            if current_user.is_blacklisted:
                flash('Your account has been blacklisted.', 'danger')
                return redirect(url_for('auth.logout'))
            if not current_user.is_approved:
                flash('Your staff registration is pending approval.', 'warning')
                return redirect(url_for('auth.pending_approval'))
            if current_user.role not in roles:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
```

---

### Task 4: Authentication Blueprint (`auth`)

**Files:**
- Create: `auth/routes.py`
- Create: `templates/auth/login.html`
- Create: `templates/auth/register_user.html`
- Create: `templates/auth/register_staff.html`
- Create: `templates/auth/pending_approval.html`
- Modify: `app.py` to register Blueprint.

- [ ] **Step 1: Create auth/routes.py**
```python
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
```

- [ ] **Step 2: Create templates/auth/login.html**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Log In - TrekManager</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <div class="container py-5">
        <div class="row justify-content-center">
            <div class="col-md-4">
                <div class="card shadow-sm p-4">
                    <h2 class="text-center text-success mb-4">Log In</h2>
                    {% with messages = get_flashed_messages(with_categories=true) %}
                        {% if messages %}
                            {% for category, message in messages %}
                                <div class="alert alert-{{ category }}">{{ message }}</div>
                            {% endfor %}
                        {% endif %}
                    {% endwith %}
                    <form method="POST" action="/login">
                        <div class="mb-3">
                            <label class="form-label">Email Address</label>
                            <input type="email" name="email" class="form-control" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Password</label>
                            <input type="password" name="password" class="form-control" required>
                        </div>
                        <button type="submit" class="btn btn-success w-100">Log In</button>
                    </form>
                    <div class="mt-3 text-center">
                        <small>Register as <a href="/register/trekker">Trekker</a> or <a href="/register/staff">Staff</a></small>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
```

- [ ] **Step 3: Create templates/auth/register_user.html**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Trekker Registration</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <div class="container py-5">
        <div class="row justify-content-center">
            <div class="col-md-5">
                <div class="card shadow-sm p-4">
                    <h2 class="text-center text-success mb-4">Register as Trekker</h2>
                    <form method="POST" action="/register/trekker">
                        <div class="mb-3">
                            <label class="form-label">Full Name</label>
                            <input type="text" name="name" class="form-control" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Email</label>
                            <input type="email" name="email" class="form-control" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Password</label>
                            <input type="password" name="password" class="form-control" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Contact Details</label>
                            <input type="text" name="contact" class="form-control">
                        </div>
                        <button type="submit" class="btn btn-success w-100">Register</button>
                    </form>
                    <div class="mt-3 text-center">
                        <small>Already have an account? <a href="/login">Log In</a></small>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
```

- [ ] **Step 4: Create templates/auth/register_staff.html**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Staff Registration</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <div class="container py-5">
        <div class="row justify-content-center">
            <div class="col-md-5">
                <div class="card shadow-sm p-4">
                    <h2 class="text-center text-primary mb-4">Register as Trek Staff</h2>
                    <form method="POST" action="/register/staff">
                        <div class="mb-3">
                            <label class="form-label">Full Name</label>
                            <input type="text" name="name" class="form-control" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Email</label>
                            <input type="email" name="email" class="form-control" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Password</label>
                            <input type="password" name="password" class="form-control" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Contact Details</label>
                            <input type="text" name="contact" class="form-control">
                        </div>
                        <button type="submit" class="btn btn-primary w-100">Register as Staff</button>
                    </form>
                    <div class="mt-3 text-center">
                        <small>Already have an account? <a href="/login">Log In</a></small>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
```

- [ ] **Step 5: Create templates/auth/pending_approval.html**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Registration Pending</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <div class="container py-5 text-center">
        <h1 class="display-5 text-warning mb-4">Registration Pending Approval</h1>
        <p class="lead">Your Trek Staff registration has been submitted and is currently awaiting administrator approval.</p>
        <a href="/logout" class="btn btn-secondary mt-3">Log Out</a>
    </div>
</body>
</html>
```

- [ ] **Step 6: Register auth Blueprint in app.py**
```python
# In app.py inside create_app():
    from auth.routes import auth_bp
    app.register_blueprint(auth_bp)
```

---

### Task 5: UI Base Layout & Custom CSS

**Files:**
- Create: `static/css/custom.css`
- Create: `templates/base.html`

- [ ] **Step 1: Create static/css/custom.css**
```css
/* Custom variables for outdoors palette */
:root {
    --primary-color: #0d6efd;
    --accent-color: #0f5132;
    --bg-gradient: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    --card-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

body {
    background: var(--bg-gradient);
    min-height: 100vh;
    font-family: system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

.navbar {
    background-color: var(--accent-color) !important;
}

.card {
    border: none;
    box-shadow: var(--card-shadow);
    border-radius: 12px;
}
```

- [ ] **Step 2: Create templates/base.html**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}TrekManager{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/custom.css') }}">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
        <div class="container">
            <a class="navbar-brand" href="/">TrekManager</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    {% if current_user.is_authenticated %}
                        {% if current_user.role == 'admin' %}
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('admin.dashboard') }}">Dashboard</a></li>
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('admin.manage_treks') }}">Manage Treks</a></li>
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('admin.view_bookings') }}">All Bookings</a></li>
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('admin.user_management') }}">User & Staff Management</a></li>
                        {% elif current_user.role == 'staff' %}
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('staff.dashboard') }}">Dashboard</a></li>
                        {% elif current_user.role == 'trekker' %}
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('trekker.dashboard') }}">Find Treks</a></li>
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('trekker.my_bookings') }}">My Bookings</a></li>
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('trekker.edit_profile') }}">My Profile</a></li>
                        {% endif %}
                    {% endif %}
                </ul>
                <ul class="navbar-nav ms-auto">
                    {% if current_user.is_authenticated %}
                        <li class="nav-item"><span class="navbar-text me-3">Logged in as {{ current_user.name }} ({{ current_user.role }})</span></li>
                        <li class="nav-item"><a class="btn btn-outline-light btn-sm" href="{{ url_for('auth.logout') }}">Log Out</a></li>
                    {% else %}
                        <li class="nav-item"><a class="nav-link" href="{{ url_for('auth.login') }}">Log In</a></li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>

    <div class="container">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        {% block content %}{% endblock %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

---

### Task 6: Admin Blueprint (`admin`)

**Files:**
- Create: `admin/routes.py`
- Create: `templates/admin/dashboard.html`
- Create: `templates/admin/manage_treks.html`
- Create: `templates/admin/view_bookings.html`
- Create: `templates/admin/user_management.html`
- Modify: `app.py` to register Blueprint.

- [ ] **Step 1: Create admin/routes.py**
```python
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from models import User, Trek, Booking
from decorators import role_required

admin_bp = Blueprint('admin', __name__, template_folder='../templates/admin')

@admin_bp.route('/admin/dashboard')
@role_required('admin')
def dashboard():
    total_treks = Trek.query.count()
    total_users = User.query.filter_by(role='trekker').count()
    total_staff = User.query.filter_by(role='staff').count()
    total_bookings = Booking.query.count()
    return render_template('dashboard.html', total_treks=total_treks, total_users=total_users, total_staff=total_staff, total_bookings=total_bookings)

@admin_bp.route('/admin/treks', methods=['GET', 'POST'])
@role_required('admin')
def manage_treks():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'create':
            name = request.form.get('name')
            location = request.form.get('location')
            difficulty = request.form.get('difficulty')
            duration = int(request.form.get('duration'))
            max_slots = int(request.form.get('max_slots'))
            start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date()
            end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date()
            staff_id = request.form.get('assigned_staff_id')
            assigned_staff_id = int(staff_id) if staff_id else None

            trek = Trek(
                name=name, location=location, difficulty=difficulty,
                duration=duration, max_slots=max_slots, available_slots=max_slots,
                start_date=start_date, end_date=end_date, assigned_staff_id=assigned_staff_id,
                status='Pending'
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
            db.session.delete(trek)
            db.session.commit()
            flash('Trek deleted successfully.', 'success')
            return redirect(url_for('admin.manage_treks'))

    search = request.args.get('search', '')
    if search:
        treks = Trek.query.filter((Trek.name.like(f"%{search}%")) | (Trek.id == search)).all()
    else:
        treks = Trek.query.all()

    staff_members = User.query.filter_by(role='staff', is_approved=True).all()
    return render_template('manage_treks.html', treks=treks, staff_members=staff_members, search=search)

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
        elif action == 'toggle_blacklist':
            user.is_blacklisted = not user.is_blacklisted
            db.session.commit()
            status = 'blacklisted' if user.is_blacklisted else 'whitelisted'
            flash(f'User {user.name} has been {status}.', 'info')
        return redirect(url_for('admin.user_management'))

    search = request.args.get('search', '')
    if search:
        users = User.query.filter(
            ((User.name.like(f"%{search}%")) | (User.email.like(f"%{search}%")) | (User.id == search)) & (User.role != 'admin')
        ).all()
    else:
        users = User.query.filter(User.role != 'admin').all()

    return render_template('user_management.html', users=users, search=search)

@admin_bp.route('/admin/bookings')
@role_required('admin')
def view_bookings():
    bookings = Booking.query.all()
    return render_template('view_bookings.html', bookings=bookings)
```

- [ ] **Step 2: Create templates/admin/dashboard.html**
```html
{% extends "base.html" %}
{% block title %}Admin Dashboard - TrekManager{% endblock %}
{% block content %}
<div class="row">
    <div class="col-12 mb-4">
        <h1>Admin Dashboard</h1>
    </div>
</div>
<div class="row g-4">
    <div class="col-md-3">
        <div class="card p-3 text-center bg-primary text-white">
            <h5>Total Treks</h5>
            <h2>{{ total_treks }}</h2>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card p-3 text-center bg-success text-white">
            <h5>Total Trekkers</h5>
            <h2>{{ total_users }}</h2>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card p-3 text-center bg-info text-white">
            <h5>Total Staff</h5>
            <h2>{{ total_staff }}</h2>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card p-3 text-center bg-warning text-white">
            <h5>Total Bookings</h5>
            <h2>{{ total_bookings }}</h2>
        </div>
    </div>
</div>
{% endblock %}
```

- [ ] **Step 3: Create templates/admin/manage_treks.html**
```html
{% extends "base.html" %}
{% block title %}Manage Treks{% endblock %}
{% block content %}
<div class="row">
    <div class="col-md-8">
        <h2>Manage Treks</h2>
    </div>
    <div class="col-md-4 text-end">
        <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#createTrekModal">Create New Trek</button>
    </div>
</div>

<form method="GET" action="{{ url_for('admin.manage_treks') }}" class="row g-3 my-3">
    <div class="col-md-10">
        <input type="text" name="search" class="form-control" placeholder="Search treks by name or ID" value="{{ search }}">
    </div>
    <div class="col-md-2">
        <button type="submit" class="btn btn-secondary w-100">Search</button>
    </div>
</form>

<table class="table table-striped table-hover mt-3">
    <thead>
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Location</th>
            <th>Difficulty</th>
            <th>Duration (Days)</th>
            <th>Slots</th>
            <th>Status</th>
            <th>Staff</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        {% for trek in treks %}
        <tr>
            <td>{{ trek.id }}</td>
            <td>{{ trek.name }}</td>
            <td>{{ trek.location }}</td>
            <td>{{ trek.difficulty }}</td>
            <td>{{ trek.duration }}</td>
            <td>{{ trek.available_slots }}/{{ trek.max_slots }}</td>
            <td><span class="badge bg-secondary">{{ trek.status }}</span></td>
            <td>{{ trek.staff.name if trek.staff else 'None' }}</td>
            <td>
                <div class="d-flex gap-2">
                    {% if trek.status == 'Pending' %}
                    <form method="POST" action="{{ url_for('admin.manage_treks') }}">
                        <input type="hidden" name="action" value="approve">
                        <input type="hidden" name="trek_id" value="{{ trek.id }}">
                        <button type="submit" class="btn btn-success btn-sm">Approve</button>
                    </form>
                    {% endif %}
                    <button class="btn btn-sm btn-info" data-bs-toggle="modal" data-bs-target="#assignModal{{ trek.id }}">Assign Staff</button>
                    <form method="POST" action="{{ url_for('admin.manage_treks') }}" onsubmit="return confirm('Are you sure?');">
                        <input type="hidden" name="action" value="delete">
                        <input type="hidden" name="trek_id" value="{{ trek.id }}">
                        <button type="submit" class="btn btn-danger btn-sm">Delete</button>
                    </form>
                </div>
            </td>
        </tr>

        <!-- Assign Modal -->
        <div class="modal fade" id="assignModal{{ trek.id }}" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <form method="POST" action="{{ url_for('admin.manage_treks') }}">
                        <div class="modal-header">
                            <h5 class="modal-title">Assign Staff for {{ trek.name }}</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <input type="hidden" name="action" value="assign">
                            <input type="hidden" name="trek_id" value="{{ trek.id }}">
                            <div class="mb-3">
                                <label class="form-label">Trek Staff</label>
                                <select name="assigned_staff_id" class="form-select">
                                    <option value="">None</option>
                                    {% for staff in staff_members %}
                                    <option value="{{ staff.id }}" {% if trek.assigned_staff_id == staff.id %}selected{% endif %}>{{ staff.name }}</option>
                                    {% endfor %}
                                </select>
                            </div>
                        </div>
                        <div class="modal-header">
                            <button type="submit" class="btn btn-primary">Save Changes</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
        {% endfor %}
    </tbody>
</table>

<!-- Create Trek Modal -->
<div class="modal fade" id="createTrekModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <form method="POST" action="{{ url_for('admin.manage_treks') }}">
                <div class="modal-header">
                    <h5 class="modal-title">Create New Trek</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <input type="hidden" name="action" value="create">
                    <div class="mb-3">
                        <label class="form-label">Trek Name</label>
                        <input type="text" name="name" class="form-control" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Location</label>
                        <input type="text" name="location" class="form-control" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Difficulty</label>
                        <select name="difficulty" class="form-select">
                            <option value="Easy">Easy</option>
                            <option value="Moderate">Moderate</option>
                            <option value="Hard">Hard</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Duration (in Days)</label>
                        <input type="number" name="duration" class="form-control" min="1" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Max Slots</label>
                        <input type="number" name="max_slots" class="form-control" min="1" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Start Date</label>
                        <input type="date" name="start_date" class="form-control" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">End Date</label>
                        <input type="date" name="end_date" class="form-control" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Assign Staff</label>
                        <select name="assigned_staff_id" class="form-select">
                            <option value="">None</option>
                            {% for staff in staff_members %}
                            <option value="{{ staff.id }}">{{ staff.name }}</option>
                            {% endfor %}
                        </select>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="submit" class="btn btn-primary">Create</button>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}
```

- [ ] **Step 4: Create templates/admin/user_management.html**
```html
{% extends "base.html" %}
{% block title %}User & Staff Management{% endblock %}
{% block content %}
<h2>User & Staff Management</h2>

<form method="GET" action="{{ url_for('admin.user_management') }}" class="row g-3 my-3">
    <div class="col-md-10">
        <input type="text" name="search" class="form-control" placeholder="Search users by name, email, or ID" value="{{ search }}">
    </div>
    <div class="col-md-2">
        <button type="submit" class="btn btn-secondary w-100">Search</button>
    </div>
</form>

<table class="table table-striped table-hover">
    <thead>
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Role</th>
            <th>Status</th>
            <th>Blacklisted</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        {% for user in users %}
        <tr>
            <td>{{ user.id }}</td>
            <td>{{ user.name }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.role }}</td>
            <td>
                {% if user.role == 'staff' %}
                    {% if user.is_approved %}
                    <span class="badge bg-success">Approved</span>
                    {% else %}
                    <span class="badge bg-warning text-dark">Pending Approval</span>
                    {% endif %}
                {% else %}
                    <span class="badge bg-info">Active</span>
                {% endif %}
            </td>
            <td>
                {% if user.is_blacklisted %}
                <span class="badge bg-danger">Yes</span>
                {% else %}
                <span class="badge bg-secondary">No</span>
                {% endif %}
            </td>
            <td>
                <div class="d-flex gap-2">
                    {% if user.role == 'staff' and not user.is_approved %}
                    <form method="POST" action="{{ url_for('admin.user_management') }}">
                        <input type="hidden" name="user_id" value="{{ user.id }}">
                        <input type="hidden" name="action" value="approve_staff">
                        <button type="submit" class="btn btn-sm btn-success">Approve Staff</button>
                    </form>
                    {% endif %}
                    <form method="POST" action="{{ url_for('admin.user_management') }}">
                        <input type="hidden" name="user_id" value="{{ user.id }}">
                        <input type="hidden" name="action" value="toggle_blacklist">
                        <button type="submit" class="btn btn-sm btn-danger">
                            {% if user.is_blacklisted %}Whitelist{% else %}Blacklist{% endif %}
                        </button>
                    </form>
                </div>
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}
```

- [ ] **Step 5: Create templates/admin/view_bookings.html**
```html
{% extends "base.html" %}
{% block title %}All Bookings{% endblock %}
{% block content %}
<h2>All Bookings</h2>
<table class="table table-striped table-hover mt-3">
    <thead>
        <tr>
            <th>Booking ID</th>
            <th>Trek Name</th>
            <th>Trekker Name</th>
            <th>Booking Date</th>
            <th>Status</th>
        </tr>
    </thead>
    <tbody>
        {% for booking in bookings %}
        <tr>
            <td>{{ booking.id }}</td>
            <td>{{ booking.trek.name }}</td>
            <td>{{ booking.trekker.name }}</td>
            <td>{{ booking.booking_date.strftime('%Y-%m-%d %H:%M') }}</td>
            <td><span class="badge bg-primary">{{ booking.status }}</span></td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}
```

- [ ] **Step 6: Register admin Blueprint in app.py**
```python
# In app.py inside create_app():
    from admin.routes import admin_bp
    app.register_blueprint(admin_bp)
```

---

### Task 7: Trek Staff Blueprint (`staff`)

**Files:**
- Create: `staff/routes.py`
- Create: `templates/staff/dashboard.html`
- Create: `templates/staff/edit_trek.html`
- Create: `templates/staff/view_participants.html`
- Modify: `app.py` to register Blueprint.

- [ ] **Step 1: Create staff/routes.py**
```python
from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from models import Trek, Booking
from decorators import role_required

staff_bp = Blueprint('staff', __name__, template_folder='../templates/staff')

@staff_bp.route('/staff/dashboard')
@role_required('staff')
def dashboard():
    from flask_login import current_user
    assigned_treks = Trek.query.filter_by(assigned_staff_id=current_user.id).all()
    # Build list of dict with trek details and total bookings count
    treks_data = []
    for trek in assigned_treks:
        booking_count = Booking.query.filter_by(trek_id=trek.id, status='Booked').count()
        treks_data.append({
            'trek': trek,
            'booking_count': booking_count
        })
    return render_template('dashboard.html', treks_data=treks_data)

@staff_bp.route('/staff/trek/<int:trek_id>/edit', methods=['GET', 'POST'])
@role_required('staff')
def edit_trek(trek_id):
    from flask_login import current_user
    trek = Trek.query.filter_by(id=trek_id, assigned_staff_id=current_user.id).first_or_404()

    if request.method == 'POST':
        slots = int(request.form.get('available_slots'))
        status = request.form.get('status')
        
        # Validation: Available slots cannot exceed max_slots
        if slots > trek.max_slots:
            flash(f'Available slots cannot exceed maximum slots ({trek.max_slots}).', 'danger')
            return redirect(url_for('staff.edit_trek', trek_id=trek.id))

        # Check existing bookings count
        bookings_count = Booking.query.filter_by(trek_id=trek.id, status='Booked').count()
        # Slots cannot be reduced below active bookings
        if slots < bookings_count:
            flash(f'Available slots cannot be less than active bookings ({bookings_count}).', 'danger')
            return redirect(url_for('staff.edit_trek', trek_id=trek.id))

        trek.available_slots = slots
        trek.status = status
        db.session.commit()
        flash('Trek updated successfully.', 'success')
        return redirect(url_for('staff.dashboard'))

    return render_template('edit_trek.html', trek=trek)

@staff_bp.route('/staff/trek/<int:trek_id>/participants')
@role_required('staff')
def view_participants(trek_id):
    from flask_login import current_user
    trek = Trek.query.filter_by(id=trek_id, assigned_staff_id=current_user.id).first_or_404()
    bookings = Booking.query.filter_by(trek_id=trek.id).all()
    return render_template('view_participants.html', trek=trek, bookings=bookings)
```

- [ ] **Step 2: Create templates/staff/dashboard.html**
```html
{% extends "base.html" %}
{% block title %}Staff Dashboard - TrekManager{% endblock %}
{% block content %}
<h2>Staff Dashboard</h2>
<div class="row mt-4">
    <div class="col-12">
        <h4>Your Assigned Treks</h4>
        <table class="table table-striped table-hover mt-3">
            <thead>
                <tr>
                    <th>Trek ID</th>
                    <th>Trek Name</th>
                    <th>Location</th>
                    <th>Date Range</th>
                    <th>Available Slots / Capacity</th>
                    <th>Active Registrations</th>
                    <th>Status</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {% for data in treks_data %}
                <tr>
                    <td>{{ data.trek.id }}</td>
                    <td>{{ data.trek.name }}</td>
                    <td>{{ data.trek.location }}</td>
                    <td>{{ data.trek.start_date.strftime('%Y-%m-%d') }} to {{ data.trek.end_date.strftime('%Y-%m-%d') }}</td>
                    <td>{{ data.trek.available_slots }} / {{ data.trek.max_slots }}</td>
                    <td>{{ data.booking_count }}</td>
                    <td><span class="badge bg-info">{{ data.trek.status }}</span></td>
                    <td>
                        <div class="d-flex gap-2">
                            <a href="{{ url_for('staff.edit_trek', trek_id=data.trek.id) }}" class="btn btn-sm btn-primary">Update Details</a>
                            <a href="{{ url_for('staff.view_participants', trek_id=data.trek.id) }}" class="btn btn-sm btn-secondary">View Trekkers</a>
                        </div>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}
```

- [ ] **Step 3: Create templates/staff/edit_trek.html**
```html
{% extends "base.html" %}
{% block title %}Update Trek Status{% endblock %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card p-4">
            <h4>Update Trek: {{ trek.name }}</h4>
            <form method="POST" class="mt-3">
                <div class="mb-3">
                    <label class="form-label">Available Slots</label>
                    <input type="number" name="available_slots" class="form-control" value="{{ trek.available_slots }}" min="0" required>
                    <small class="text-muted">Maximum capacity is {{ trek.max_slots }}</small>
                </div>
                <div class="mb-3">
                    <label class="form-label">Trek Status</label>
                    <select name="status" class="form-select">
                        <option value="Pending" {% if trek.status == 'Pending' %}selected{% endif %}>Pending</option>
                        <option value="Approved" {% if trek.status == 'Approved' %}selected{% endif %}>Approved</option>
                        <option value="Open" {% if trek.status == 'Open' %}selected{% endif %}>Open</option>
                        <option value="Closed" {% if trek.status == 'Closed' %}selected{% endif %}>Closed</option>
                        <option value="Completed" {% if trek.status == 'Completed' %}selected{% endif %}>Completed</option>
                    </select>
                </div>
                <button type="submit" class="btn btn-primary w-100">Update Trek</button>
            </form>
        </div>
    </div>
</div>
{% endblock %}
```

- [ ] **Step 24: Create templates/staff/view_participants.html**
```html
{% extends "base.html" %}
{% block title %}Participants - {{ trek.name }}{% endblock %}
{% block content %}
<h2>Trekkers Registered for {{ trek.name }}</h2>
<table class="table table-striped table-hover mt-3">
    <thead>
        <tr>
            <th>Trekker Name</th>
            <th>Email</th>
            <th>Contact</th>
            <th>Booking Date</th>
            <th>Status</th>
        </tr>
    </thead>
    <tbody>
        {% for booking in bookings %}
        <tr>
            <td>{{ booking.trekker.name }}</td>
            <td>{{ booking.trekker.email }}</td>
            <td>{{ booking.trekker.contact_details }}</td>
            <td>{{ booking.booking_date.strftime('%Y-%m-%d') }}</td>
            <td><span class="badge bg-success">{{ booking.status }}</span></td>
        </tr>
        {% endfor %}
    </tbody>
</table>
<a href="{{ url_for('staff.dashboard') }}" class="btn btn-secondary mt-3">Back to Dashboard</a>
{% endblock %}
```

- [ ] **Step 5: Register staff Blueprint in app.py**
```python
# In app.py inside create_app():
    from staff.routes import staff_bp
    app.register_blueprint(staff_bp)
```

---

### Task 8: Trekker Blueprint (`trekker`)

**Files:**
- Create: `trekker/routes.py`
- Create: `templates/trekker/dashboard.html`
- Create: `templates/trekker/my_bookings.html`
- Create: `templates/trekker/edit_profile.html`
- Modify: `app.py` to register Blueprint.

- [ ] **Step 1: Create trekker/routes.py**
```python
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user
from app import db
from models import Trek, Booking, User
from decorators import role_required

trekker_bp = Blueprint('trekker', __name__, template_folder='../templates/trekker')

@trekker_bp.route('/trekker/dashboard')
@role_required('trekker')
def dashboard():
    search = request.args.get('search', '')
    difficulty = request.args.get('difficulty', '')

    query = Trek.query.filter(Trek.status == 'Open')

    if search:
        query = query.filter((Trek.name.like(f"%{search}%")) | (Trek.location.like(f"%{search}%")))
    if difficulty:
        query = query.filter(Trek.difficulty == difficulty)

    treks = query.all()
    return render_template('dashboard.html', treks=treks, search=search, difficulty=difficulty)

@trekker_bp.route('/trekker/book/<int:trek_id>', methods=['POST'])
@role_required('trekker')
def book_trek(trek_id):
    trek = Trek.query.get_or_404(trek_id)

    # Double check: Trek must be Open
    if trek.status != 'Open':
        flash('This trek is not open for booking.', 'danger')
        return redirect(url_for('trekker.dashboard'))

    # Check for overbooking
    if trek.available_slots <= 0:
        flash('No available slots remaining for this trek.', 'danger')
        return redirect(url_for('trekker.dashboard'))

    # Prevent double booking
    existing_booking = Booking.query.filter_by(user_id=current_user.id, trek_id=trek.id, status='Booked').first()
    if existing_booking:
        flash('You have already booked this trek.', 'warning')
        return redirect(url_for('trekker.dashboard'))

    # Decrement slot and create booking atomically
    trek.available_slots -= 1
    booking = Booking(user_id=current_user.id, trek_id=trek.id, status='Booked')
    db.session.add(booking)
    db.session.commit()

    flash(f'Trek {trek.name} booked successfully!', 'success')
    return redirect(url_for('trekker.my_bookings'))

@trekker_bp.route('/trekker/my-bookings')
@role_required('trekker')
def my_bookings():
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    return render_template('my_bookings.html', bookings=bookings)

@trekker_bp.route('/trekker/profile', methods=['GET', 'POST'])
@role_required('trekker')
def edit_profile():
    if request.method == 'POST':
        name = request.form.get('name')
        contact = request.form.get('contact')

        current_user.name = name
        current_user.contact_details = contact
        db.session.commit()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('trekker.edit_profile'))

    return render_template('edit_profile.html')
```

- [ ] **Step 2: Create templates/trekker/dashboard.html**
```html
{% extends "base.html" %}
{% block title %}Find Treks - TrekManager{% endblock %}
{% block content %}
<h2>Find Your Next Adventure</h2>

<form method="GET" action="{{ url_for('trekker.dashboard') }}" class="row g-3 my-4">
    <div class="col-md-6">
        <input type="text" name="search" class="form-control" placeholder="Search by name or location" value="{{ search }}">
    </div>
    <div class="col-md-3">
        <select name="difficulty" class="form-select">
            <option value="">Any Difficulty</option>
            <option value="Easy" {% if difficulty == 'Easy' %}selected{% endif %}>Easy</option>
            <option value="Moderate" {% if difficulty == 'Moderate' %}selected{% endif %}>Moderate</option>
            <option value="Hard" {% if difficulty == 'Hard' %}selected{% endif %}>Hard</option>
        </select>
    </div>
    <div class="col-md-3">
        <button type="submit" class="btn btn-success w-100">Filter Treks</button>
    </div>
</form>

<div class="row g-4">
    {% for trek in treks %}
    <div class="col-md-4">
        <div class="card h-100 shadow-sm">
            <div class="card-body d-flex flex-column">
                <h5 class="card-title">{{ trek.name }}</h5>
                <h6 class="card-subtitle mb-2 text-muted">{{ trek.location }}</h6>
                <div class="my-2">
                    <span class="badge bg-warning text-dark">{{ trek.difficulty }}</span>
                    <span class="badge bg-info text-dark">{{ trek.duration }} Days</span>
                </div>
                <p class="card-text mt-2">
                    <strong>Date:</strong> {{ trek.start_date.strftime('%Y-%m-%d') }} to {{ trek.end_date.strftime('%Y-%m-%d') }}<br>
                    <strong>Available Slots:</strong> {{ trek.available_slots }} / {{ trek.max_slots }}
                </p>
                <div class="mt-auto">
                    <form method="POST" action="{{ url_for('trekker.book_trek', trek_id=trek.id) }}">
                        <button type="submit" class="btn btn-success w-100" {% if trek.available_slots <= 0 %}disabled{% endif %}>
                            {% if trek.available_slots <= 0 %}Sold Out{% else %}Book Now{% endif %}
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>
    {% else %}
    <div class="col-12">
        <div class="alert alert-warning text-center">No open treks found matching the filters.</div>
    </div>
    {% endfor %}
</div>
{% endblock %}
```

- [ ] **Step 3: Create templates/trekker/my_bookings.html**
```html
{% extends "base.html" %}
{% block title %}My Bookings - TrekManager{% endblock %}
{% block content %}
<h2>My Bookings & History</h2>
<table class="table table-striped table-hover mt-3">
    <thead>
        <tr>
            <th>Booking ID</th>
            <th>Trek Name</th>
            <th>Location</th>
            <th>Difficulty</th>
            <th>Duration</th>
            <th>Booking Date</th>
            <th>Status</th>
        </tr>
    </thead>
    <tbody>
        {% for booking in bookings %}
        <tr>
            <td>{{ booking.id }}</td>
            <td>{{ booking.trek.name }}</td>
            <td>{{ booking.trek.location }}</td>
            <td>{{ booking.trek.difficulty }}</td>
            <td>{{ booking.trek.duration }} Days</td>
            <td>{{ booking.booking_date.strftime('%Y-%m-%d %H:%M') }}</td>
            <td><span class="badge bg-success">{{ booking.status }}</span></td>
        </tr>
        {% else %}
        <tr>
            <td colspan="7" class="text-center">You have no booking history.</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}
```

- [ ] **Step 4: Create templates/trekker/edit_profile.html**
```html
{% extends "base.html" %}
{% block title %}Edit Profile{% endblock %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card p-4">
            <h4>Update Profile</h4>
            <form method="POST" class="mt-3">
                <div class="mb-3">
                    <label class="form-label">Full Name</label>
                    <input type="text" name="name" class="form-control" value="{{ current_user.name }}" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">Contact Details</label>
                    <input type="text" name="contact" class="form-control" value="{{ current_user.contact_details }}">
                </div>
                <button type="submit" class="btn btn-success w-100">Save Changes</button>
            </form>
        </div>
    </div>
</div>
{% endblock %}
```

- [ ] **Step 5: Register trekker Blueprint in app.py**
```python
# In app.py inside create_app():
    from trekker.routes import trekker_bp
    app.register_blueprint(trekker_bp)
```

---

## Verification Plan

### Automated Verification
We will run a test script (`verify_app.py`) to verify role creation, database migrations, and basic authorization rules.

### Manual Verification
1. Run application `python app.py`.
2. Access `http://127.0.5.1:5000` or `http://localhost:5000`.
3. Log in with `admin@trek.com` / `admin123`.
4. Register a staff user, verify that logging in immediately redirects them to pending approval page.
5. In admin dashboard, approve the registered staff user and create a trek, assigning it to the staff.
6. Register a trekker user, find and book the trek.
7. Verify that available slots decrement.
8. Blacklist the trekker user from the admin dashboard, verify that they are logged out and unable to log in again.

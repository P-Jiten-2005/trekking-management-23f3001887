from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db

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
    
    # New expedition fields
    safety_equipment = db.Column(db.String(500), nullable=True)
    altitude = db.Column(db.String(100), nullable=True)
    length = db.Column(db.String(100), nullable=True)
    price = db.Column(db.Float, nullable=True)
    image_url = db.Column(db.String(500), nullable=True)

    bookings = db.relationship('Booking', backref='trek', lazy=True)

class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey('treks.id'), nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Booked')  # 'Booked', 'Cancelled', 'Completed'

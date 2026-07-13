from flask import Blueprint, jsonify
from app.models import User, Trek, Booking

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/treks', methods=['GET'])
def get_treks():
    treks = Trek.query.all()
    output = []
    for trek in treks:
        output.append({
            'id': trek.id,
            'name': trek.name,
            'location': trek.location,
            'difficulty': trek.difficulty,
            'duration': trek.duration,
            'available_slots': trek.available_slots,
            'max_slots': trek.max_slots,
            'status': trek.status,
            'start_date': trek.start_date.strftime('%Y-%m-%d'),
            'end_date': trek.end_date.strftime('%Y-%m-%d'),
            'assigned_staff_id': trek.assigned_staff_id,
            'altitude': trek.altitude,
            'length': trek.length,
            'safety_equipment': trek.safety_equipment,
            'price': trek.price,
            'image_url': trek.image_url
        })
    return jsonify(output)

@api_bp.route('/treks/<int:trek_id>', methods=['GET'])
def get_trek(trek_id):
    trek = Trek.query.get_or_404(trek_id)
    return jsonify({
        'id': trek.id,
        'name': trek.name,
        'location': trek.location,
        'difficulty': trek.difficulty,
        'duration': trek.duration,
        'available_slots': trek.available_slots,
        'max_slots': trek.max_slots,
        'status': trek.status,
        'start_date': trek.start_date.strftime('%Y-%m-%d'),
        'end_date': trek.end_date.strftime('%Y-%m-%d'),
        'assigned_staff_id': trek.assigned_staff_id,
        'altitude': trek.altitude,
        'length': trek.length,
        'safety_equipment': trek.safety_equipment,
        'price': trek.price,
        'image_url': trek.image_url
    })

@api_bp.route('/bookings', methods=['GET'])
def get_bookings():
    bookings = Booking.query.all()
    output = []
    for booking in bookings:
        output.append({
            'id': booking.id,
            'user_id': booking.user_id,
            'trek_id': booking.trek_id,
            'booking_date': booking.booking_date.strftime('%Y-%m-%d %H:%M:%S') if booking.booking_date else None,
            'status': booking.status
        })
    return jsonify(output)

@api_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    output = []
    for user in users:
        output.append({
            'id': user.id,
            'email': user.email,
            'role': user.role,
            'name': user.name,
            'contact_details': user.contact_details,
            'is_approved': user.is_approved,
            'is_blacklisted': user.is_blacklisted
        })
    return jsonify(output)

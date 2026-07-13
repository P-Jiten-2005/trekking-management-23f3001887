from datetime import date

from app import create_app
from app.extensions import db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        from app.models import User, Trek, Booking

        # Seed Admin
        admin = User.query.filter_by(email='Jiten@trek.com').first()
        if not admin:
            admin = User(
                email='Jiten@trek.com',
                role='admin',
                name='System Administrator',
                is_approved=True,
                is_blacklisted=False
            )
            admin.set_password('Jiten@123')
            db.session.add(admin)
            print("Admin user seeded.")

        # Seed Staff
        staff = User.query.filter_by(email='vyeshwanth@trek.com').first()
        if not staff:
            staff = User(
                email='vyeshwanth@trek.com',
                role='staff',
                name='Yeshwanth Vutukuru',
                contact_details='+919999888777',
                is_approved=True,
                is_blacklisted=False
            )
            staff.set_password('yesh@1234')
            db.session.add(staff)
            print("Staff user seeded.")

        # Seed Trekker
        trekker = User.query.filter_by(email='gupta14@gmail.com').first()
        if not trekker:
            trekker = User(
                email='gupta14@gmail.com',
                role='trekker',
                name='Priya Patel',
                contact_details='+919876543210',
                is_approved=True,
                is_blacklisted=False
            )
            trekker.set_password('gupta@123')
            db.session.add(trekker)
            print("Trekker user seeded.")

        db.session.commit()

        # Seed Treks (re-fetch staff id after commit)
        staff = User.query.filter_by(email='vyeshwanth@trek.com').first()

        trek1 = Trek.query.filter_by(name='Valley of Flowers').first()
        if not trek1:
            trek1 = Trek(
                name='Valley of Flowers',
                location='Uttarakhand',
                difficulty='Moderate',
                duration=6,
                max_slots=10,
                available_slots=8,
                start_date=date(2026, 7, 10),
                end_date=date(2026, 7, 16),
                assigned_staff_id=staff.id if staff else None,
                status='Open',
                altitude='12,500 ft',
                length='25 km',
                safety_equipment='Trekking poles, microspikes, first-aid kit',
                price=5000.0,
                image_url='https://images.unsplash.com/photo-1585409677983-0f6c41ca9c3b'
            )
            db.session.add(trek1)
            print("Trek 'Valley of Flowers' seeded.")

        trek2 = Trek.query.filter_by(name='Kedarkantha Base Camp').first()
        if not trek2:
            trek2 = Trek(
                name='Kedarkantha Base Camp',
                location='Uttarakhand',
                difficulty='Easy',
                duration=4,
                max_slots=15,
                available_slots=15,
                start_date=date(2026, 8, 15),
                end_date=date(2026, 8, 19),
                assigned_staff_id=None,
                status='Approved',
                altitude='12,000 ft',
                length='20 km',
                safety_equipment='Warm clothing, trekking shoes, headlamp',
                price=3500.0,
                image_url='https://images.unsplash.com/photo-1599493594087-e555d44d5263'
            )
            db.session.add(trek2)
            print("Trek 'Kedarkantha Base Camp' seeded.")

        trek3 = Trek.query.filter_by(name='Chadar Trek').first()
        if not trek3:
            trek3 = Trek(
                name='Chadar Trek',
                location='Ladakh',
                difficulty='Hard',
                duration=9,
                max_slots=8,
                available_slots=8,
                start_date=date(2026, 12, 1),
                end_date=date(2026, 12, 10),
                assigned_staff_id=staff.id if staff else None,
                status='Pending',
                altitude='11,500 ft',
                length='62 km',
                safety_equipment='Crampons, microspikes, sleeping bag (-20°C), tent',
                price=8000.0,
                image_url='https://images.unsplash.com/photo-1562095241-8c6714fd4178'
            )
            db.session.add(trek3)
            print("Trek 'Chadar Trek' seeded.")

        db.session.commit()

        # Seed Booking (trekker booked on Open trek)
        trekker = User.query.filter_by(email='gupta14@gmail.com').first()
        open_trek = Trek.query.filter_by(name='Valley of Flowers').first()
        if trekker and open_trek:
            existing = Booking.query.filter_by(user_id=trekker.id, trek_id=open_trek.id).first()
            if not existing:
                booking = Booking(user_id=trekker.id, trek_id=open_trek.id, status='Booked')
                db.session.add(booking)
                print("Sample booking seeded.")
                db.session.commit()

    app.run(host='127.0.0.1', port=1234, debug=True)

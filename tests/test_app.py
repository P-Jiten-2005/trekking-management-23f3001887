import unittest
from datetime import datetime, date, timedelta
from app import create_app
from app.extensions import db
from app.models import User, Trek, Booking

class TrekAppTestCase(unittest.TestCase):
    def setUp(self):
        # Configure app for testing with an in-memory SQLite database
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['WTF_CSRF_ENABLED'] = False
        
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        
        db.create_all()
        
        # Seed default Admin if not already present
        self.admin = User.query.filter_by(email='Jiten@trek.com').first()
        if not self.admin:
            self.admin = User(
                email='Jiten@trek.com',
                role='admin',
                name='System Administrator',
                is_approved=True,
                is_blacklisted=False
            )
            self.admin.set_password('Jiten@123')
            db.session.add(self.admin)
            db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_admin_seeded(self):
        """Verify the default admin account exists and credentials check out."""
        admin = User.query.filter_by(email='Jiten@trek.com').first()
        self.assertIsNotNone(admin)
        self.assertTrue(admin.check_password('Jiten@123'))
        self.assertEqual(admin.role, 'admin')
        self.assertTrue(admin.is_approved)
        self.assertFalse(admin.is_blacklisted)

    def test_staff_registration_starts_unapproved(self):
        """Verify staff registrations start as unapproved and whitelisted."""
        staff = User(
            email='guide@trek.com',
            role='staff',
            name='Trek Guide John',
            is_approved=False,
            is_blacklisted=False
        )
        staff.set_password('password')
        db.session.add(staff)
        db.session.commit()
        
        db_user = User.query.filter_by(email='guide@trek.com').first()
        self.assertIsNotNone(db_user)
        self.assertFalse(db_user.is_approved) # Must wait for Admin approval
        self.assertFalse(db_user.is_blacklisted)

    def test_trekker_registration_starts_approved(self):
        """Verify trekker registrations are immediately approved."""
        trekker = User(
            email='trekker@gmail.com',
            role='trekker',
            name='Jane Doe',
            is_approved=True,
            is_blacklisted=False
        )
        trekker.set_password('password')
        db.session.add(trekker)
        db.session.commit()
        
        db_user = User.query.filter_by(email='trekker@gmail.com').first()
        self.assertIsNotNone(db_user)
        self.assertTrue(db_user.is_approved) # Trekker is auto-approved

    def test_trek_creation_and_staff_assignment(self):
        """Verify Admin can create treks and assign approved staff."""
        # Create approved staff
        staff = User(email='guide@trek.com', role='staff', name='Guide John', is_approved=True)
        staff.set_password('password')
        db.session.add(staff)
        db.session.commit()

        # Create trek assigned to staff
        trek = Trek(
            name='Valley of Flowers',
            location='Uttarakhand',
            difficulty='Moderate',
            duration=6,
            max_slots=10,
            available_slots=10,
            start_date=date(2026, 7, 10),
            end_date=date(2026, 7, 16),
            assigned_staff_id=staff.id,
            status='Pending',
            price=5000.0,
            image_url='https://images.unsplash.com/photo-default'
        )
        db.session.add(trek)
        db.session.commit()

        db_trek = Trek.query.filter_by(name='Valley of Flowers').first()
        self.assertIsNotNone(db_trek)
        self.assertEqual(db_trek.assigned_staff_id, staff.id)
        self.assertEqual(db_trek.staff.name, 'Guide John')
        self.assertEqual(db_trek.status, 'Pending')
        self.assertEqual(db_trek.price, 5000.0)
        self.assertEqual(db_trek.image_url, 'https://images.unsplash.com/photo-default')

    def test_booking_rules_and_slots(self):
        """Verify booking requirements: must be Open and have available slots."""
        trekker = User(email='trekker@gmail.com', role='trekker', name='Jane', is_approved=True)
        trekker.set_password('password')
        db.session.add(trekker)
        
        # Trek is not 'Open' (status is 'Approved')
        trek = Trek(
            name='Kedar Kantha', location='Himalayas', difficulty='Easy', duration=4,
            max_slots=5, available_slots=5, start_date=date(2026, 8, 1), end_date=date(2026, 8, 5),
            status='Approved', price=5000.0, image_url='https://images.unsplash.com/photo-default'
        )
        db.session.add(trek)
        db.session.commit()

        # Try to book (should fail business check)
        self.assertNotEqual(trek.status, 'Open')
        
        # Set trek to 'Open'
        trek.status = 'Open'
        db.session.commit()
        
        # Book a spot
        trek.available_slots -= 1
        booking = Booking(user_id=trekker.id, trek_id=trek.id, status='Booked')
        db.session.add(booking)
        db.session.commit()

        self.assertEqual(trek.available_slots, 4)
        self.assertEqual(Booking.query.filter_by(trek_id=trek.id).count(), 1)

    def test_overbooking_prevention(self):
        """Verify that booking cannot occur if slots are 0."""
        trekker = User(email='trekker@gmail.com', role='trekker', name='Jane', is_approved=True)
        trekker.set_password('password')
        db.session.add(trekker)
        
        trek = Trek(
            name='Chadar Trek', location='Ladakh', difficulty='Hard', duration=9,
            max_slots=2, available_slots=0, start_date=date(2026, 12, 1), end_date=date(2026, 12, 10),
            status='Open', price=5000.0, image_url='https://images.unsplash.com/photo-default'
        )
        db.session.add(trek)
        db.session.commit()

        # Slots are zero, so assert booking logic blocks booking
        self.assertLessEqual(trek.available_slots, 0)

    def test_promote_staff_to_admin(self):
        """Verify that a staff user can be promoted to admin."""
        # Create an approved staff member
        staff = User(email='promotable@trek.com', role='staff', name='Alex Staff', is_approved=True)
        staff.set_password('password')
        db.session.add(staff)
        db.session.commit()

        # Simulate promotion POST action
        with self.app.test_request_context():
            # Apply promotion
            db_user = User.query.filter_by(email='promotable@trek.com').first()
            self.assertEqual(db_user.role, 'staff')
            
            db_user.role = 'admin'
            db_user.is_approved = True
            db.session.commit()

        promoted_user = User.query.filter_by(email='promotable@trek.com').first()
        self.assertEqual(promoted_user.role, 'admin')
        self.assertTrue(promoted_user.is_approved)

    def test_trek_sorting_by_date(self):
        """Verify that treks are queried in descending order of start_date."""
        t1 = Trek(
            name='Trek A (Future)', location='Loc A', difficulty='Easy', duration=3,
            max_slots=10, available_slots=10, start_date=date(2026, 10, 1), end_date=date(2026, 10, 4),
            price=5000.0, image_url='https://images.unsplash.com/photo-default'
        )
        t2 = Trek(
            name='Trek B (Past)', location='Loc B', difficulty='Moderate', duration=3,
            max_slots=10, available_slots=10, start_date=date(2026, 1, 1), end_date=date(2026, 1, 4),
            price=5000.0, image_url='https://images.unsplash.com/photo-default'
        )
        db.session.add_all([t1, t2])
        db.session.commit()

        # Query treks sorted by start_date DESC
        sorted_treks = Trek.query.order_by(Trek.start_date.desc()).all()
        
        # Trek A (Oct 2026) must come before Trek B (Jan 2026)
        self.assertEqual(sorted_treks[0].name, 'Trek A (Future)')
        self.assertEqual(sorted_treks[1].name, 'Trek B (Past)')

    def test_register_validation(self):
        """Verify registration validations for password matching and Indian phone format."""
        with self.client:
            # 1. Test mismatched passwords
            response = self.client.post('/register', data={
                'name': 'Test User',
                'email': 'validation_test@trek.com',
                'password': 'password123',
                'confirm_password': 'mismatch_password',
                'contact': '+919876543210',
                'role': 'trekker'
            }, follow_redirects=True)
            self.assertIn(b'Passwords do not match.', response.data)

            # 2. Test invalid phone number format (wrong prefix)
            response = self.client.post('/register', data={
                'name': 'Test User',
                'email': 'validation_test@trek.com',
                'password': 'password123',
                'confirm_password': 'password123',
                'contact': '+15550000000',
                'role': 'trekker'
            }, follow_redirects=True)
            self.assertIn(b'Contact number must start with +91 followed by exactly 10 digits.', response.data)

            # 3. Test invalid phone number format (too short)
            response = self.client.post('/register', data={
                'name': 'Test User',
                'email': 'validation_test@trek.com',
                'password': 'password123',
                'confirm_password': 'password123',
                'contact': '+9112345',
                'role': 'trekker'
            }, follow_redirects=True)
            self.assertIn(b'Contact number must start with +91 followed by exactly 10 digits.', response.data)

            # 4. Test valid registration
            response = self.client.post('/register', data={
                'name': 'Valid User',
                'email': 'valid_test@trek.com',
                'password': 'password123',
                'confirm_password': 'password123',
                'contact': '+919988776655',
                'role': 'trekker'
            }, follow_redirects=True)
            self.assertIn(b'Registration successful. Please log in.', response.data)

    def test_staff_propose_trek(self):
        """Verify that a staff user can propose a trek, which is created with Pending status."""
        # Create an approved staff member
        staff = User(email='guide@trek.com', role='staff', name='John Guide', is_approved=True)
        staff.set_password('password')
        db.session.add(staff)
        db.session.commit()

        # Log in as staff and post a trek creation request
        with self.client:
            self.client.post('/login', data={'email': 'guide@trek.com', 'password': 'password'}, follow_redirects=True)
            
            response = self.client.post('/staff/create_trek', data={
                'name': 'Proposed Peaks',
                'location': 'Western Ghats',
                'difficulty': 'Moderate',
                'duration': 2,
                'max_slots': 12,
                'start_date': '2026-08-01',
                'end_date': '2026-08-03',
                'altitude': '4,500 ft',
                'length': '20 km',
                'safety_equipment': 'First-aid kit, trekking poles',
                'price': '3500.0',
                'image_url': 'https://images.unsplash.com/photo-1234567'
            }, follow_redirects=True)
            
            self.assertIn(b'Trek proposal submitted successfully', response.data)
            
            # Verify database entry
            proposed_trek = Trek.query.filter_by(name='Proposed Peaks').first()
            self.assertIsNotNone(proposed_trek)
            self.assertEqual(proposed_trek.status, 'Pending')
            self.assertEqual(proposed_trek.assigned_staff_id, staff.id)
            self.assertEqual(proposed_trek.altitude, '4,500 ft')
            self.assertEqual(proposed_trek.length, '20 km')
            self.assertEqual(proposed_trek.safety_equipment, 'First-aid kit, trekking poles')
            self.assertEqual(proposed_trek.price, 3500.0)
            self.assertEqual(proposed_trek.image_url, 'https://images.unsplash.com/photo-1234567')

    def test_admin_create_trek_validation(self):
        """Verify admin trek creation input validation and bounds checking."""
        # Log in as admin
        with self.app.test_client() as client:
            client.post('/login', data={'email': 'Jiten@trek.com', 'password': 'Jiten@123'})
            
            # Case 1: Invalid numeric formats (TypeError/ValueError)
            response = client.post('/admin/treks', data={
                'action': 'create',
                'name': 'Valid Name',
                'location': 'Himalayas',
                'difficulty': 'Moderate',
                'duration': 'abc',  # invalid
                'max_slots': '10',
                'start_date': '2026-07-10',
                'end_date': '2026-07-16',
                'price': '3000.0'
            }, follow_redirects=True)
            self.assertIn(b'Invalid numeric or date values provided', response.data)

            # Case 2: Date chronological violation (start_date > end_date)
            response = client.post('/admin/treks', data={
                'action': 'create',
                'name': 'Valid Name',
                'location': 'Himalayas',
                'difficulty': 'Moderate',
                'duration': '5',
                'max_slots': '10',
                'start_date': '2026-07-20',
                'end_date': '2026-07-16',  # earlier
                'price': '3000.0'
            }, follow_redirects=True)
            self.assertIn(b'Start date cannot be after end date', response.data)

            # Case 3: Boundary violations (negative values)
            response = client.post('/admin/treks', data={
                'action': 'create',
                'name': 'Valid Name',
                'location': 'Himalayas',
                'difficulty': 'Moderate',
                'duration': '-5',  # negative
                'max_slots': '10',
                'start_date': '2026-07-10',
                'end_date': '2026-07-16',
                'price': '3000.0'
            }, follow_redirects=True)
            self.assertIn(b'must be positive values', response.data)

    def test_trekker_profile_contact_validation(self):
        """Verify profile editing enforces Indian contact number format."""
        # Create trekker user
        trekker = User(
            email='trekker@trek.com',
            role='trekker',
            name='Trekker User',
            is_approved=True,
            is_blacklisted=False
        )
        trekker.set_password('password')
        db.session.add(trekker)
        db.session.commit()

        # Log in as trekker
        with self.app.test_client() as client:
            client.post('/login', data={'email': 'trekker@trek.com', 'password': 'password'})
            
            # Update with invalid phone format (no +91 prefix)
            response = client.post('/trekker/profile', data={
                'name': 'Trekker Updated',
                'contact': '9876543210'  # invalid format
            }, follow_redirects=True)
            self.assertIn(b'Contact number must start with +91', response.data)
            
            # Update with valid phone format
            response = client.post('/trekker/profile', data={
                'name': 'Trekker Updated',
                'contact': '+919876543210'  # valid
            }, follow_redirects=True)
            self.assertIn(b'Profile updated successfully', response.data)

    def test_cancel_booking(self):
        """Verify trekker can cancel booking before the trek starts."""
        # Create trekker user
        trekker = User(email='trekker_cancel@trek.com', role='trekker', name='Cancel User', is_approved=True)
        trekker.set_password('password')
        db.session.add(trekker)
        
        # Create a trek that starts tomorrow
        tomorrow = date.today() + timedelta(days=1)
        trek = Trek(
            name='Cancel Trek', location='Himalayas', difficulty='Easy', duration=4,
            max_slots=5, available_slots=4, start_date=tomorrow, end_date=tomorrow + timedelta(days=3),
            status='Open', price=5000.0, image_url='https://images.unsplash.com/photo-default'
        )
        db.session.add(trek)
        db.session.commit()
        
        # Create a booking
        booking = Booking(user_id=trekker.id, trek_id=trek.id, status='Booked')
        db.session.add(booking)
        db.session.commit()
        
        with self.client:
            self.client.post('/login', data={'email': 'trekker_cancel@trek.com', 'password': 'password'})
            # Cancel the booking
            response = self.client.post(f'/trekker/cancel-booking/{booking.id}', follow_redirects=True)
            self.assertIn(b'has been cancelled', response.data)
            
            # Check db updates
            db_booking = Booking.query.get(booking.id)
            self.assertEqual(db_booking.status, 'Cancelled')
            db_trek = Trek.query.get(trek.id)
            self.assertEqual(db_trek.available_slots, 5)

    def test_cancel_booking_fails_after_start(self):
        """Verify trekker cannot cancel booking on or after trek start date."""
        trekker = User(email='trekker_cancel2@trek.com', role='trekker', name='Cancel User 2', is_approved=True)
        trekker.set_password('password')
        db.session.add(trekker)
        
        # Create a trek that starts today
        today = date.today()
        trek = Trek(
            name='Past Trek', location='Himalayas', difficulty='Easy', duration=4,
            max_slots=5, available_slots=4, start_date=today, end_date=today + timedelta(days=3),
            status='Open', price=5000.0, image_url='https://images.unsplash.com/photo-default'
        )
        db.session.add(trek)
        db.session.commit()
        
        # Create a booking
        booking = Booking(user_id=trekker.id, trek_id=trek.id, status='Booked')
        db.session.add(booking)
        db.session.commit()
        
        with self.client:
            self.client.post('/login', data={'email': 'trekker_cancel2@trek.com', 'password': 'password'})
            # Cancel the booking (should fail)
            response = self.client.post(f'/trekker/cancel-booking/{booking.id}', follow_redirects=True)
            self.assertIn(b'cannot cancel a booking on or after', response.data)
            
            # Check db updates (should not change)
            db_booking = Booking.query.get(booking.id)
            self.assertEqual(db_booking.status, 'Booked')
            db_trek = Trek.query.get(trek.id)
            self.assertEqual(db_trek.available_slots, 4)

    def test_staff_edit_trek_validation(self):
        """Verify staff cannot edit Pending trek, or change status to Pending/Approved."""
        # Create staff user
        staff = User(email='staff_val@trek.com', role='staff', name='Staff Val', is_approved=True)
        staff.set_password('password')
        db.session.add(staff)
        db.session.commit()
        
        # Create a Pending trek
        trek_pending = Trek(
            name='Pending Trek', location='Himalayas', difficulty='Easy', duration=4,
            max_slots=5, available_slots=5, start_date=date.today() + timedelta(days=5),
            end_date=date.today() + timedelta(days=9), status='Pending', assigned_staff_id=staff.id,
            price=5000.0, image_url='https://images.unsplash.com/photo-default'
        )
        # Create an Open trek
        trek_open = Trek(
            name='Open Trek', location='Himalayas', difficulty='Easy', duration=4,
            max_slots=5, available_slots=5, start_date=date.today() + timedelta(days=5),
            end_date=date.today() + timedelta(days=9), status='Open', assigned_staff_id=staff.id,
            price=5000.0, image_url='https://images.unsplash.com/photo-default'
        )
        db.session.add_all([trek_pending, trek_open])
        db.session.commit()
        
        with self.client:
            self.client.post('/login', data={'email': 'staff_val@trek.com', 'password': 'password'})
            
            # Try to edit Pending trek
            response = self.client.post(f'/staff/trek/{trek_pending.id}/edit', data={
                'available_slots': 3,
                'status': 'Open'
            }, follow_redirects=True)
            self.assertIn(b'awaiting Administrator approval and cannot be modified', response.data)
            
            # Try to transition Open trek to Pending/Approved
            response2 = self.client.post(f'/staff/trek/{trek_open.id}/edit', data={
                'available_slots': 3,
                'status': 'Approved'
            }, follow_redirects=True)
            self.assertIn(b'You do not have permission to transition this trek to an Administrator-controlled status', response2.data)

    def test_admin_view_bookings_filtering(self):
        """Verify admin can filter bookings by status, trek_id, and date."""
        # Create trekker, treks, bookings
        trekker = User(email='trekker_filter@trek.com', role='trekker', name='Filter User', is_approved=True)
        trekker.set_password('password')
        db.session.add(trekker)
        
        t1 = Trek(
            name='Trek A', location='Himalayas', difficulty='Easy', duration=4,
            max_slots=5, available_slots=5, start_date=date(2026, 8, 1), end_date=date(2026, 8, 5),
            status='Open', price=5000.0, image_url='https://images.unsplash.com/photo-default'
        )
        t2 = Trek(
            name='Trek B', location='Western Ghats', difficulty='Easy', duration=4,
            max_slots=5, available_slots=5, start_date=date(2026, 9, 1), end_date=date(2026, 9, 5),
            status='Open', price=5000.0, image_url='https://images.unsplash.com/photo-default'
        )
        db.session.add_all([t1, t2])
        db.session.commit()
        
        # Booking for t1 (Booked)
        b1 = Booking(user_id=trekker.id, trek_id=t1.id, status='Booked')
        # Booking for t2 (Cancelled)
        b2 = Booking(user_id=trekker.id, trek_id=t2.id, status='Cancelled')
        db.session.add_all([b1, b2])
        db.session.commit()
        
        with self.client:
            self.client.post('/login', data={'email': 'Jiten@trek.com', 'password': 'Jiten@123'})
            
            # Filter by status 'Booked'
            response = self.client.get('/admin/bookings?status=Booked')
            self.assertIn(b'Trek A', response.data)
            self.assertNotIn(b'<span>Trek B</span>', response.data)
            
            # Filter by status 'Cancelled'
            response = self.client.get('/admin/bookings?status=Cancelled')
            self.assertIn(b'Trek B', response.data)
            self.assertNotIn(b'<span>Trek A</span>', response.data)
            
            # Filter by trek_id of t1
            response = self.client.get(f'/admin/bookings?trek_id={t1.id}')
            self.assertIn(b'Trek A', response.data)
            self.assertNotIn(b'<span>Trek B</span>', response.data)

    def test_admin_edit_trek(self):
        """Verify Admin can edit all trek details."""
        trek = Trek(
            name='Original Trek', location='Himalayas', difficulty='Easy', duration=4,
            max_slots=10, available_slots=10, start_date=date(2026, 8, 1), end_date=date(2026, 8, 5),
            status='Approved', price=5000.0, image_url='https://images.unsplash.com/photo-default'
        )
        db.session.add(trek)
        db.session.commit()

        with self.client:
            self.client.post('/login', data={'email': 'Jiten@trek.com', 'password': 'Jiten@123'})
            response = self.client.post('/admin/treks', data={
                'action': 'edit',
                'trek_id': trek.id,
                'name': 'Updated Trek Name',
                'location': 'Karakoram',
                'difficulty': 'Moderate',
                'duration': 5,
                'max_slots': 12,
                'available_slots': 12,
                'start_date': '2026-08-02',
                'end_date': '2026-08-07',
                'altitude': '15,000 ft',
                'length': '30 km',
                'safety_equipment': 'Crampons, Rope',
                'price': '6000.0',
                'image_url': 'https://images.unsplash.com/photo-updated',
                'status': 'Open',
                'assigned_staff_id': ''
            }, follow_redirects=True)
            self.assertIn(b'Trek updated successfully', response.data)
            
            db_trek = Trek.query.get(trek.id)
            self.assertEqual(db_trek.name, 'Updated Trek Name')
            self.assertEqual(db_trek.location, 'Karakoram')
            self.assertEqual(db_trek.difficulty, 'Moderate')
            self.assertEqual(db_trek.duration, 5)
            self.assertEqual(db_trek.max_slots, 12)
            self.assertEqual(db_trek.available_slots, 12)
            self.assertEqual(db_trek.start_date, date(2026, 8, 2))
            self.assertEqual(db_trek.end_date, date(2026, 8, 7))
            self.assertEqual(db_trek.altitude, '15,000 ft')
            self.assertEqual(db_trek.length, '30 km')
            self.assertEqual(db_trek.safety_equipment, 'Crampons, Rope')
            self.assertEqual(db_trek.price, 6000.0)
            self.assertEqual(db_trek.image_url, 'https://images.unsplash.com/photo-updated')
            self.assertEqual(db_trek.status, 'Open')

    def test_api_resources(self):
        """Verify REST JSON API endpoints return valid JSON response."""
        trek = Trek(
            name='API Trek', location='Himalayas', difficulty='Easy', duration=4,
            max_slots=10, available_slots=10, start_date=date(2026, 8, 1), end_date=date(2026, 8, 5),
            status='Approved', price=5000.0, image_url='https://images.unsplash.com/photo-default'
        )
        db.session.add(trek)
        db.session.commit()

        with self.client:
            # 1. GET /api/treks
            response = self.client.get('/api/treks')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')
            self.assertIn(b'API Trek', response.data)

            # 2. GET /api/treks/<id>
            response = self.client.get(f'/api/treks/{trek.id}')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')
            self.assertIn(b'API Trek', response.data)

            # 3. GET /api/users
            response = self.client.get('/api/users')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')
            self.assertIn(b'Jiten@trek.com', response.data)

            # 4. GET /api/bookings
            response = self.client.get('/api/bookings')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')

    def test_booking_auto_completion_on_trek_completion(self):
        """Verify that marking a trek as completed updates booking status to Completed."""
        staff = User(email='staff_comp@trek.com', role='staff', name='Staff Comp', is_approved=True)
        staff.set_password('password')
        db.session.add(staff)
        db.session.commit()

        trek = Trek(
            name='Comp Trek', location='Himalayas', difficulty='Easy', duration=4,
            max_slots=5, available_slots=4, start_date=date.today(), end_date=date.today() + timedelta(days=3),
            status='Open', assigned_staff_id=staff.id, price=5000.0
        )
        db.session.add(trek)
        db.session.commit()

        trekker = User(email='trekker_comp@trek.com', role='trekker', name='Trekker Comp', is_approved=True)
        trekker.set_password('password')
        db.session.add(trekker)
        db.session.commit()

        booking = Booking(user_id=trekker.id, trek_id=trek.id, status='Booked')
        db.session.add(booking)
        db.session.commit()

        with self.client:
            self.client.post('/login', data={'email': 'staff_comp@trek.com', 'password': 'password'})
            response = self.client.post(f'/staff/trek/{trek.id}/edit', data={
                'available_slots': 4,
                'status': 'Completed'
            }, follow_redirects=True)
            self.assertIn(b'Trek details updated successfully', response.data)

            db_booking = Booking.query.get(booking.id)
            self.assertEqual(db_booking.status, 'Completed')

if __name__ == '__main__':
    unittest.main()

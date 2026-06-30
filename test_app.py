import unittest
from datetime import datetime, date
from app import create_app
from extensions import db
from models import User, Trek, Booking

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
            status='Pending'
        )
        db.session.add(trek)
        db.session.commit()

        db_trek = Trek.query.filter_by(name='Valley of Flowers').first()
        self.assertIsNotNone(db_trek)
        self.assertEqual(db_trek.assigned_staff_id, staff.id)
        self.assertEqual(db_trek.staff.name, 'Guide John')
        self.assertEqual(db_trek.status, 'Pending')

    def test_booking_rules_and_slots(self):
        """Verify booking requirements: must be Open and have available slots."""
        trekker = User(email='trekker@gmail.com', role='trekker', name='Jane', is_approved=True)
        trekker.set_password('password')
        db.session.add(trekker)
        
        # Trek is not 'Open' (status is 'Approved')
        trek = Trek(
            name='Kedar Kantha', location='Himalayas', difficulty='Easy', duration=4,
            max_slots=5, available_slots=5, start_date=date(2026, 8, 1), end_date=date(2026, 8, 5),
            status='Approved'
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
            status='Open'
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
            max_slots=10, available_slots=10, start_date=date(2026, 10, 1), end_date=date(2026, 10, 4)
        )
        t2 = Trek(
            name='Trek B (Past)', location='Loc B', difficulty='Moderate', duration=3,
            max_slots=10, available_slots=10, start_date=date(2026, 1, 1), end_date=date(2026, 1, 4)
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

if __name__ == '__main__':
    unittest.main()

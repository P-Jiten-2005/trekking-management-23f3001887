from app import create_app
from extensions import db
from models import User

app = create_app()
with app.app_context():
    db.create_all()
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
        db.session.commit()
        print("Admin user seeded successfully.")
    else:
        print("Admin user already exists.")

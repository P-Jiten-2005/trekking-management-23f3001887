from app import create_app
from app.extensions import db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        from app.models import User
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
            db.session.commit()
            print("Admin user seeded.")
    app.run(host='127.0.0.1', port = 1234,debug=True)

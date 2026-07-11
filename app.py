from flask import Flask, render_template
from config import Config
from extensions import db, login_manager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from routes.admin import admin_bp
    app.register_blueprint(admin_bp)

    from routes.staff import staff_bp
    app.register_blueprint(staff_bp)

    from routes.trekker import trekker_bp
    app.register_blueprint(trekker_bp)

    @app.route('/')
    def index():
        from models import Trek
        featured_treks = Trek.query.filter(Trek.status.in_(['Approved', 'Open'])).limit(3).all()
        return render_template('index.html', featured_treks=featured_treks)

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
        from models import User
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
    app.run(debug=True)

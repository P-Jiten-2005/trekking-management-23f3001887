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

    from models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    from admin.routes import admin_bp
    app.register_blueprint(admin_bp)

    from staff.routes import staff_bp
    app.register_blueprint(staff_bp)

    from trekker.routes import trekker_bp
    app.register_blueprint(trekker_bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app

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

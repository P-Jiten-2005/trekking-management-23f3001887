from flask import Flask, render_template
from app.config import Config
from app.extensions import db, login_manager

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from app.models import User
    
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

    from routes.api import api_bp
    app.register_blueprint(api_bp)

    @app.route('/')
    def index():
        from app.models import Trek
        featured_treks = Trek.query.filter(Trek.status.in_(['Approved', 'Open'])).limit(3).all()
        return render_template('index.html', featured_treks=featured_treks)

    return app

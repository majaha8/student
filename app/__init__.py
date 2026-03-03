from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate

# from flask_sqlalchemy import SQLAlchemy
from app.extension import db
from app.routes import main
from app.routes.category.category import cat_bp

from .auth.auth import auth_bp

# db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///student.db"
    app.config["SECRET_KEY"] = "secret"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = "auth.login"

    # Register routes

    app.register_blueprint(auth_bp)
    app.register_blueprint(main)
    app.register_blueprint(cat_bp, url_prefix="/category")

    # Import models so Flask-Migrate sees them
    from .model import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    return app

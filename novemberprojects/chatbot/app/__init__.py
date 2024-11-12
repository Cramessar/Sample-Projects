from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
login = LoginManager()
login.login_view = 'main.login'
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    login.init_app(app)
    csrf.init_app(app)

    # Register Blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app

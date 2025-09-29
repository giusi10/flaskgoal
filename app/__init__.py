from dotenv import load_dotenv
load_dotenv()
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
mail = Mail()
login.login_view = 'routes.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)

    from app import models
    from app.routes import bp as routes_bp
    from app.api import bp as api_bp

    app.register_blueprint(routes_bp)
    app.register_blueprint(api_bp)

    return app
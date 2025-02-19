from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_argon2 import Argon2
from flask_login import LoginManager
from flask_mail import Mail
from enigma.config import Config

db = SQLAlchemy()
argon2 = Argon2()
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    argon2.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from enigma.users.routes import users
    from enigma.posts.routes import posts
    from enigma.main.routes import main
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)

    return app
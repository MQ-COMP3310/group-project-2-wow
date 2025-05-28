from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from pathlib import Path

db = SQLAlchemy()


def create_app():
  app = Flask(__name__)

  app.config["SECRET_KEY"] = "secret-key-do-not-reveal"
  app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///photos.db"
  CWD = Path(os.path.dirname(__file__))
  app.config["UPLOAD_DIR"] = CWD / "uploads"

  db.init_app(app)

  # Import main blueprint for the main routes and register it with the Flask app
  from .main import main as main_blueprint
  app.register_blueprint(main_blueprint)

  # Import auth blueprint for login/signup/logout routes and register it with the Flask app
  from .auth import auth as auth_blueprint
  app.register_blueprint(auth_blueprint)

  # Import the user model i.e. the structure for users in the database
  from .models import User

  # Create an instance of the Loginmanager which is being used to handle the user sessions and then set the login page URL to auth.login
  login_manager = LoginManager()
  login_manager.login_view = "auth.login"

  # Return corresponding user object from the session given a user id
  @login_manager.user_loader
  def load_user(user_id):
      return User.query.get(int(user_id))

  # Initialise the LoginManager
  login_manager.init_app(app)

  return app
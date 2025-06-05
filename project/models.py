from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# New User Class
class User(UserMixin, db.Model):
  # Includes an id (pk), username and password hash (which uses the functions from wekzueg library)
  id = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String(50), unique = True, nullable = False)
  password_hash = db.Column(db.String(128), nullable = False)
  isAdmin = db.Column(db.Boolean, default=False)

  # Method to set user to admin
  def set_admin(self):
    self.isAdmin = True

  # Given a password, hash the password (scrypt by default) before saving it (which will then be stored in the DB)
  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  # Given a password (plaintext), hash the password then return a boolean depending on if the object's (user's) password_hash field matches
  def check_password(self, password):
    return check_password_hash(self.password_hash, password)

# Updated Photo Class
# Includes a foreign key now for the user_id and is required
# Each photo now has a field for a user_id so each photo gets mapped to a user and different users can't access photos that aren't theirs
class Photo(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(50), nullable = False)
  caption = db.Column(db.String(250), nullable = False)
  file = db.Column(db.String(250), nullable = False)
  description = db.Column(db.String(600), nullable = True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

from flask import (
  Blueprint,
  render_template,
  request,
  flash,
  redirect,
  url_for,
  send_from_directory,
  current_app
)
from flask_login import login_required, current_user
from .models import Photo, User
from sqlalchemy import asc, text
from . import db
import os

# Create the main blueprint
main = Blueprint("main", __name__)

# Route for homepage
@main.route("/")
def homepage():
  # Check if the user is logged in and if so then query/filter photos alphabetically (only the ones that match the current user's id)
  # Then return index.html with the photos that were queried from the DB
  # If user is admin then return all photos
  if current_user.is_authenticated:
    if current_user.is_admin:
        photos = db.session.query(Photo).order_by(asc(Photo.file)).all()
    else:
       photos = db.session.query(Photo).filter_by(user_id=current_user.id).order_by(asc(Photo.file)).all()
  else:
    photos = []
  return render_template("index.html", photos = photos)


# Route for uploads given an image name
@main.route("/uploads/<name>")
def display_file(name):
  return send_from_directory(current_app.config["UPLOAD_DIR"], name)


# Route for upload page with GET and POST requests
@main.route("/upload/", methods = ["GET", "POST"])
# User is required to be logged in, comes from the LoginManager instance --> this will auto redirect to "auth.login" (set in init.py) if the user isn't logged in
@login_required
def newPhoto():
  # If the request is a POST method then get the photo details that the user has entered and upload it to the DB
  if request.method == "POST":
    file = None
    if "fileToUpload" in request.files:
      file = request.files.get("fileToUpload")
    else:
      flash("Invalid request!", "error")

    if not file or not file.filename:
      flash("No file selected!", "error")
      return redirect(request.url)

    filepath = os.path.join(current_app.config["UPLOAD_DIR"], file.filename)
    file.save(filepath)

    # current_user.id is the new field used for the auth mechanism
    newPhoto = Photo(
      name = current_user.username,
      caption = request.form["caption"],
      description = request.form["description"],
      file = file.filename,
      user_id = current_user.id,
    )

    flash('New Photo %s Successfully Created' % newPhoto.name)

    db.session.add(newPhoto)
    db.session.commit()

    # Return the user to the home page
    return redirect(url_for("main.homepage"))
  # If it's a GET request then return upload.html
  else:
    return render_template("upload.html")


# Route for editing a photo given the photo id integer (accepts GET and POST requests + login is required)
@main.route("/photo/<int:photo_id>/edit/", methods = ["GET", "POST"])
@login_required
def editPhoto(photo_id):
  # Query the DB to find the photo that needs to be edited and return a 404 if it can't be found (note the filter_by method also includes the user_id field now)
  # If user is admin, return query for all photos otherwise only the ones that the user owns
  if current_user.is_admin:
    editedPhoto = db.session.query(Photo).filter_by(id = photo_id).first_or_404()
  else:
    editedPhoto = (db.session.query(Photo).filter_by(id = photo_id, user_id = current_user.id).first_or_404())
  
  # Update the photo if the request is POST and photo_id is valid (given form details)
  if request.method == "POST":
    editedPhoto.name = request.form['user']
    editedPhoto.caption = request.form["caption"]
    editedPhoto.description = request.form["description"]

    db.session.add(editedPhoto)
    db.session.commit()

    flash('Photo Successfully Edited %s' % editedPhoto.name)
    return redirect(url_for("main.homepage"))
    # If the request is GET then return edit.html and set the photo to the editiedPhoto
  else:
    return render_template("edit.html", photo = editedPhoto)


# Handler for the photo deleting route (accepts GET and POST requests + login is required)
@main.route("/photo/<int:photo_id>/delete/", methods = ["GET", "POST"])
@login_required
def deletePhoto(photo_id):
  # Query the DB to find the photo that needs to be deleted and if it can't be found then return a 404
  # If user is admin then return all photos
  if current_user.is_admin:
    photo = db.session.query(Photo).filter_by(id = photo_id).first_or_404()
  else:
    photo = (db.session.query(Photo).filter_by(id = photo_id, user_id = current_user.id).first_or_404())
  
  # If photo has been found (meaning the photo_id is valid and user_id is valid) then delete it, update the DB and return to the home page
  filepath = os.path.join(current_app.config["UPLOAD_DIR"], photo.file)

  if os.path.exists(filepath):
    os.unlink(filepath)

  db.session.delete(photo)
  db.session.commit()

  flash('Photo id %s Successfully Deleted' % photo_id)
  return redirect(url_for("main.homepage"))

# Route for GET request to admin page where they can modify users
@main.route("/admin/users/", methods=["GET"])
@login_required
def adminUsersList():
    # If user isn't admin then flash and redirect them to the home page
    if not current_user.is_admin:
        flash('Admin access required.')
        return redirect(url_for("main.homepage"))
    # If user is admin then query the DB for all users and render the adminPanel.html template with the query response
    all_users = db.session.query(User).all()
    return render_template("adminPanel.html", users=all_users)

# Route for POST request to admin page where they can modify users
@main.route("/admin/users/<int:user_id>", methods = ["POST"])
@login_required
def adminUsersAction(user_id):
  # If the current user isn't admin then flash them with a warning and redirect them to the homepage
  if not current_user.is_admin:
    flash('Cannot access page, admin privileges required.')
    return redirect(url_for("main.homepage"))
  
  # If user is admin the query and find the user object that needs to be modified and find out what the action was using the form data
  userToModify = db.session.query(User).filter_by(id = user_id).first_or_404()
  modificationAction = request.form['action']

  # If action was delete then first check that the user isn't deleting themselves and then delete the user specified
  if modificationAction == "delete":
    if userToModify.id == current_user.id:
      flash('Admins cannot delete themselves.', 'error')
      return redirect(url_for("adminPanel.html"))
    db.session.delete(userToModify)
  
  # If the action was to promote a user then first check that the user isn't already an admin and the give them admin privileges
  elif modificationAction == "promote":
    if userToModify.is_admin:
      flash('User is already admin')
      return redirect(url_for("adminPanel.html"))
    else:
      userToModify.set_admin()
  
  # If any other action was specified then warn the user and redirect them to the admin panel
  else:
      flash('Invalid action.')
      return redirect(url_for("adminPanel.html"))

  # Commit all changes to the DB and let the user know that this has been successfully done
  db.session.commit()
  flash('User Access Successfully Modified %s' % userToModify.username)
  return redirect(url_for("main.homepage"))
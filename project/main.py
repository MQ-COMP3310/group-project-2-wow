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
from .models import Photo
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
  photos = (
    db.session.query(Photo).filter_by(user_id = current_user.id).order_by(asc(Photo.file)) if current_user.is_authenticated else []
  )
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
  editedPhoto = (
    db.session.query(Photo)
    .filter_by(id = photo_id, user_id = current_user.id)
    .first_or_404()
  )
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
  photo = (
    db.session.query(Photo)
    .filter_by(id = photo_id, user_id = current_user.id)
    .first_or_404()
  )

  # If photo has been found (meaning the photo_id is valid and user_id is valid) then delete it, update the DB and return to the home page
  filepath = os.path.join(current_app.config["UPLOAD_DIR"], photo.file)

  if os.path.exists(filepath):
    os.unlink(filepath)

  db.session.delete(photo)
  db.session.commit()

  flash('Photo id %s Successfully Deleted' % photo_id)
  return redirect(url_for("main.homepage"))

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db

# Create a blueprint called auth --> gets used in __init__.py
auth = Blueprint("auth", __name__)

# Handles the login page route with GET and POST methods
@auth.route("/login", methods = ["GET", "POST"])
def login():
	# If the request is POST grab the username and password and see if first the username matches and then the password
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]

		# Get the User instance
		user = User.query.filter_by(username = username).first()

		# If the User instance isn't empty (i.e. no user with given username) and the password matches (using custom hash function) then log the user in
		# and redirect them to the homepage
		if user and user.check_password(password):
			login_user(user)
			flash("Logged in successfully.")
			return redirect(url_for("main.homepage"))
		
		# Flash if username or password is invalid
		flash("Invalid username or password.")
		return redirect(url_for("main.homepage"))
	else:
		# Return the login.html page if the request is GET
		return render_template("login.html")


# Handles the signup page route with GET and POST methods
@auth.route("/signup", methods = ["GET", "POST"])
def signup():
	# If the request is POST check if the username already exists and if it doesn't then add the user to the DB
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]

		if username == "" or password == "":
			flash("Invalid username or password field.")
			return redirect(url_for("auth.signup"))

		# If the username already exists then let the user know and redirect them back to the signup page
		if User.query.filter_by(username = username).first():
			flash("Username already exists.")
			return redirect(url_for("auth.signup"))
		
		# Username is valid so create the new user given the user details (generate hash for the password) and add it to the DB
		new_user = User(username = username)
		new_user.set_password(password)
		db.session.add(new_user)
		db.session.commit()
		flash("Account created.")
		return redirect(url_for("auth.login"))
	else:
		# If the request is GET then return the signup.html page
		return render_template("signup.html")


# Handles logging out --> Call the logout_user() function and then redirect them to the main homepage
@auth.route("/logout")
@login_required
def logout():
	logout_user()
	flash("Logged out.")
	return redirect(url_for("main.homepage"))
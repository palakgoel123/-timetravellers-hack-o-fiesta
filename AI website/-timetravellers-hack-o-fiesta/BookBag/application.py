import os
import re

from flask import Flask, session, request, redirect, render_template
from flask_session import Session
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Change the databse link
uri = os.getenv("DATABASE_URL")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

# Set up database
engine = create_engine(uri)
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    '''
    Render the Welcome Webpage
    '''
    return render_template("index.html")


@app.route("/register", methods = ["GET", "POST"])
def register():
    '''
    Registeration Method
    '''

    # Logout any logged-in user
    session.clear()

    # The form will be submitted only when a POST request is made
    if request.method == 'POST':

        # no name provided
        if not request.form.get('name'):
            return render_template("error.html", message = "Must provide your username")

        # no password provided
        if not request.form.get('password'):
            return render_template("error.html", message = "Must provide your password")

        # the passwords in the two fields doesn't match with each other
        if request.form.get('password') != request.form.get('re_password'):
            return render_template("error.html", message = "The password don't match")

        # taking the username from the form
        username = request.form.get('name')

        user = db.execute("SELECT * FROM users WHERE username = :username",
        { "username": username}).fetchone()

        # username is unique for each user
        if user is not None :
            return render_template("error.html", message = "Username already exists \n Try another!!")

        # taking the password from the form
        password = request.form.get('password')

        # hashing the password
        password = generate_password_hash(password, "sha256")

        # inserting the username and password into the database
        db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
                  {"username": username, "password" : password})
        db.commit()

        # after registeration login is required
        return redirect("/login")
    # When a GET request is made render the "register.html" template
    else :
        return render_template("register.html")


@app.route("/login", methods = ["GET", "POST"])
def login():
    '''
    Login Method
    '''

    # logout and logged-in user
    session.clear()

    # The form will be submitted only when a POST request is made
    if request.method == 'POST':

        # checking if name not provided
        if not request.form.get('name'):
            return render_template("error.html", message = "Must provide your username")

        # checking if password not provided
        if not request.form.get('password'):
            return render_template("error.html", message = "Must provide your password")

        # taking the username and password form the login form
        username = request.form.get('name')
        password = request.form.get('password')

        # searching for the user in the databse
        user = db.execute("SELECT * FROM users WHERE username = :username ",
                         {"username":username}).fetchone()

        # is no user found with the given username
        if user is None:
            return render_template("error.html", message = "No such username exists. Try Again!!")

        # checking whether the password is correct or not
        user_P = user.password
        valid = check_password_hash(user_P, password)
        if not valid :
            return render_template("error.html", message = "Incorrect password")

        # setting the current session user_name to username
        session["user_name"] = user.username

        # setting the current session user_id to the id of user
        session["user_id"] = user.id

        # rendering the search template
        return redirect("/search")

    # When a GET request is made render the "login.html" template
    else :
        return render_template("login.html")

@app.route("/logout")
def logout():
    '''
    Logout Method
    '''

    # clearing the session i.e. removing all the previously stored session values
    session.clear()

    # rendering the welcome page
    return redirect("/")

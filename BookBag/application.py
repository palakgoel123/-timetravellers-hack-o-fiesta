import os
import re

from flask import Flask, session, request, redirect, render_template
from flask_session import Session
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import scoped_session, sessionmaker
from functools import wraps


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

def login_required(f):
    '''
    For certain routes making the login required
    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    '''
    @wraps(f)
    def decorated_function(*args, **kwargs):

        # if no user is logged in
        if not session.get("user_id"):
            # redirect to login page
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

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
@login_required
def logout():
    '''
    Logout Method
    '''

    # clearing the session i.e. removing all the previously stored session values
    session.clear()

    # rendering the welcome page
    return redirect("/")

@app.route("/search", methods = ["POST", "GET"])
@login_required
def search():
    '''
    Searching for Books
    '''

    # POST method allowed for searching
    if request.method == "POST" :

        # checking if an empty string is submitted
        if request.form.get('book') is None:
            return render_template("error.html", message="Cannot search for empty string")

        # adding the '%' symbol for matching the given string with the possible values
        book = '%' + request.form.get('book') + '%'

        book = book.title()

        # searching for the books matching the input provided (max 16)
        books = db.execute("SELECT * FROM books WHERE isbn LIKE :book OR title LIKE :book OR author LIKE :book LIMIT 16",
                            {"book" : book }).fetchall()

        # if no book found
        if books == None:
            return render_template("error.html", message = "We could not find a book with that description")

        name = session["user_name"]

        # render the "books.html" to displaythe list of avaliable books
        return render_template("books.html", books = books, name = name )

    # GET method renders "home.html" i.e. the search form
    else :
        return render_template("home.html")



@app.route("/book/<string:isbn>", methods = ["GET", "POST"])
@login_required
def book(isbn):

    # when the review form is submitted
    if request.method == "POST":

        # taking the user-id of the currently logged-in user
        user = session["user_id"]

        # getting the rating and the comment from the uer-submitted form
        rating = request.form.get('rating')
        comment = request.form.get('comment')

        # fetching the book-id for the book with the given isbn no.
        book_id = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn" : isbn}).fetchone()
        book_id = book_id.id

        # converting the rating into an integer
        rating = int(rating)

        # inserting the values of rating and the comment given by the user
        db.execute("INSERT INTO reviews (book_id, user_id, content, ratings) VALUES (:book_id, :user_id, :content, :ratings)",
        {"book_id" : book_id, "user_id" : user, "content" : comment, "ratings" : rating})
        db.commit()

        # redirecting to the same function but not through POST request along with the reviews added
        return redirect("/book/" + isbn)

    else :

        # fetching the book with the given isbn no.
        book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn" : isbn}).fetchone()

        #fetching all the reviews for the given book
        reviews = db.execute("SELECT * FROM reviews WHERE book_id = :book_id ORDER BY ratings DESC limit 5",
        {"book_id" : book.id}).fetchall()

        # image url for the book
        img = f"http://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"

        # rendering the bookinfo.html file to diaply the book details along with the respective reviews
        return render_template("bookinfo.html" , book = book, reviews = reviews, img = img)

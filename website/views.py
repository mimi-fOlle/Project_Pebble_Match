from flask import Blueprint, render_template

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("index.html")

@views.route('/login.html')
def login():
    return render_template("login.html")

@views.route('/signup.html')
def sign_up():
    return render_template("signup.html")
from flask import Blueprint, render_template, flash


views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("index.html")

@views.route('/login.html', methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@views.route('/signup.html', methods=['GET', 'POST'])
def signup():
    return render_template("signup.html")
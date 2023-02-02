from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from flask_login import login_required, logout_user

auth = Blueprint('auth', __name__)


@auth.route('/login.html', methods=['GET', 'POST'])
def login():
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    database = {
        "user1": "pass1",
        "user2": "pass2",
        "user3": "pass3"
    }
    if email in database and database[email] == password:
        print("Access granted")
    else:
        print("Access denied")
        
    return render_template('home.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup.html', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Implement logic to store user information in database
        return 'Successfully registered user with username: {}'.format(email)
    return render_template('signup.html')

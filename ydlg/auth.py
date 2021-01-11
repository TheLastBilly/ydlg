from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get("username")
    password = request.form.get("password")
    remember = True if request.form.get("remember") == "remember" else False

    if not username or not password:
        return render_template('login.html', message="Please enter valid credentials")
    
    user = User.query.filter_by(name=username).first()
    
    if user is None or not check_password_hash(user.password, password):
            return render_template('login.html', message="Invalid username/password")
    
    login_user(user, remember=remember)

    return redirect( url_for('main.index') )

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
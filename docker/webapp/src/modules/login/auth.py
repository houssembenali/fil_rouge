from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from .. import db
import wordings

auth = Blueprint('auth', __name__, template_folder='templates')

PROJECTS_PAGE_LIST_PROJETS = "projects.page_list_projets"

@auth.route('/login')
def login():
    if  current_user.is_authenticated: 
        return redirect(url_for(PROJECTS_PAGE_LIST_PROJETS))
    else:
        return render_template('login.html')

@auth.route('/signup')
def signup():
    if current_user.is_authenticated: 
        return redirect(url_for(PROJECTS_PAGE_LIST_PROJETS))
    else:
        return render_template('signup.html')

@auth.route('/login', methods=['POST'])
def login_post():
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    name = request.form.get('name')
    user = User.query.filter_by(name=name).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash(wordings.LOGIN_INVALIDE)
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for(PROJECTS_PAGE_LIST_PROJETS))

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash(wordings.EMAIL_DEJA_UTILISE)
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

from flask import Blueprint, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.user.models import User

main = Blueprint('main', __name__)


@main.get('/')
def main_page():
    return render_template('main/index.html')


@main.get('/login/')
def login_page():
    """
    Login page
    :return: rendered template (main/login.html)
    """
    return render_template('main/login.html')


@main.post('/login/')
def login():
    """
    Authentication by password
    :return: redirect to events page
    """
    username = request.form.get('username')
    password = request.form.get('password')
    query = db.select(User).where(User.username == username)
    user = db.session.execute(query).scalar()
    if user:
        password_hash = generate_password_hash(user.password)
        if check_password_hash(password_hash, password):
            session['username'] = username
            session['user_id'] = user.id
            session['full_name'] = f'{user.first_name} {user.last_name}'
            return redirect('/events/', 302)

    flash('Invalid username or password', 'danger')
    return redirect('/login/', 302)


@main.get('/logout/')
def logout():
    """
    Logout endpoint
    :return:
    """
    session.clear()
    # session.pop('username', None)
    return redirect('/login/', 302)

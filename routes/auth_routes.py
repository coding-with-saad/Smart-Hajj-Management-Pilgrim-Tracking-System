from flask import Blueprint, request, session, redirect, url_for, flash, render_template
from functools import wraps
from database.db import db
from utils.responses import success_response, error_response

auth_bp = Blueprint('auth', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            if request.path.startswith('/api/'):
                return error_response("Unauthorized access", 401)
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        username = data.get('username')
        password = data.get('password')

        user = db.admins.find_one({"username": username, "password": password})
        if user:
            session['user'] = username
            if request.is_json:
                return success_response(message="Login successful")
            return redirect(url_for('dashboard_ui'))
        
        if request.is_json:
            return error_response("Invalid credentials", 401)
        flash("Invalid username or password")
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('auth.login'))

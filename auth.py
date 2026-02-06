"""Login system for Coaching Portal."""

from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from functools import wraps
import os

login_bp = Blueprint('login', __name__)

# Simple username/password - change these!
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'coaching123')

def login_required(f):
    """Decorator to require login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_logged_in' not in session:
            return redirect(url_for('login.login_page'))
        return f(*args, **kwargs)
    return decorated_function

@login_bp.route('/login', methods=['GET', 'POST'])
def login_page():
    """Login page."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check credentials
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['user_logged_in'] = True
            session['username'] = username
            return redirect(url_for('new_client_form'))
        else:
            error = "Invalid username or password"
            return render_template('login.html', error=error)
    
    return render_template('login.html')

@login_bp.route('/logout')
def logout():
    """Logout."""
    session.clear()
    return redirect(url_for('login.login_page'))

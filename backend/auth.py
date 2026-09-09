"""
SkillDNA-AI Authentication Module
Handles user registration, login, logout, and session management.
"""

import re
from functools import wraps
from flask import Blueprint, request, session, redirect, url_for, flash, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from models import User, UserProfile

auth_bp = Blueprint('auth', __name__)


def login_required(f):
    """Decorator to require authentication for protected routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def get_current_user():
    """Get the currently logged-in user object."""
    if 'user_id' in session:
        return db.session.get(User, session['user_id'])
    return None


def validate_email(email):
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password):
    """
    Validate password strength.
    Returns (is_valid, message).
    """
    if len(password) < 8:
        return False, 'Password must be at least 8 characters long.'
    if not re.search(r'[A-Z]', password):
        return False, 'Password must contain at least one uppercase letter.'
    if not re.search(r'[a-z]', password):
        return False, 'Password must contain at least one lowercase letter.'
    if not re.search(r'[0-9]', password):
        return False, 'Password must contain at least one digit.'
    return True, 'Password is strong.'


# ============================================
# Registration Route
# ============================================
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    # If user is already logged in, redirect to dashboard
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))

    if request.method == 'GET':
        return render_template('register.html')

    # POST — Process registration
    full_name = request.form.get('full_name', '').strip()
    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')
    confirm_password = request.form.get('confirm_password', '')

    # Validation
    errors = []

    if not full_name:
        errors.append('Full name is required.')
    elif len(full_name) < 2:
        errors.append('Full name must be at least 2 characters.')
    elif len(full_name) > 150:
        errors.append('Full name must be less than 150 characters.')

    if not email:
        errors.append('Email is required.')
    elif not validate_email(email):
        errors.append('Please enter a valid email address.')

    if not password:
        errors.append('Password is required.')
    else:
        is_valid, msg = validate_password(password)
        if not is_valid:
            errors.append(msg)

    if password != confirm_password:
        errors.append('Passwords do not match.')

    if errors:
        for error in errors:
            flash(error, 'error')
        return render_template('register.html', full_name=full_name, email=email)

    # Check if email already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash('An account with this email already exists.', 'error')
        return render_template('register.html', full_name=full_name, email=email)

    # Create new user
    try:
        new_user = User(
            full_name=full_name,
            email=email,
            password_hash=generate_password_hash(password, method='pbkdf2:sha256')
        )
        db.session.add(new_user)
        db.session.flush()  # Get the user ID

        # Create empty profile for the user
        profile = UserProfile(user_id=new_user.id, skills=[])
        db.session.add(profile)

        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    except Exception as e:
        db.session.rollback()
        print(f'Registration error: {e}')
        flash('An error occurred during registration. Please try again.', 'error')
        return render_template('register.html', full_name=full_name, email=email)


# ============================================
# Login Route
# ============================================
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    # If user is already logged in, redirect to dashboard
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))

    if request.method == 'GET':
        return render_template('login.html')

    # POST — Process login
    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')

    # Validation
    if not email or not password:
        flash('Please enter both email and password.', 'error')
        return render_template('login.html', email=email)

    # Find user by email
    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        flash('Invalid email or password.', 'error')
        return render_template('login.html', email=email)

    # Create session
    session['user_id'] = user.id
    session['user_name'] = user.full_name
    session['user_email'] = user.email
    session.permanent = True

    flash(f'Welcome back, {user.full_name}!', 'success')
    return redirect(url_for('main.dashboard'))


# ============================================
# Logout Route
# ============================================
@auth_bp.route('/logout')
def logout():
    """Handle user logout."""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

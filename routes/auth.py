"""
Authentication routes for registration, login, and logout.
"""
from urllib.parse import urlparse, urljoin
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, User
from utils.security import (
    validate_csrf,
    validate_email_format,
    validate_password_strength
)

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


def is_safe_url(target: str) -> bool:
    """Ensure redirect target is a safe internal relative path."""
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new citizen account."""
    if 'user_id' in session:
        return redirect(url_for('citizen.dashboard' if session.get('user_role') != 'admin' else 'admin.dashboard'))

    if request.method == 'POST':
        csrf_token = request.form.get('csrf_token')
        if not validate_csrf(csrf_token):
            flash('Security token invalid or expired. Please submit again.', 'danger')
            return render_template('auth/register.html')

        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Input Validations
        errors = []
        if not name or len(name) < 2:
            errors.append("Please provide a valid full name (at least 2 characters).")
        if not validate_email_format(email):
            errors.append("Please provide a valid email address.")
        
        is_strong, msg = validate_password_strength(password)
        if not is_strong:
            errors.append(msg)
        if password != confirm_password:
            errors.append("Passwords do not match.")

        # Check existing user
        if not errors:
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                errors.append("An account with this email already exists. Please log in.")

        if errors:
            for err in errors:
                flash(err, 'danger')
            return render_template('auth/register.html', name=name, email=email)

        # Create new citizen user
        user = User(
            name=name,
            email=email,
            role='citizen'
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        # Log in newly registered user
        session['user_id'] = user.id
        session['user_name'] = user.name
        session['user_email'] = user.email
        session['user_role'] = user.role

        flash(f"Welcome to EcoTrack, {user.name}! Your account has been created successfully.", "success")
        return redirect(url_for('citizen.dashboard'))

    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Log in an existing user (Citizen or Administrator)."""
    if 'user_id' in session:
        return redirect(url_for('citizen.dashboard' if session.get('user_role') != 'admin' else 'admin.dashboard'))

    next_page = request.args.get('next', '')

    if request.method == 'POST':
        csrf_token = request.form.get('csrf_token')
        if not validate_csrf(csrf_token):
            flash('Security token invalid or expired. Please submit again.', 'danger')
            return render_template('auth/login.html')

        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        submitted_next = request.form.get('next', '')

        if not email or not password:
            flash("Please enter both email and password.", "danger")
            return render_template('auth/login.html', email=email, next=submitted_next)

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            flash("Invalid email or password. Please verify your credentials.", "danger")
            return render_template('auth/login.html', email=email, next=submitted_next)

        # Establish authenticated session
        session.clear()
        session['user_id'] = user.id
        session['user_name'] = user.name
        session['user_email'] = user.email
        session['user_role'] = user.role

        flash(f"Welcome back, {user.name}!", "success")

        target = submitted_next if submitted_next and is_safe_url(submitted_next) else None
        if target:
            return redirect(target)

        if user.is_admin:
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('citizen.dashboard'))

    return render_template('auth/login.html', next=next_page)


@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    """Clear session and log out the user."""
    user_name = session.get('user_name', 'User')
    session.clear()
    flash(f"You have been successfully logged out. Thank you for contributing, {user_name}!", "info")
    return redirect(url_for('main.index'))


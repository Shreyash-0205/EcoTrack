"""
Security and authentication helper utilities for EcoTrack.
Includes route protection decorators, CSRF validation, and safe file uploads.
"""
import os
import re
import secrets
import uuid
from functools import wraps
from pathlib import Path
from flask import session, redirect, url_for, flash, request, abort, current_app
from PIL import Image
from werkzeug.utils import secure_filename


def generate_csrf_token() -> str:
    """Generate or retrieve the session CSRF token."""
    if '_csrf_token' not in session:
        session['_csrf_token'] = secrets.token_hex(32)
    return session['_csrf_token']


def validate_csrf(token: str) -> bool:
    """Validate submitted CSRF token against session token."""
    session_token = session.get('_csrf_token')
    if not session_token or not token:
        return False
    return secrets.compare_digest(session_token, token)


def login_required(f):
    """Decorator to enforce user authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator to enforce administrator authorization."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in with administrator credentials.', 'warning')
            return redirect(url_for('auth.login', next=request.path))
        if session.get('user_role') != 'admin':
            flash('Access denied: Administrator privileges required.', 'danger')
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function


def validate_email_format(email: str) -> bool:
    """Validate email address format."""
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email.strip())) if email else False


def validate_password_strength(password: str) -> tuple[bool, str]:
    """Validate that password meets security requirements."""
    if not password or len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r'[A-Za-z]', password):
        return False, "Password must contain at least one letter."
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number."
    return True, ""


def allowed_file(filename: str, allowed_extensions: set) -> bool:
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def save_uploaded_image(file_storage, upload_folder: str, allowed_extensions: set) -> tuple[bool, str]:
    """
    Safely validate and save an uploaded image file.
    Validates extension and image binary integrity using Pillow.
    Returns (success, filename_or_error_message).
    """
    if not file_storage or file_storage.filename == '':
        return False, "No file provided"

    filename = secure_filename(file_storage.filename)
    if not filename or not allowed_file(filename, allowed_extensions):
        return False, "Invalid file type. Only JPG, JPEG, PNG, and WEBP images are permitted."

    # Validate image binary data using Pillow to prevent script execution
    try:
        file_storage.seek(0)
        image = Image.open(file_storage)
        image.verify()  # Verifies file integrity and format
        # Reset file pointer after verify
        file_storage.seek(0)
    except Exception:
        return False, "Uploaded file is corrupted or not a valid image."

    # Generate unique, collision-proof filename
    extension = filename.rsplit('.', 1)[1].lower()
    unique_name = f"{uuid.uuid4().hex}_{secrets.token_hex(4)}.{extension}"
    target_path = Path(upload_folder) / unique_name

    # Ensure upload directory exists
    os.makedirs(upload_folder, exist_ok=True)

    try:
        # Re-open and save safely (this also strips any potential embedded payloads)
        image = Image.open(file_storage)
        # Convert RGBA to RGB for JPEG compatibility if needed
        if extension in ['jpg', 'jpeg'] and image.mode in ('RGBA', 'P'):
            image = image.convert('RGB')
        image.save(target_path)
        return True, unique_name
    except Exception as e:
        return False, f"Failed to save image securely: {str(e)}"


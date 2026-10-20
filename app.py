"""
EcoTrack — Smart Waste Management and Segregation System.
Main Flask application entry point and application factory.
"""
import os
from pathlib import Path
from datetime import datetime, timezone
from flask import Flask, render_template, session, g

from config import config_by_name, Config
from models import db, User, Report, ActivityLog
from utils.security import generate_csrf_token
from routes.auth import auth_bp
from routes.main import main_bp
from routes.citizen import citizen_bp
from routes.admin import admin_bp
from routes.api import api_bp


def create_app(config_name='development') -> Flask:
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    config_class = config_by_name.get(config_name, config_by_name['default'])
    app.config.from_object(config_class)

    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialize extensions
    db.init_app(app)

    # Register template context processors
    @app.context_processor
    def inject_global_template_vars():
        """Inject security tokens, user status, and global variables to all templates."""
        user = None
        if 'user_id' in session:
            user = db.session.get(User, session['user_id'])

        return {
            'csrf_token': generate_csrf_token,
            'current_user': user,
            'user_role': session.get('user_role'),
            'current_year': datetime.now(timezone.utc).year
        }

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(citizen_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)

    # Register custom error handlers without exposing stack traces
    @app.errorhandler(400)
    def bad_request(error):
        return render_template('errors/400.html'), 400

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    # Auto-create tables if running in development mode and db doesn't exist
    with app.app_context():
        db.create_all()

    return app


app = create_app(os.environ.get('FLASK_ENV', 'production'))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

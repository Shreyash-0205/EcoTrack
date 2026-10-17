"""
Configuration module for EcoTrack application.
Supports Development, Testing, and Production environments.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Config:
    """Base configuration with safe defaults."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'ecotrack-dev-secret-key-mumbai-2026')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload configurations
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', str(BASE_DIR / 'uploads' / 'reports'))
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB maximum upload
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
    
    # Session security
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours in seconds


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', f"sqlite:///{BASE_DIR / 'ecotrack.db'}"
    )


class TestingConfig(Config):
    """Testing configuration with separate in-memory or test database."""
    TESTING = True
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR / 'test_ecotrack.db'}"
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'test-secret-key-ecotrack'


class ProductionConfig(Config):
    """Production configuration with strict security."""
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


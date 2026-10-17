"""
Pytest configuration and fixtures for EcoTrack test suite.
Uses an isolated in-memory or separate SQLite test database.
"""
import io
import os
import sys
from pathlib import Path

# Add project root directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from PIL import Image
from app import create_app
from models import db, User, Report, ActivityLog


@pytest.fixture
def app():
    """Create and configure a fresh application instance for testing."""
    app = create_app('testing')
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """A test client for the application."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test CLI runner for the application."""
    return app.test_cli_runner()


@pytest.fixture
def sample_users(app):
    """Seed test database with an admin and citizen user."""
    admin = User(name="Test Admin", email="admin@test.org", role="admin")
    admin.set_password("AdminSecure123")
    db.session.add(admin)

    citizen = User(name="Test Citizen", email="citizen@test.org", role="citizen")
    citizen.set_password("CitizenSecure123")
    db.session.add(citizen)

    citizen2 = User(name="Other Citizen", email="other@test.org", role="citizen")
    citizen2.set_password("CitizenSecure123")
    db.session.add(citizen2)

    db.session.commit()
    return {'admin': admin, 'citizen': citizen, 'citizen2': citizen2}


@pytest.fixture
def auth_citizen_client(client, sample_users):
    """Test client authenticated as a Citizen."""
    with client.session_transaction() as sess:
        sess['user_id'] = sample_users['citizen'].id
        sess['user_name'] = sample_users['citizen'].name
        sess['user_email'] = sample_users['citizen'].email
        sess['user_role'] = sample_users['citizen'].role
        sess['_csrf_token'] = 'test-valid-csrf-token'
    return client


@pytest.fixture
def auth_admin_client(client, sample_users):
    """Test client authenticated as an Administrator."""
    with client.session_transaction() as sess:
        sess['user_id'] = sample_users['admin'].id
        sess['user_name'] = sample_users['admin'].name
        sess['user_email'] = sample_users['admin'].email
        sess['user_role'] = sample_users['admin'].role
        sess['_csrf_token'] = 'test-valid-csrf-token'
    return client


@pytest.fixture
def dummy_image():
    """Create a minimal in-memory valid PNG image for upload testing."""
    file_bytes = io.BytesIO()
    image = Image.new('RGB', (100, 100), color='green')
    image.save(file_bytes, format='PNG')
    file_bytes.seek(0)
    return file_bytes

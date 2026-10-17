"""
Automated unit and integration tests for authentication and authorization.
"""
from models import User


def test_registration_success(client, app):
    """Test successful citizen user registration."""
    with client.session_transaction() as sess:
        sess['_csrf_token'] = 'test-token'

    response = client.post('/auth/register', data={
        'csrf_token': 'test-token',
        'name': 'Rahul Verma',
        'email': 'rahul@example.com',
        'password': 'Password123',
        'confirm_password': 'Password123'
    }, follow_redirects=True)

    assert response.status_code == 200
    with app.app_context():
        user = User.query.filter_by(email='rahul@example.com').first()
        assert user is not None
        assert user.name == 'Rahul Verma'
        assert user.role == 'citizen'
        assert user.check_password('Password123')


def test_registration_duplicate_email(client, sample_users):
    """Test that duplicate registration with an existing email is rejected."""
    with client.session_transaction() as sess:
        sess['_csrf_token'] = 'test-token'

    response = client.post('/auth/register', data={
        'csrf_token': 'test-token',
        'name': 'Duplicate User',
        'email': 'citizen@test.org',
        'password': 'Password123',
        'confirm_password': 'Password123'
    }, follow_redirects=True)

    assert b"An account with this email already exists" in response.data


def test_registration_weak_password(client):
    """Test that passwords shorter than 8 characters are rejected."""
    with client.session_transaction() as sess:
        sess['_csrf_token'] = 'test-token'

    response = client.post('/auth/register', data={
        'csrf_token': 'test-token',
        'name': 'Short Pass',
        'email': 'short@example.com',
        'password': 'pass',
        'confirm_password': 'pass'
    }, follow_redirects=True)

    assert b"Password must be at least 8 characters long" in response.data


def test_registration_mismatched_password(client):
    """Test that mismatched passwords are rejected."""
    with client.session_transaction() as sess:
        sess['_csrf_token'] = 'test-token'

    response = client.post('/auth/register', data={
        'csrf_token': 'test-token',
        'name': 'Mismatch User',
        'email': 'mismatch@example.com',
        'password': 'Password123',
        'confirm_password': 'DifferentPassword123'
    }, follow_redirects=True)

    assert b"Passwords do not match" in response.data


def test_login_success_citizen(client, sample_users):
    """Test successful login for citizen account with correct redirect."""
    with client.session_transaction() as sess:
        sess['_csrf_token'] = 'test-token'

    response = client.post('/auth/login', data={
        'csrf_token': 'test-token',
        'email': 'citizen@test.org',
        'password': 'CitizenSecure123'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Citizen Dashboard" in response.data
    with client.session_transaction() as sess:
        assert sess['user_role'] == 'citizen'
        assert sess['user_email'] == 'citizen@test.org'


def test_login_success_admin(client, sample_users):
    """Test successful login for admin account with redirect to admin dashboard."""
    with client.session_transaction() as sess:
        sess['_csrf_token'] = 'test-token'

    response = client.post('/auth/login', data={
        'csrf_token': 'test-token',
        'email': 'admin@test.org',
        'password': 'AdminSecure123'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Civic Waste Operations Dashboard" in response.data
    with client.session_transaction() as sess:
        assert sess['user_role'] == 'admin'


def test_login_invalid_password(client, sample_users):
    """Test login failure with incorrect password."""
    with client.session_transaction() as sess:
        sess['_csrf_token'] = 'test-token'

    response = client.post('/auth/login', data={
        'csrf_token': 'test-token',
        'email': 'citizen@test.org',
        'password': 'WrongPassword999'
    }, follow_redirects=True)

    assert b"Invalid email or password" in response.data


def test_login_nonexistent_user(client):
    """Test login failure with unregistered email."""
    with client.session_transaction() as sess:
        sess['_csrf_token'] = 'test-token'

    response = client.post('/auth/login', data={
        'csrf_token': 'test-token',
        'email': 'doesnotexist@test.org',
        'password': 'SomePassword123'
    }, follow_redirects=True)

    assert b"Invalid email or password" in response.data


def test_logout(client, sample_users):
    """Test user logout clearing session."""
    with client.session_transaction() as sess:
        sess['user_id'] = sample_users['citizen'].id
        sess['user_name'] = 'Test Citizen'
        sess['user_role'] = 'citizen'

    response = client.get('/auth/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b"You have been successfully logged out" in response.data
    with client.session_transaction() as sess:
        assert 'user_id' not in sess


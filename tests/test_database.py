"""
Automated unit tests for database models, relationships, and constraints.
"""
from models import db, User, Report, ActivityLog


def test_user_password_hashing(app):
    """Test user password hashing and verification."""
    with app.app_context():
        user = User(name="Security Test", email="sec@test.org")
        user.set_password("SecretPass123")
        db.session.add(user)
        db.session.commit()

        assert user.password_hash != "SecretPass123"
        assert user.check_password("SecretPass123") is True
        assert user.check_password("WrongPass123") is False


def test_user_admin_property():
    """Test is_admin boolean property based on role string."""
    admin_user = User(name="Admin", email="a@test.org", role="admin")
    citizen_user = User(name="Citizen", email="c@test.org", role="citizen")

    assert admin_user.is_admin is True
    assert citizen_user.is_admin is False


def test_report_coordinates_property():
    """Test has_coordinates helper logic."""
    r_valid = Report(latitude=19.0760, longitude=72.8777)
    r_none = Report(latitude=None, longitude=None)
    r_partial = Report(latitude=19.0760, longitude=None)
    r_invalid = Report(latitude=105.0, longitude=72.8777)

    assert r_valid.has_coordinates is True
    assert r_none.has_coordinates is False
    assert r_partial.has_coordinates is False
    assert r_invalid.has_coordinates is False


def test_report_cascade_logs(app, sample_users):
    """Test that deleting a report cascades to its associated activity logs."""
    with app.app_context():
        rep = Report(
            user_id=sample_users['citizen'].id,
            title="Cascade Test Hotspot",
            category="Dry",
            location="Test Lane",
            description="Testing log deletion cascade."
        )
        db.session.add(rep)
        db.session.commit()

        log = ActivityLog(
            admin_user_id=sample_users['admin'].id,
            report_id=rep.id,
            action="Created log for cascade test"
        )
        db.session.add(log)
        db.session.commit()

        log_id = log.id
        db.session.delete(rep)
        db.session.commit()

        assert db.session.get(ActivityLog, log_id) is None

"""
Automated unit and integration tests for administrator authorization, status triage, and audit trail.
"""
from models import db, Report, ActivityLog


def test_admin_dashboard_access(auth_admin_client):
    """Administrator can successfully view the admin dashboard."""
    response = auth_admin_client.get('/admin/dashboard')
    assert response.status_code == 200
    assert b"Civic Waste Operations Dashboard" in response.data


def test_citizen_cannot_access_admin_dashboard(auth_citizen_client):
    """Citizen user receives 403 Forbidden when attempting to view administrator dashboard."""
    response = auth_citizen_client.get('/admin/dashboard')
    assert response.status_code == 403
    assert b"Access Denied" in response.data or b"403" in response.data


def test_guest_cannot_access_admin_dashboard(client):
    """Anonymous user is redirected to login when trying to view admin dashboard."""
    response = client.get('/admin/dashboard', follow_redirects=False)
    assert response.status_code == 302
    assert '/auth/login' in response.location


def test_admin_update_report_status_and_logs(auth_admin_client, app, sample_users):
    """Admin updating report status changes the status and records an ActivityLog."""
    with app.app_context():
        report = Report(
            user_id=sample_users['citizen'].id,
            title="Complaint Awaiting Triage",
            category="Wet",
            location="Market Lane, Dadar",
            description="Organic waste overflowing into street.",
            status="Reported"
        )
        db.session.add(report)
        db.session.commit()
        report_id = report.id

    response = auth_admin_client.post(f'/admin/reports/{report_id}/status', data={
        'csrf_token': 'test-valid-csrf-token',
        'status': 'In Progress',
        'admin_notes': 'Ward G/North sanitation truck dispatched with lime powder.'
    }, follow_redirects=True)

    assert response.status_code == 200
    with app.app_context():
        updated_report = db.session.get(Report, report_id)
        assert updated_report.status == 'In Progress'
        assert 'Ward G/North' in updated_report.admin_notes

        # Verify audit log entry was created
        log = ActivityLog.query.filter_by(report_id=report_id).first()
        assert log is not None
        assert "Status updated from 'Reported' to 'In Progress'" in log.action
        assert log.admin_user_id == sample_users['admin'].id


def test_admin_delete_report(auth_admin_client, app, sample_users):
    """Admin deleting an inappropriate or duplicate report removes it and creates an audit entry."""
    with app.app_context():
        report = Report(
            user_id=sample_users['citizen'].id,
            title="Duplicate Spam Hotspot",
            category="Other",
            location="Unknown Corner",
            description="Spam text repeated multiple times."
        )
        db.session.add(report)
        db.session.commit()
        report_id = report.id

    response = auth_admin_client.post(f'/admin/reports/{report_id}/delete', data={
        'csrf_token': 'test-valid-csrf-token'
    }, follow_redirects=True)

    assert response.status_code == 200
    with app.app_context():
        deleted = db.session.get(Report, report_id)
        assert deleted is None

        # Verify deletion audit log
        log = ActivityLog.query.filter(ActivityLog.action.ilike("%Deleted report%")).first()
        assert log is not None
        assert f"Deleted report #{report_id}" in log.action


def test_admin_view_audit_logs(auth_admin_client):
    """Admin can view the audit trail page."""
    response = auth_admin_client.get('/admin/logs')
    assert response.status_code == 200
    assert b"Administrative Activity Logs" in response.data

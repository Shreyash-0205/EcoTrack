"""
ActivityLog model for administrative audit trail.
"""
from datetime import datetime, timezone
from . import db


class ActivityLog(db.Model):
    """Audit log model for recording administrative actions."""
    __tablename__ = 'activity_logs'

    id = db.Column(db.Integer, primary_key=True)
    admin_user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True, index=True)
    report_id = db.Column(db.Integer, db.ForeignKey('reports.id', ondelete='CASCADE'), nullable=True, index=True)
    action = db.Column(db.String(255), nullable=False)
    details = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)

    def to_dict(self) -> dict:
        """Serialize activity log entry."""
        return {
            'id': self.id,
            'admin_user_id': self.admin_user_id,
            'admin_name': self.admin_user.name if self.admin_user else 'System Admin',
            'report_id': self.report_id,
            'report_title': self.report.title if self.report else 'N/A',
            'action': self.action,
            'details': self.details,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }

    def __repr__(self) -> str:
        return f"<ActivityLog id={self.id} action='{self.action}' admin_id={self.admin_user_id}>"


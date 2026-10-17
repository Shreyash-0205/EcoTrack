"""
Report model representing waste hotspot submissions.
"""
from datetime import datetime, timezone
from . import db


class Report(db.Model):
    """Waste report database model."""
    __tablename__ = 'reports'

    CATEGORIES = ['Wet', 'Dry', 'Plastic', 'E-waste', 'Mixed', 'Other']
    STATUSES = ['Reported', 'In Progress', 'Resolved', 'Rejected']

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False, index=True)
    location = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    image_filename = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(30), nullable=False, default='Reported', index=True)
    admin_notes = db.Column(db.Text, nullable=True)
    is_demo = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationship to activity logs
    activity_logs = db.relationship('ActivityLog', backref='report', lazy='dynamic', cascade='all, delete-orphan')

    @property
    def has_coordinates(self) -> bool:
        """Check if report has valid geo coordinates."""
        return (
            self.latitude is not None and 
            self.longitude is not None and 
            -90.0 <= self.latitude <= 90.0 and 
            -180.0 <= self.longitude <= 180.0
        )

    @property
    def status_badge_class(self) -> str:
        """Return Bootstrap badge class based on status."""
        mapping = {
            'Reported': 'bg-warning text-dark',
            'In Progress': 'bg-primary text-white',
            'Resolved': 'bg-success text-white',
            'Rejected': 'bg-secondary text-white'
        }
        return mapping.get(self.status, 'bg-secondary text-white')

    @property
    def category_badge_class(self) -> str:
        """Return Bootstrap badge class based on category."""
        mapping = {
            'Wet': 'badge-category-wet',
            'Dry': 'badge-category-dry',
            'Plastic': 'badge-category-plastic',
            'E-waste': 'badge-category-ewaste',
            'Mixed': 'badge-category-mixed',
            'Other': 'badge-category-other'
        }
        return mapping.get(self.category, 'badge-category-other')

    def to_dict(self) -> dict:
        """Serialize report to dictionary for API and map visualization."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'reporter_name': self.reporter.name if self.reporter else 'Anonymous',
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'location': self.location,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'has_coordinates': self.has_coordinates,
            'image_filename': self.image_filename,
            'status': self.status,
            'admin_notes': self.admin_notes,
            'is_demo': self.is_demo,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M') if self.updated_at else None
        }

    def __repr__(self) -> str:
        return f"<Report id={self.id} title='{self.title}' status='{self.status}'>"

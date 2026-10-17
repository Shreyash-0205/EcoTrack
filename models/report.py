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

    @property
    def category_slug(self) -> str:
        """Return standardized slug for category assets."""
        mapping = {
            'Wet': 'wet',
            'Dry': 'dry',
            'Plastic': 'plastic',
            'E-waste': 'ewaste',
            'Mixed': 'mixed',
            'Other': 'other'
        }
        return mapping.get(self.category, 'mixed')

    @property
    def fallback_image_url(self) -> str:
        """Return category-specific SVG fallback illustration URL."""
        return f"/static/images/fallbacks/{self.category_slug}.svg"

    @property
    def has_valid_image(self) -> bool:
        """Check if report has an associated uploaded image that exists on disk."""
        if not self.image_filename:
            return False
        import os
        from flask import current_app
        try:
            upload_dir = current_app.config.get('UPLOAD_FOLDER')
            if upload_dir:
                return os.path.isfile(os.path.join(upload_dir, self.image_filename))
        except RuntimeError:
            pass
        return True

    @property
    def sample_photo_filename(self) -> str:
        """Return the appropriate realistic sample photograph filename."""
        content_lower = f"{self.title or ''} {self.description or ''} {self.location or ''}".lower()
        if "monitor" in content_lower or "crt" in content_lower or "screen" in content_lower:
            return "discarded_monitors.jpg"
        if "battery" in content_lower or "batteries" in content_lower:
            return "discarded_batteries.jpg"
        if ("dustbin" in content_lower or "dust bin" in content_lower or "community dustbin" in content_lower) and self.category == "Mixed":
            return "mixed_dustbin_waste.jpg"
        
        category_map = {
            'Wet': 'wet_organic_waste.jpg',
            'Dry': 'cardboard_recycling.jpg',
            'Plastic': 'plastic_beach_litter.jpg',
            'E-waste': 'discarded_batteries.jpg',
            'Mixed': 'mixed_garbage_public.jpg',
            'Other': 'construction_debris.jpg'
        }
        return category_map.get(self.category, 'mixed_garbage_public.jpg')

    @property
    def sample_image_url(self) -> str:
        """Return local static URL for realistic waste photograph."""
        return f"/static/images/photos/{self.sample_photo_filename}"

    @property
    def display_image_url(self) -> str:
        """Return the uploaded image URL if it exists on disk, else the realistic sample photograph."""
        if self.has_valid_image:
            return f"/uploads/reports/{self.image_filename}"
        return self.sample_image_url

    @property
    def display_title(self) -> str:
        """Return clean title for website presentation without any '[DEMO]' prefix."""
        if not self.title:
            return ""
        clean = self.title.strip()
        if clean.upper().startswith("[DEMO]"):
            clean = clean[6:].strip()
        return clean

    def to_dict(self) -> dict:
        """Serialize report to dictionary for API and map visualization."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'reporter_name': self.reporter.name if self.reporter else 'Anonymous',
            'title': self.display_title,
            'original_title': self.title,
            'description': self.description,
            'category': self.category,
            'category_slug': self.category_slug,
            'category_badge_class': self.category_badge_class,
            'status_badge_class': self.status_badge_class,
            'location': self.location,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'has_coordinates': self.has_coordinates,
            'image_filename': self.image_filename,
            'image_url': self.display_image_url,
            'sample_image_url': self.sample_image_url,
            'fallback_image_url': self.fallback_image_url,
            'has_uploaded_image': self.has_valid_image,
            'is_sample_image': not self.has_valid_image,
            'status': self.status,
            'admin_notes': self.admin_notes,
            'is_demo': self.is_demo,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M') if self.updated_at else None
        }

    def __repr__(self) -> str:
        return f"<Report id={self.id} title='{self.title}' status='{self.status}'>"


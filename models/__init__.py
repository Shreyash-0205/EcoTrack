"""
Database initialization for EcoTrack models.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .report import Report
from .activity_log import ActivityLog

__all__ = ['db', 'User', 'Report', 'ActivityLog']

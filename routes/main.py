"""
Main public routes for EcoTrack: Landing page, Segregation Guide, Map View, and About.
"""
from flask import Blueprint, render_template
from models import Report, User

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Public landing page displaying project overview and real-time statistics."""
    total_reports = Report.query.count()
    resolved_reports = Report.query.filter_by(status='Resolved').count()
    pending_reports = Report.query.filter_by(status='Reported').count()
    in_progress = Report.query.filter_by(status='In Progress').count()
    total_citizens = User.query.filter_by(role='citizen').count()

    recent_reports = (
        Report.query
        .order_by(Report.created_at.desc())
        .limit(6)
        .all()
    )

    stats = {
        'total': total_reports,
        'resolved': resolved_reports,
        'pending': pending_reports,
        'in_progress': in_progress,
        'citizens': total_citizens,
        'resolution_rate': round((resolved_reports / total_reports * 100), 1) if total_reports > 0 else 0
    }

    return render_template('pages/index.html', stats=stats, recent_reports=recent_reports)


@main_bp.route('/guide')
def segregation_guide():
    """Educational page explaining waste categorization and municipal segregation."""
    return render_template('pages/segregation_guide.html')


@main_bp.route('/map')
def map_view():
    """Interactive Leaflet map showing reported waste hotspots with filters."""
    categories = Report.CATEGORIES
    statuses = Report.STATUSES
    
    # Reports with coordinates
    geo_reports = (
        Report.query
        .filter(Report.latitude.isnot(None), Report.longitude.isnot(None))
        .order_by(Report.created_at.desc())
        .all()
    )
    
    # Count of reports without coordinates for transparency
    missing_coords_count = Report.query.filter(
        (Report.latitude.is_(None)) | (Report.longitude.is_(None))
    ).count()

    return render_template(
        'pages/map_view.html',
        categories=categories,
        statuses=statuses,
        reports_count=len(geo_reports),
        missing_coords_count=missing_coords_count
    )


@main_bp.route('/about')
def about():
    """About page outlining the project background, university context, and architecture."""
    return render_template('pages/about.html')


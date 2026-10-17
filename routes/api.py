"""
API and media endpoints for Leaflet map integration, Chart.js datasets, and safe image delivery.
"""
from pathlib import Path
from flask import Blueprint, jsonify, request, current_app, send_from_directory, abort
from models import Report, User

api_bp = Blueprint('api', __name__)


@api_bp.route('/api/reports')
def get_map_reports():
    """
    Return JSON list of reports that have valid geographic coordinates.
    Supports filtering by category and status.
    """
    category = request.args.get('category', '').strip()
    status = request.args.get('status', '').strip()
    search = request.args.get('q', '').strip()

    query = Report.query.filter(
        Report.latitude.isnot(None),
        Report.longitude.isnot(None),
        Report.latitude >= -90.0,
        Report.latitude <= 90.0,
        Report.longitude >= -180.0,
        Report.longitude <= 180.0
    )

    if category and category in Report.CATEGORIES:
        query = query.filter(Report.category == category)

    if status and status in Report.STATUSES:
        query = query.filter(Report.status == status)

    if search:
        query = query.filter(
            (Report.title.ilike(f"%{search}%")) |
            (Report.location.ilike(f"%{search}%"))
        )

    reports = query.order_by(Report.created_at.desc()).all()

    data = []
    for r in reports:
        item = r.to_dict()
        item['status_badge_class'] = r.status_badge_class
        item['category_badge_class'] = r.category_badge_class
        data.append(item)

    return jsonify({
        'success': True,
        'count': len(data),
        'reports': data
    })


@api_bp.route('/api/stats/categories')
def get_category_stats():
    """Return category distribution for Chart.js visualization."""
    labels = Report.CATEGORIES
    counts = [Report.query.filter_by(category=cat).count() for cat in labels]
    return jsonify({
        'labels': labels,
        'counts': counts
    })


@api_bp.route('/api/stats/statuses')
def get_status_stats():
    """Return status distribution for Chart.js visualization."""
    labels = Report.STATUSES
    counts = [Report.query.filter_by(status=st).count() for st in labels]
    return jsonify({
        'labels': labels,
        'counts': counts
    })


@api_bp.route('/uploads/reports/<path:filename>')
def serve_uploaded_image(filename):
    """
    Safely serve uploaded report images.
    Prevents path traversal and validates file existence.
    """
    # Reject path traversal attempts
    if '..' in filename or filename.startswith('/') or filename.startswith('\\'):
        abort(404)

    upload_dir = Path(current_app.config['UPLOAD_FOLDER']).resolve()
    target_file = (upload_dir / filename).resolve()

    # Ensure target path is strictly within the upload directory
    if not str(target_file).startswith(str(upload_dir)):
        abort(403)

    if not target_file.is_file():
        abort(404)

    return send_from_directory(str(upload_dir), filename)


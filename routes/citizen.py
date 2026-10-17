"""
Citizen routes for submitting reports, viewing dashboard, and managing personal submissions.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, abort
from models import db, Report, User
from utils.security import login_required, validate_csrf, save_uploaded_image

citizen_bp = Blueprint('citizen', __name__)


@citizen_bp.route('/dashboard')
@login_required
def dashboard():
    """Citizen dashboard displaying personal statistics, charts, and recent activity."""
    user_id = session['user_id']
    
    # Personal counts
    my_reports_query = Report.query.filter_by(user_id=user_id)
    total_count = my_reports_query.count()
    pending_count = my_reports_query.filter_by(status='Reported').count()
    in_progress_count = my_reports_query.filter_by(status='In Progress').count()
    resolved_count = my_reports_query.filter_by(status='Resolved').count()

    recent_reports = (
        my_reports_query
        .order_by(Report.created_at.desc())
        .limit(5)
        .all()
    )

    # Category counts for chart
    category_counts = {}
    for cat in Report.CATEGORIES:
        category_counts[cat] = my_reports_query.filter_by(category=cat).count()

    stats = {
        'total': total_count,
        'pending': pending_count,
        'in_progress': in_progress_count,
        'resolved': resolved_count,
        'category_counts': category_counts
    }

    return render_template('citizen/dashboard.html', stats=stats, recent_reports=recent_reports)


@citizen_bp.route('/report', methods=['GET', 'POST'])
@login_required
def report_waste():
    """Submit a new waste hotspot report with optional coordinates and photo."""
    if request.method == 'POST':
        csrf_token = request.form.get('csrf_token')
        if not validate_csrf(csrf_token):
            flash('Security token invalid or expired. Please submit again.', 'danger')
            return redirect(url_for('citizen.report_waste'))

        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        category = request.form.get('category', '').strip()
        location = request.form.get('location', '').strip()
        lat_str = request.form.get('latitude', '').strip()
        lng_str = request.form.get('longitude', '').strip()
        photo_file = request.files.get('photo')

        # Form Validation
        errors = []
        if not title or len(title) < 5 or len(title) > 150:
            errors.append("Title must be between 5 and 150 characters.")
        if not description or len(description) < 10:
            errors.append("Please provide a detailed description (at least 10 characters).")
        if category not in Report.CATEGORIES:
            errors.append("Please select a valid waste category.")
        if not location or len(location) < 3:
            errors.append("Please enter a valid location or landmark.")

        # Coordinate Validation (Optional)
        latitude = None
        longitude = None
        if lat_str or lng_str:
            try:
                lat_val = float(lat_str)
                lng_val = float(lng_str)
                if not (-90.0 <= lat_val <= 90.0) or not (-180.0 <= lng_val <= 180.0):
                    errors.append("Geographic coordinates are out of valid bounds (-90 to 90, -180 to 180).")
                else:
                    latitude = round(lat_val, 6)
                    longitude = round(lng_val, 6)
            except ValueError:
                errors.append("Latitude and longitude must be valid decimal numbers.")

        # Photo Validation & Saving (Optional)
        image_filename = None
        if photo_file and photo_file.filename:
            success, result = save_uploaded_image(
                photo_file,
                current_app.config['UPLOAD_FOLDER'],
                current_app.config['ALLOWED_EXTENSIONS']
            )
            if not success:
                errors.append(result)
            else:
                image_filename = result

        if errors:
            for err in errors:
                flash(err, 'danger')
            return render_template(
                'citizen/report_waste.html',
                categories=Report.CATEGORIES,
                form_data=request.form
            )

        # Create Report
        report = Report(
            user_id=session['user_id'],
            title=title,
            description=description,
            category=category,
            location=location,
            latitude=latitude,
            longitude=longitude,
            image_filename=image_filename,
            status='Reported'
        )

        db.session.add(report)
        db.session.commit()

        flash(f"Waste hotspot reported successfully! Complaint ID: #{report.id}. Our civic team has been notified.", "success")
        return redirect(url_for('citizen.report_detail', report_id=report.id))

    return render_template('citizen/report_waste.html', categories=Report.CATEGORIES, form_data={})


@citizen_bp.route('/my-reports')
@login_required
def my_reports():
    """List citizen's own submitted waste reports with search, filtering, and sorting."""
    user_id = session['user_id']
    query = Report.query.filter_by(user_id=user_id)

    # Search filter
    search = request.args.get('q', '').strip()
    if search:
        query = query.filter(
            (Report.title.ilike(f"%{search}%")) |
            (Report.location.ilike(f"%{search}%")) |
            (Report.description.ilike(f"%{search}%"))
        )

    # Category filter
    category = request.args.get('category', '').strip()
    if category and category in Report.CATEGORIES:
        query = query.filter_by(category=category)

    # Status filter
    status = request.args.get('status', '').strip()
    if status and status in Report.STATUSES:
        query = query.filter_by(status=status)

    # Sorting
    sort = request.args.get('sort', 'newest')
    if sort == 'oldest':
        query = query.order_by(Report.created_at.asc())
    else:
        query = query.order_by(Report.created_at.desc())

    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = 8
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        'citizen/my_reports.html',
        reports=pagination.items,
        pagination=pagination,
        categories=Report.CATEGORIES,
        statuses=Report.STATUSES,
        current_search=search,
        current_category=category,
        current_status=status,
        current_sort=sort
    )


@citizen_bp.route('/reports/<int:report_id>')
def report_detail(report_id):
    """View details of a specific waste hotspot report."""
    report = db.get_or_404(Report, report_id)
    
    # Check if current user is owner or admin
    is_owner = 'user_id' in session and session['user_id'] == report.user_id
    is_admin = session.get('user_role') == 'admin'

    return render_template(
        'citizen/report_detail.html',
        report=report,
        is_owner=is_owner,
        is_admin=is_admin
    )


@citizen_bp.route('/reports/<int:report_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_report(report_id):
    """Allow citizen to edit their report only while status is still 'Reported'."""
    report = db.get_or_404(Report, report_id)

    if report.user_id != session['user_id']:
        flash("You are not authorized to edit this report.", "danger")
        return abort(403)

    if report.status != 'Reported':
        flash("Reports that are In Progress or Resolved can no longer be edited.", "warning")
        return redirect(url_for('citizen.report_detail', report_id=report.id))

    if request.method == 'POST':
        csrf_token = request.form.get('csrf_token')
        if not validate_csrf(csrf_token):
            flash('Security token invalid or expired.', 'danger')
            return redirect(url_for('citizen.edit_report', report_id=report.id))

        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        category = request.form.get('category', '').strip()
        location = request.form.get('location', '').strip()
        lat_str = request.form.get('latitude', '').strip()
        lng_str = request.form.get('longitude', '').strip()
        photo_file = request.files.get('photo')

        errors = []
        if not title or len(title) < 5:
            errors.append("Title must be at least 5 characters.")
        if not description or len(description) < 10:
            errors.append("Description must be at least 10 characters.")
        if category not in Report.CATEGORIES:
            errors.append("Invalid category.")
        if not location:
            errors.append("Location is required.")

        latitude = report.latitude
        longitude = report.longitude
        if lat_str or lng_str:
            try:
                lat_val = float(lat_str)
                lng_val = float(lng_str)
                if -90.0 <= lat_val <= 90.0 and -180.0 <= lng_val <= 180.0:
                    latitude = round(lat_val, 6)
                    longitude = round(lng_val, 6)
                else:
                    errors.append("Coordinates out of range.")
            except ValueError:
                errors.append("Coordinates must be valid numbers.")

        if photo_file and photo_file.filename:
            success, result = save_uploaded_image(
                photo_file,
                current_app.config['UPLOAD_FOLDER'],
                current_app.config['ALLOWED_EXTENSIONS']
            )
            if not success:
                errors.append(result)
            else:
                report.image_filename = result

        if errors:
            for err in errors:
                flash(err, 'danger')
            return render_template(
                'citizen/edit_report.html',
                report=report,
                categories=Report.CATEGORIES
            )

        report.title = title
        report.description = description
        report.category = category
        report.location = location
        report.latitude = latitude
        report.longitude = longitude

        db.session.commit()
        flash("Your waste report has been updated successfully.", "success")
        return redirect(url_for('citizen.report_detail', report_id=report.id))

    return render_template('citizen/edit_report.html', report=report, categories=Report.CATEGORIES)

"""
Administrator routes for managing waste reports, updating status, viewing audit logs, and analytics.
"""
import os
from pathlib import Path
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, abort
from models import db, Report, User, ActivityLog
from utils.security import admin_required, validate_csrf

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    """Administrator dashboard overview with aggregate metrics, charts, and activity logs."""
    total_reports = Report.query.count()
    pending_reports = Report.query.filter_by(status='Reported').count()
    in_progress_reports = Report.query.filter_by(status='In Progress').count()
    resolved_reports = Report.query.filter_by(status='Resolved').count()
    rejected_reports = Report.query.filter_by(status='Rejected').count()
    total_citizens = User.query.filter_by(role='citizen').count()

    # Category counts
    category_counts = {}
    for cat in Report.CATEGORIES:
        category_counts[cat] = Report.query.filter_by(category=cat).count()

    # Status counts
    status_counts = {
        'Reported': pending_reports,
        'In Progress': in_progress_reports,
        'Resolved': resolved_reports,
        'Rejected': rejected_reports
    }

    # Recent submissions
    recent_reports = (
        Report.query
        .order_by(Report.created_at.desc())
        .limit(6)
        .all()
    )

    # Recent activity logs
    recent_logs = (
        ActivityLog.query
        .order_by(ActivityLog.created_at.desc())
        .limit(8)
        .all()
    )

    stats = {
        'total': total_reports,
        'pending': pending_reports,
        'in_progress': in_progress_reports,
        'resolved': resolved_reports,
        'rejected': rejected_reports,
        'citizens': total_citizens,
        'category_counts': category_counts,
        'status_counts': status_counts
    }

    return render_template(
        'admin/dashboard.html',
        stats=stats,
        recent_reports=recent_reports,
        recent_logs=recent_logs,
        statuses=Report.STATUSES
    )


@admin_bp.route('/reports')
@admin_required
def manage_reports():
    """Administrative reports management table with multi-criteria filters, search, and sorting."""
    query = Report.query

    # Search filter
    search = request.args.get('q', '').strip()
    if search:
        query = query.outerjoin(User, Report.user_id == User.id).filter(
            (Report.title.ilike(f"%{search}%")) |
            (Report.location.ilike(f"%{search}%")) |
            (Report.description.ilike(f"%{search}%")) |
            (User.name.ilike(f"%{search}%"))
        )

    # Category filter
    category = request.args.get('category', '').strip()
    if category and category in Report.CATEGORIES:
        query = query.filter(Report.category == category)

    # Status filter
    status = request.args.get('status', '').strip()
    if status and status in Report.STATUSES:
        query = query.filter(Report.status == status)

    # Sorting
    sort = request.args.get('sort', 'newest')
    if sort == 'oldest':
        query = query.order_by(Report.created_at.asc())
    else:
        query = query.order_by(Report.created_at.desc())

    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = 10
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        'admin/manage_reports.html',
        reports=pagination.items,
        pagination=pagination,
        categories=Report.CATEGORIES,
        statuses=Report.STATUSES,
        current_search=search,
        current_category=category,
        current_status=status,
        current_sort=sort
    )


@admin_bp.route('/reports/<int:report_id>/status', methods=['POST'])
@admin_required
def update_report_status(report_id):
    """Update report status and administrator notes, recording an activity log."""
    csrf_token = request.form.get('csrf_token')
    if not validate_csrf(csrf_token):
        flash('Security token invalid or expired.', 'danger')
        return redirect(url_for('admin.manage_reports'))

    report = db.get_or_404(Report, report_id)
    new_status = request.form.get('status', '').strip()
    admin_notes = request.form.get('admin_notes', '').strip()

    if new_status not in Report.STATUSES:
        flash('Invalid status provided.', 'danger')
        return redirect(url_for('admin.manage_reports'))

    old_status = report.status
    report.status = new_status
    if admin_notes:
        report.admin_notes = admin_notes

    # Create Activity Log
    action_text = f"Status updated from '{old_status}' to '{new_status}'"
    log = ActivityLog(
        admin_user_id=session['user_id'],
        report_id=report.id,
        action=action_text,
        details=f"Admin Notes: {admin_notes}" if admin_notes else "No notes provided."
    )
    db.session.add(log)
    db.session.commit()

    flash(f"Report #{report.id} successfully updated to '{new_status}'.", "success")
    
    # Redirect back to referring page if available
    next_page = request.form.get('redirect_to')
    if next_page == 'detail':
        return redirect(url_for('citizen.report_detail', report_id=report.id))
    elif next_page == 'dashboard':
        return redirect(url_for('admin.dashboard'))
    return redirect(url_for('admin.manage_reports'))


@admin_bp.route('/reports/<int:report_id>/delete', methods=['POST'])
@admin_required
def delete_report(report_id):
    """Delete an inappropriate, duplicate, or spam report with activity logging."""
    csrf_token = request.form.get('csrf_token')
    if not validate_csrf(csrf_token):
        flash('Security token invalid or expired.', 'danger')
        return redirect(url_for('admin.manage_reports'))

    report = db.get_or_404(Report, report_id)
    report_title = report.title

    # Remove attached image if exists
    if report.image_filename:
        file_path = Path(current_app.config['UPLOAD_FOLDER']) / report.image_filename
        if file_path.exists():
            try:
                os.remove(file_path)
            except Exception:
                pass

    # Create Activity Log before deletion
    log = ActivityLog(
        admin_user_id=session['user_id'],
        report_id=None,
        action=f"Deleted report #{report.id} ('{report_title}')",
        details="Report removed as duplicate, spam, or inappropriate by administrator."
    )
    db.session.add(log)
    db.session.delete(report)
    db.session.commit()

    flash(f"Report #{report_id} ('{report_title}') has been permanently removed.", "warning")
    return redirect(url_for('admin.manage_reports'))


@admin_bp.route('/logs')
@admin_required
def activity_logs():
    """Audit log history displaying all administrative modifications."""
    query = ActivityLog.query.order_by(ActivityLog.created_at.desc())

    # Search filter
    search = request.args.get('q', '').strip()
    if search:
        query = query.filter(
            (ActivityLog.action.ilike(f"%{search}%")) |
            (ActivityLog.details.ilike(f"%{search}%"))
        )

    page = request.args.get('page', 1, type=int)
    per_page = 15
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        'admin/logs.html',
        logs=pagination.items,
        pagination=pagination,
        current_search=search
    )

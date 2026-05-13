from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db
from models.models import User, LostItem, FoundItem, Claim

admin = Blueprint('admin', __name__)

@admin.before_request
@login_required
def require_admin():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.dashboard'))

@admin.route('/dashboard')
def admin_dashboard():
    users_count = User.query.count()
    lost_items_count = LostItem.query.count()
    found_items_count = FoundItem.query.count()
    claims_count = Claim.query.filter_by(status='pending').count()
    recent_lost = LostItem.query.order_by(LostItem.created_at.desc()).limit(5).all()
    recent_found = FoundItem.query.order_by(FoundItem.created_at.desc()).limit(5).all()
    return render_template('admin_dashboard.html', title='Admin Dashboard',
                          users_count=users_count, lost_items_count=lost_items_count,
                          found_items_count=found_items_count, claims_count=claims_count,
                          recent_lost=recent_lost, recent_found=recent_found)

@admin.route('/manage_reports')
def manage_reports():
    lost_items = LostItem.query.all()
    found_items = FoundItem.query.all()
    return render_template('manage_reports.html', title='Manage Reports',
                          lost_items=lost_items, found_items=found_items)

@admin.route('/manage_users')
def manage_users():
    users = User.query.all()
    return render_template('manage_users.html', title='Manage Users', users=users)

@admin.route('/claim_requests')
def claim_requests():
    claims = Claim.query.filter_by(status='pending').all()
    return render_template('claim_requests.html', title='Claim Requests', claims=claims)

@admin.route('/approve_claim/<int:claim_id>')
def approve_claim(claim_id):
    claim = Claim.query.get_or_404(claim_id)
    claim.status = 'approved'
    if claim.item_type == 'lost':
        item = LostItem.query.get(claim.item_id)
        item.status = 'claimed'
    else:
        item = FoundItem.query.get(claim.item_id)
        item.status = 'claimed'
    db.session.commit()
    flash('Claim approved successfully!', 'success')
    return redirect(url_for('admin.claim_requests'))

@admin.route('/reject_claim/<int:claim_id>')
def reject_claim(claim_id):
    claim = Claim.query.get_or_404(claim_id)
    claim.status = 'rejected'
    db.session.commit()
    flash('Claim rejected!', 'warning')
    return redirect(url_for('admin.claim_requests'))

@admin.route('/delete_report/<item_type>/<int:item_id>')
def delete_report(item_type, item_id):
    if item_type == 'lost':
        item = LostItem.query.get_or_404(item_id)
    else:
        item = FoundItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Report deleted successfully!', 'success')
    return redirect(url_for('admin.manage_reports'))

@admin.route('/mark_returned/<item_type>/<int:item_id>')
def mark_returned(item_type, item_id):
    if item_type == 'lost':
        item = LostItem.query.get_or_404(item_id)
    else:
        item = FoundItem.query.get_or_404(item_id)
    item.status = 'returned'
    db.session.commit()
    flash('Item marked as returned!', 'success')
    return redirect(url_for('admin.manage_reports'))
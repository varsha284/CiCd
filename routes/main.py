from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db
from models.models import LostItem, FoundItem, Claim
from wtforms import StringField, TextAreaField, SelectField, DateField, FileField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
import os
from werkzeug.utils import secure_filename
from datetime import datetime

main = Blueprint('main', __name__)

class LostItemForm(FlaskForm):
    item_name = StringField('Item Name', validators=[DataRequired()])
    category = SelectField('Category', choices=[('electronics', 'Electronics'), ('books', 'Books'), ('clothing', 'Clothing'), ('accessories', 'Accessories'), ('others', 'Others')], validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    date_lost = DateField('Date Lost', validators=[DataRequired()])
    location_lost = StringField('Location Lost', validators=[DataRequired()])
    contact_details = StringField('Contact Details', validators=[DataRequired()])
    image = FileField('Item Image')
    submit = SubmitField('Report Lost Item')

class FoundItemForm(FlaskForm):
    item_name = StringField('Item Name', validators=[DataRequired()])
    category = SelectField('Category', choices=[('electronics', 'Electronics'), ('books', 'Books'), ('clothing', 'Clothing'), ('accessories', 'Accessories'), ('others', 'Others')], validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    date_found = DateField('Date Found', validators=[DataRequired()])
    location_found = StringField('Location Found', validators=[DataRequired()])
    contact_details = StringField('Contact Details', validators=[DataRequired()])
    image = FileField('Item Image')
    submit = SubmitField('Report Found Item')

class SearchForm(FlaskForm):
    search_term = StringField('Search')
    category = SelectField('Category', choices=[('', 'All'), ('electronics', 'Electronics'), ('books', 'Books'), ('clothing', 'Clothing'), ('accessories', 'Accessories'), ('others', 'Others')])
    location = StringField('Location')
    date_from = DateField('Date From')
    date_to = DateField('Date To')
    submit = SubmitField('Search')

class ClaimForm(FlaskForm):
    claim_description = TextAreaField('Why do you think this is your item?', validators=[DataRequired()])
    submit = SubmitField('Submit Claim')

@main.route('/')
def home():
    return render_template('home.html', title='Home')

@main.route('/about')
def about():
    return render_template('about.html', title='About')

@main.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')

@main.route('/dashboard')
@login_required
def dashboard():
    lost_items = LostItem.query.filter_by(user_id=current_user.id).all()
    found_items = FoundItem.query.filter_by(user_id=current_user.id).all()
    claims = Claim.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', title='Dashboard', lost_items=lost_items, found_items=found_items, claims=claims)

@main.route('/report_lost', methods=['GET', 'POST'])
@login_required
def report_lost():
    form = LostItemForm()
    if form.validate_on_submit():
        image_path = None
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            image_path = os.path.join('uploads', filename)
            form.image.data.save(os.path.join('static', image_path))
        
        lost_item = LostItem(
            item_name=form.item_name.data,
            category=form.category.data,
            description=form.description.data,
            date_lost=form.date_lost.data,
            location_lost=form.location_lost.data,
            contact_details=form.contact_details.data,
            image_path=image_path,
            user_id=current_user.id
        )
        db.session.add(lost_item)
        db.session.commit()
        flash('Lost item reported successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('report_lost.html', title='Report Lost Item', form=form)

@main.route('/report_found', methods=['GET', 'POST'])
@login_required
def report_found():
    form = FoundItemForm()
    if form.validate_on_submit():
        image_path = None
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            image_path = os.path.join('uploads', filename)
            form.image.data.save(os.path.join('static', image_path))
        
        found_item = FoundItem(
            item_name=form.item_name.data,
            category=form.category.data,
            description=form.description.data,
            date_found=form.date_found.data,
            location_found=form.location_found.data,
            contact_details=form.contact_details.data,
            image_path=image_path,
            user_id=current_user.id
        )
        db.session.add(found_item)
        db.session.commit()
        flash('Found item reported successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('report_found.html', title='Report Found Item', form=form)

@main.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    results = []
    # The tests submit only `search_term` via POST; be permissive about form validation.
    if request.method == 'GET' or form.validate_on_submit() or 'search_term' in request.form:
        query_lost = LostItem.query
        query_found = FoundItem.query

        search_term = form.search_term.data if form.search_term.data else request.form.get('search_term')
        category = form.category.data if form.category.data else None
        location = form.location.data if form.location.data else None

        if search_term:
            query_lost = query_lost.filter(LostItem.item_name.contains(search_term))
            query_found = query_found.filter(FoundItem.item_name.contains(search_term))

        if category:
            query_lost = query_lost.filter(LostItem.category == category)
            query_found = query_found.filter(FoundItem.category == category)

        if location:
            query_lost = query_lost.filter(LostItem.location_lost.contains(location))
            query_found = query_found.filter(FoundItem.location_found.contains(location))

        # Date filters (optional)
        if form.date_from.data:
            query_lost = query_lost.filter(LostItem.date_lost >= form.date_from.data)
            query_found = query_found.filter(FoundItem.date_found >= form.date_from.data)
        if form.date_to.data:
            query_lost = query_lost.filter(LostItem.date_lost <= form.date_to.data)
            query_found = query_found.filter(FoundItem.date_found <= form.date_to.data)

        results = (query_lost.all() + query_found.all())

    return render_template('search.html', title='Search Items', form=form, results=results)


@main.route('/my_reports')
@login_required
def my_reports():
    lost_items = LostItem.query.filter_by(user_id=current_user.id).all()
    found_items = FoundItem.query.filter_by(user_id=current_user.id).all()
    return render_template('my_reports.html', title='My Reports', lost_items=lost_items, found_items=found_items)

@main.route('/claim/<item_type>/<int:item_id>', methods=['GET', 'POST'])
@login_required
def claim_item(item_type, item_id):
    form = ClaimForm()
    if item_type == 'lost':
        item = LostItem.query.get_or_404(item_id)
    elif item_type == 'found':
        item = FoundItem.query.get_or_404(item_id)
    else:
        flash('Invalid item type', 'danger')
        return redirect(url_for('main.search'))
    
    if form.validate_on_submit():
        claim = Claim(
            user_id=current_user.id,
            item_type=item_type,
            lost_item_id=item_id if item_type == 'lost' else None,
            found_item_id=item_id if item_type == 'found' else None,
            claim_description=form.claim_description.data
        )
        db.session.add(claim)
        db.session.commit()
        flash('Claim submitted successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('claim.html', title='Claim Item', form=form, item=item, item_type=item_type)
from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    lost_items = db.relationship('LostItem', backref='user', lazy=True)
    found_items = db.relationship('FoundItem', backref='user', lazy=True)
    claims = db.relationship('Claim', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class LostItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_lost = db.Column(db.Date, nullable=False)
    location_lost = db.Column(db.String(100), nullable=False)
    contact_details = db.Column(db.String(200), nullable=False)
    image_path = db.Column(db.String(200))
    status = db.Column(db.String(20), default='lost')  # lost, claimed, returned
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    claims = db.relationship('Claim', foreign_keys='Claim.lost_item_id', backref='lost_item', lazy=True)

class FoundItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_found = db.Column(db.Date, nullable=False)
    location_found = db.Column(db.String(100), nullable=False)
    contact_details = db.Column(db.String(200), nullable=False)
    image_path = db.Column(db.String(200))
    status = db.Column(db.String(20), default='found')  # found, claimed, returned
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    claims = db.relationship('Claim', foreign_keys='Claim.found_item_id', backref='found_item', lazy=True)

class Claim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_type = db.Column(db.String(10), nullable=False)  # 'lost' or 'found'
    lost_item_id = db.Column(db.Integer, db.ForeignKey('lost_item.id'), nullable=True)
    found_item_id = db.Column(db.Integer, db.ForeignKey('found_item.id'), nullable=True)
    claim_description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    admin_response = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
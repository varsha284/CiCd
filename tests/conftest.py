import pytest
from datetime import date
from app import create_app
from models import db
from models.models import User, LostItem, FoundItem, Claim


@pytest.fixture
def app():
    """Create and configure a test app instance."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False

    with app.app_context():
        # Fresh schema for each test run.
        db.drop_all()
        db.create_all()



    yield app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def test_user(app):
    """Create a test user."""
    with app.app_context():
        user = User(username='testuser', email='test@example.com')
        user.set_password('password')
        try:
            db.session.add(user)
            db.session.commit()
        except:
            db.session.rollback()
            # User might already exist, just fetch it
            user = User.query.filter_by(email='test@example.com').first()
            if user is not None:
                # Re-bind by refreshing while the session is active
                user = User.query.filter_by(email='test@example.com').first()

        # Force-load primary key
        _ = user.id
        return user


@pytest.fixture
def test_admin(app):
    """Create a test admin user."""
    with app.app_context():
        admin = User(username='admin', email='admin@example.com', is_admin=True)
        admin.set_password('adminpass')
        try:
            db.session.add(admin)
            db.session.commit()
        except:
            db.session.rollback()
            admin = User.query.filter_by(email='admin@example.com').first()
        return admin


@pytest.fixture
def test_lost_item(app, test_user):
    """Create a test lost item."""
    with app.app_context():
        item = LostItem(
            item_name='Test Wallet',
            category='accessories',
            description='Black leather wallet',
            date_lost=date(2024, 1, 1),
            location_lost='Library',
            contact_details='123-456-7890',
            user_id=test_user.id
        )
        db.session.add(item)
        db.session.commit()

        # Force-load PK then detach to prevent lazy-loading outside session
        _ = item.id
        db.session.expunge(item)
        return item


@pytest.fixture
def test_found_item(app, test_user):
    """Create a test found item."""
    with app.app_context():
        item = FoundItem(
            item_name='Test Keys',
            category='accessories',
            description='Car keys',
            date_found=date(2024, 1, 1),
            location_found='Parking Lot',
            contact_details='123-456-7890',
            user_id=test_user.id
        )
        db.session.add(item)
        db.session.commit()

        _ = item.id
        db.session.expunge(item)
        return item


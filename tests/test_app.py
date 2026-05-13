import pytest
from datetime import date
from app import create_app
from models import db
from models.models import User, LostItem, FoundItem, Claim

def test_home_page(client):
    """Test home page loads."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Campus Lost & Found' in response.data

def test_register(client):
    """Test user registration."""
    response = client.post('/register', data={
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Registration successful' in response.data

def test_login(client, test_user):
    """Test user login."""
    response = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Dashboard' in response.data

def test_logout(client, test_user):
    """Test user logout."""
    client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password'
    })
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data

def test_report_lost_item(client, test_user):
    """Test reporting a lost item."""
    client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password'
    })
    
    response = client.post('/report_lost', data={
        'item_name': 'Test Item',
        'category': 'electronics',
        'description': 'A test item',
        'date_lost': '2024-01-01',
        'location_lost': 'Classroom',
        'contact_details': '123-456-7890'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Lost item reported successfully' in response.data

def test_report_found_item(client, test_user):
    """Test reporting a found item."""
    client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password'
    })
    
    response = client.post('/report_found', data={
        'item_name': 'Found Item',
        'category': 'books',
        'description': 'A found book',
        'date_found': '2024-01-01',
        'location_found': 'Cafeteria',
        'contact_details': '123-456-7890'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Found item reported successfully' in response.data

def test_search_items(client, test_user, test_lost_item):
    """Test searching for items."""
    client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password'
    })
    
    response = client.post('/search', data={
        'search_term': 'wallet'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Test Wallet' in response.data

def test_claim_item(client, test_user, test_lost_item):
    """Test claiming an item."""
    client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password'
    })
    
    response = client.post(f'/claim/lost/{test_lost_item.id}', data={
        'claim_description': 'This is my wallet'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Claim submitted successfully' in response.data

def test_admin_access(client, test_admin):
    """Test admin access to dashboard."""
    client.post('/login', data={
        'email': 'admin@example.com',
        'password': 'adminpass'
    })
    
    response = client.get('/admin/dashboard', follow_redirects=True)
    assert response.status_code == 200
    assert b'Admin Dashboard' in response.data

def test_unauthorized_admin_access(client, test_user):
    """Test that regular users cannot access admin pages."""
    client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password'
    })
    
    response = client.get('/admin/dashboard', follow_redirects=True)
    assert b'Access denied' in response.data

def test_database_models(app):
    """Test database models creation."""
    with app.app_context():
        # Test User model
        user = User(username='test', email='test@test.com')
        user.set_password('pass')
        db.session.add(user)
        db.session.commit()
        
        assert user.id is not None
        assert user.check_password('pass')
        
        # Test LostItem model
        lost_item = LostItem(
            item_name='Phone',
            category='electronics',
            description='iPhone',
            date_lost=date(2024, 1, 1),
            location_lost='Gym',
            contact_details='555-1234',
            user_id=user.id
        )
        db.session.add(lost_item)
        db.session.commit()
        
        assert lost_item.id is not None
        assert lost_item.status == 'lost'
        
        # Test FoundItem model
        found_item = FoundItem(
            item_name='Book',
            category='books',
            description='Math textbook',
            date_found=date(2024, 1, 1),
            location_found='Library',
            contact_details='555-5678',
            user_id=user.id
        )
        db.session.add(found_item)
        db.session.commit()
        
        assert found_item.id is not None
        assert found_item.status == 'found'
        
        # Test Claim model
        claim = Claim(
            user_id=user.id,
            item_type='lost',
            lost_item_id=lost_item.id,
            claim_description='This is my phone'
        )
        db.session.add(claim)
        db.session.commit()
        
        assert claim.id is not None
        assert claim.status == 'pending'
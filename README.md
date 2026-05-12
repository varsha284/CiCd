# Campus Lost & Found Portal

A comprehensive web application for college students to report and recover lost and found items. Built with Python Flask, featuring a modern responsive UI, secure authentication, and CI/CD integration with AWS services.

## Features

### 🔐 Authentication System
- User registration and login
- Secure password hashing
- Session management
- Role-based access (User/Admin)

### 📦 Item Management
- Report lost items with photos
- Report found items
- Advanced search functionality
- Category-based organization

### 🔍 Search & Discovery
- Search by item name, category, location, date
- Filter results
- View item details and images

### 📋 Claim System
- Submit ownership claims
- Admin approval/rejection process
- Claim status tracking

### 👨‍💼 Admin Dashboard
- Manage users and reports
- Approve/reject claims
- View analytics and statistics
- Delete inappropriate reports

### 🎨 Modern UI/UX
- Responsive Bootstrap 5 design
- Blue/white professional theme
- Smooth animations and hover effects
- Mobile-friendly interface
- Dark mode toggle (placeholder)

## Tech Stack

- **Backend**: Python Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Authentication**: Flask-Login, Werkzeug
- **Forms**: Flask-WTF
- **Testing**: Pytest
- **CI/CD**: AWS CodeCommit, CodePipeline, CodeBuild

## Project Structure

```
campus-lost-found/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── buildspec.yml              # AWS CodeBuild configuration
├── README.md                  # Project documentation
├── config/
│   └── __init__.py           # Configuration settings
├── models/
│   ├── __init__.py           # Database initialization
│   └── models.py             # SQLAlchemy models
├── routes/
│   ├── __init__.py           # Blueprint imports
│   ├── auth.py               # Authentication routes
│   ├── main.py               # Main user routes
│   └── admin.py              # Admin routes
├── static/
│   ├── css/
│   │   └── style.css         # Custom styles
│   ├── js/
│   │   └── script.js         # JavaScript functionality
│   └── images/               # Static images
├── templates/                 # Jinja2 templates
│   ├── base.html             # Base template
│   ├── home.html             # Home page
│   ├── login.html            # Login page
│   ├── register.html         # Registration page
│   ├── dashboard.html        # User dashboard
│   ├── admin_dashboard.html  # Admin dashboard
│   └── ...                   # Other templates
└── tests/
    ├── __init__.py           # Test package
    ├── conftest.py           # Test fixtures
    └── test_app.py           # Test cases
```

## Database Schema

### Users Table
- id (Primary Key)
- username (Unique)
- email (Unique)
- password_hash
- is_admin (Boolean)
- created_at

### Lost Items Table
- id (Primary Key)
- item_name
- category
- description
- date_lost
- location_lost
- contact_details
- image_path
- status
- user_id (Foreign Key)

### Found Items Table
- id (Primary Key)
- item_name
- category
- description
- date_found
- location_found
- contact_details
- image_path
- status
- user_id (Foreign Key)

### Claims Table
- id (Primary Key)
- user_id (Foreign Key)
- item_type
- item_id
- claim_description
- status
- admin_response
- created_at
- updated_at

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip package manager

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd campus-lost-found
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables** (optional)
   ```bash
   export SECRET_KEY='your-secret-key'
   export DATABASE_URL='sqlite:///campus_lost_found.db'
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   - Open http://localhost:5000 in your browser
   - Register a new account or login

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_app.py

# Run with coverage
pytest --cov=.
```

## CI/CD Pipeline

### AWS Services Integration

1. **AWS CodeCommit**: Store source code
2. **AWS CodePipeline**: Orchestrate CI/CD workflow
3. **AWS CodeBuild**: Build and test application

### Pipeline Stages

1. **Source**: Code changes trigger pipeline
2. **Build**: Install dependencies and run tests
3. **Deploy**: Deploy to staging/production (future enhancement)

### Build Configuration

The `buildspec.yml` file defines:
- Python runtime version
- Dependency installation
- Test execution
- Artifact generation

## Usage Guide

### For Students

1. **Register**: Create account with email and password
2. **Login**: Access your dashboard
3. **Report Lost Items**: Add details and upload photos
4. **Report Found Items**: Help others recover items
5. **Search**: Find items using filters
6. **Claim Items**: Submit ownership claims

### For Admins

1. **Access Admin Panel**: Login with admin account
2. **Manage Reports**: View, edit, delete reports
3. **Handle Claims**: Approve or reject claims
4. **User Management**: Monitor user activity
5. **View Analytics**: Track system statistics

## Security Features

- Password hashing with Werkzeug
- CSRF protection with Flask-WTF
- SQL injection prevention with SQLAlchemy
- Secure session management
- File upload restrictions
- Admin role validation

## API Endpoints

### Authentication
- `GET/POST /register` - User registration
- `GET/POST /login` - User login
- `GET /logout` - User logout

### User Routes
- `GET /` - Home page
- `GET /dashboard` - User dashboard
- `GET/POST /report_lost` - Report lost item
- `GET/POST /report_found` - Report found item
- `GET/POST /search` - Search items
- `GET /my_reports` - User's reports
- `GET/POST /claim/<type>/<id>` - Claim item

### Admin Routes
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/manage_reports` - Manage all reports
- `GET /admin/manage_users` - Manage users
- `GET /admin/claim_requests` - Handle claims
- `GET /admin/approve_claim/<id>` - Approve claim
- `GET /admin/reject_claim/<id>` - Reject claim

## Testing

The application includes comprehensive test coverage:

- User registration and authentication
- Item reporting functionality
- Search and filtering
- Claim submission process
- Admin panel access
- Database model validation

Run tests with:
```bash
pytest tests/ -v --tb=short
```

## Deployment

### AWS Deployment (Conceptual)

1. **CodeCommit Setup**
   - Create repository
   - Push code to CodeCommit

2. **CodePipeline Configuration**
   - Source: CodeCommit
   - Build: CodeBuild
   - Deploy: Manual or automated

3. **CodeBuild Setup**
   - Use provided `buildspec.yml`
   - Configure environment variables
   - Set up build triggers

### Local Production

```bash
# Set production environment
export FLASK_ENV=production
export SECRET_KEY='strong-secret-key'

# Run with production server
gunicorn app:create_app() -b 0.0.0.0:8000
```

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## Future Enhancements

- [ ] Email notifications for claims
- [ ] Real-time chat between users and admins
- [ ] Advanced image recognition for item matching
- [ ] Mobile app companion
- [ ] Multi-language support
- [ ] Integration with campus directory
- [ ] QR code generation for items
- [ ] Analytics dashboard improvements

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Bootstrap 5 for responsive design
- Flask community for excellent documentation
- Font Awesome for icons
- AWS for CI/CD services

## Support

For support or questions:
- Email: support@campuslostfound.edu
- GitHub Issues: Report bugs or request features

---

**Note**: This is a college mini-project suitable for demonstration and learning purposes. For production use, additional security measures and scalability considerations would be required.
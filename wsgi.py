"""
WSGI application entry point for production deployment.
Used by Gunicorn, AWS Elastic Beanstalk, and other WSGI servers.

Usage:
    gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
    
AWS Elastic Beanstalk automatically detects this file.
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()

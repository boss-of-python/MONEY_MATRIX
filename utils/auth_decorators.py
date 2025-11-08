"""
Authentication Decorators
Flask route decorators for authentication and authorization
"""

from functools import wraps
from flask import request, jsonify, g
from .firebase_helpers import verify_token, get_user_from_token
import logging

logger = logging.getLogger(__name__)


def require_auth(f):
    """
    Decorator to require Firebase authentication
    Verifies ID token from Authorization header
    
    Usage:
        @app.route('/protected')
        @require_auth
        def protected_route():
            user_id = g.user_id  # Access authenticated user ID
            return {'message': 'Success'}
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization', '')
        token = auth_header.replace('Bearer ', '').strip()
        
        if not token:
            return jsonify({'error': 'No authentication token provided'}), 401
        
        # Verify token with Firebase
        decoded_token = verify_token(token)
        
        if not decoded_token:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Store user ID in Flask g object for access in route
        g.user_id = decoded_token.get('uid')
        g.user_email = decoded_token.get('email')
        
        return f(*args, **kwargs)
    
    return decorated_function


def require_admin(f):
    """
    Decorator to require admin role
    Checks Firebase custom claims for admin role
    
    Usage:
        @app.route('/admin')
        @require_admin
        def admin_route():
            return {'message': 'Admin access granted'}
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization', '')
        token = auth_header.replace('Bearer ', '').strip()
        
        if not token:
            return jsonify({'error': 'No authentication token provided'}), 401
        
        # Verify token and get user
        decoded_token = verify_token(token)
        
        if not decoded_token:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Check for admin custom claim
        is_admin = decoded_token.get('admin', False)
        
        if not is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        
        # Store user info in g object
        g.user_id = decoded_token.get('uid')
        g.user_email = decoded_token.get('email')
        g.is_admin = True
        
        return f(*args, **kwargs)
    
    return decorated_function


def optional_auth(f):
    """
    Decorator for optional authentication
    Sets g.user_id if authenticated, otherwise None
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization', '')
        token = auth_header.replace('Bearer ', '').strip()
        
        if token:
            decoded_token = verify_token(token)
            if decoded_token:
                g.user_id = decoded_token.get('uid')
                g.user_email = decoded_token.get('email')
            else:
                g.user_id = None
                g.user_email = None
        else:
            g.user_id = None
            g.user_email = None
        
        return f(*args, **kwargs)
    
    return decorated_function


def login_required(f):
    """
    Alias for require_auth for consistency with Flask-Login naming
    Also sets g.user_id and g.user_email for easier access in routes
    In development mode without Firebase, allows access with a demo user
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization', '')
        token = auth_header.replace('Bearer ', '').strip()
        
        if not token:
            # Check if Firebase is configured
            try:
                from firebase_admin import auth as firebase_auth
                from flask import current_app
                
                # If Firebase is not initialized, allow demo access in development
                if current_app.config.get('DEBUG', False):
                    logger.warning('Firebase not configured - using demo user for development')
                    g.user_id = 'demo-user-id'
                    g.user_email = 'demo@example.com'
                    return f(*args, **kwargs)
                else:
                    return jsonify({'error': 'Authentication required'}), 401
            except Exception:
                # Firebase not initialized - allow demo access in development
                from flask import current_app
                if current_app.config.get('DEBUG', False):
                    logger.warning('Firebase not configured - using demo user for development')
                    g.user_id = 'demo-user-id'
                    g.user_email = 'demo@example.com'
                    return f(*args, **kwargs)
                else:
                    return jsonify({'error': 'Authentication required'}), 401
        
        # Verify token with Firebase
        decoded_token = verify_token(token)
        
        if not decoded_token:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Store user ID in Flask g object for access in route
        g.user_id = decoded_token.get('uid')
        g.user_email = decoded_token.get('email')
        
        return f(*args, **kwargs)
    
    return decorated_function

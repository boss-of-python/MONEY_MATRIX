"""
Authentication Feature - Initialization
Handles Firebase-based user authentication
"""

from flask import Blueprint


def init_feature(app):
    """
    Initialize authentication feature
    
    Args:
        app: Flask application instance
    
    Returns:
        Blueprint: Configured Flask Blueprint
    """
    bp = Blueprint(
        'auth',
        __name__,
        template_folder='templates',
        static_folder='static',
        url_prefix='/auth'
    )
    
    # Import and register routes
    from .routes import register_routes
    register_routes(bp, app)
    
    return bp

"""
Cloud Sync Feature
Handles data synchronization between local and cloud storage
"""

from flask import Blueprint


def init_feature(app):
    """
    Initialize cloud sync feature
    
    Args:
        app: Flask application instance
    
    Returns:
        Blueprint: Configured Flask Blueprint
    """
    bp = Blueprint(
        'sync',
        __name__,
        url_prefix='/sync'
    )
    
    # Import and register routes
    from .routes import register_routes
    register_routes(bp, app)
    
    return bp

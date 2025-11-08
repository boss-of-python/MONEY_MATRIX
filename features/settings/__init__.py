"""
Settings Feature
User preferences and cloud sync management
"""

from flask import Blueprint


def init_feature(app):
    """
    Initialize settings feature
    
    Args:
        app: Flask application instance
    
    Returns:
        Blueprint: Configured Flask Blueprint
    """
    bp = Blueprint(
        'settings',
        __name__,
        template_folder='templates',
        url_prefix='/settings'
    )
    
    # Import and register routes
    from .routes import register_routes
    register_routes(bp, app)
    
    return bp

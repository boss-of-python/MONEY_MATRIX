"""Dashboard Feature Module"""
from flask import Blueprint

def init_feature(app):
    """Initialize dashboard feature"""
    bp = Blueprint(
        'dashboard',
        __name__,
        template_folder='templates',
        static_folder='static',
        url_prefix='/dashboard'
    )
    
    from .routes import register_routes
    register_routes(bp, app)
    
    return bp

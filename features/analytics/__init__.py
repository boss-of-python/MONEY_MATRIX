"""Analytics Feature Module"""
from flask import Blueprint

def init_feature(app):
    """Initialize analytics feature"""
    bp = Blueprint(
        'analytics',
        __name__,
        template_folder='templates',
        static_folder='static',
        url_prefix='/analytics'
    )
    
    from .routes import register_routes
    register_routes(bp, app)
    
    return bp

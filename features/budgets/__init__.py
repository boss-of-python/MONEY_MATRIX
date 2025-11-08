"""Budgets Feature Module"""
from flask import Blueprint

def init_feature(app):
    """Initialize budgets feature"""
    bp = Blueprint(
        'budgets',
        __name__,
        template_folder='templates',
        static_folder='static',
        url_prefix='/budgets'
    )
    
    from .routes import register_routes
    register_routes(bp, app)
    
    return bp

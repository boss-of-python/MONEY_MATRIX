"""Settings Routes"""
from flask import render_template
from utils.auth_decorators import login_required


def register_routes(bp, app):
    """Register settings routes"""
    
    @bp.route('/')
    @login_required
    def index():
        """Settings page"""
        return render_template('settings.html')

"""
Simple Preview Application for Money Matrix
This is a lightweight version that serves static files and templates
without database or Firebase dependencies for preview purposes.
"""

import os
from flask import Flask, render_template, send_from_directory

def create_preview_app():
    """Create a simple Flask app for preview purposes"""
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    
    # Serve static files
    @app.route('/static/<path:filename>')
    def static_files(filename):
        return send_from_directory('static', filename)
    
    # Serve CSS files specifically
    @app.route('/static/css/<path:filename>')
    def css_files(filename):
        return send_from_directory('static/css', filename)
    
    # Serve JS files specifically
    @app.route('/static/js/<path:filename>')
    def js_files(filename):
        return send_from_directory('static/js', filename)
    
    # Serve feature static files
    @app.route('/features/<feature>/static/<path:filename>')
    def feature_static_files(feature, filename):
        return send_from_directory(f'features/{feature}/static', filename)
    
    # Main routes
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/login')
    def login():
        return render_template('login.html')
    
    @app.route('/register')
    def register():
        return render_template('register.html')
    
    @app.route('/dashboard')
    def dashboard():
        # Demo mode - serve dashboard without authentication
        return render_template('dashboard.html')
    
    @app.route('/budgets')
    def budgets():
        return render_template('budgets.html')
    
    @app.route('/transactions')
    def transactions():
        return render_template('transactions.html')
    
    @app.route('/analytics')
    def analytics():
        return render_template('analytics.html')
    
    @app.route('/settings')
    def settings():
        return render_template('settings.html')
    
    @app.route('/export')
    def export():
        return render_template('export.html')
    
    @app.route('/help')
    def help():
        return render_template('help.html')
    
    return app

if __name__ == '__main__':
    app = create_preview_app()
    print("Money Matrix Preview Server Starting...")
    print("Access the application at: http://localhost:5000")
    print("Press CTRL+C to stop the server")
    app.run(host='localhost', port=5000, debug=True)
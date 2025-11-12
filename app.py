"""
Money Matrix - Flask Application Core
Commercial-Grade Personal Finance Platform

This is the main application entry point that implements a fail-safe
modular architecture with self-healing feature loading.
"""

import os
import sys
import logging
from flask import Flask, render_template, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import firebase_admin
from firebase_admin import credentials

# Import configuration
from config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)


# Global database session
db_session = None
firebase_app = None


def create_app(config_name='default'):
    """
    Application factory pattern
    Creates and configures the Flask application
    
    Args:
        config_name: Configuration name ('development', 'production', 'default')
    
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Enable CORS
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Initialize Firebase Admin SDK
    init_firebase(app)
    
    # Initialize Database
    init_database(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Load features (fail-safe modular system)
    load_features(app)
    
    # Register root route
    @app.route('/')
    def index():
        """Root route - redirect to dashboard if authenticated, else to login"""
        return render_template('index.html')
    
    @app.route('/dashboard')
    def dashboard():
        """Dashboard page for authenticated users"""
        return render_template('dashboard.html')
    
    @app.route('/transactions')
    def transactions():
        """Transactions page"""
        return render_template('transactions.html')
    
    @app.route('/budgets')
    def budgets():
        """Budgets page"""
        return render_template('budgets.html')
    
    @app.route('/analytics')
    def analytics():
        """Analytics page"""
        return render_template('analytics.html')
    
    @app.route('/settings')
    def settings():
        """Settings page"""
        return render_template('settings.html')
    
    @app.route('/export')
    def export_page():
        """Export page"""
        return render_template('export.html')
    
    @app.route('/help')
    def help_page():
        """Help page"""
        return render_template('help.html')
    
    @app.route('/api/config/firebase')
    def firebase_config():
        """Serve Firebase configuration for frontend"""
        return jsonify({
            'apiKey': app.config['FIREBASE_API_KEY'],
            'authDomain': app.config['FIREBASE_AUTH_DOMAIN'],
            'projectId': app.config['FIREBASE_PROJECT_ID'],
            'storageBucket': app.config['FIREBASE_STORAGE_BUCKET'],
            'messagingSenderId': app.config['FIREBASE_MESSAGING_SENDER_ID'],
            'appId': app.config['FIREBASE_APP_ID'],
            'measurementId': app.config['FIREBASE_MEASUREMENT_ID']
        }), 200
    
    logger.info(f"Money Matrix initialized in {config_name} mode")
    logger.info(f"Registered routes: {[str(rule) for rule in app.url_map.iter_rules()]}")
    
    return app


def init_firebase(app):
    """
    Initialize Firebase Admin SDK for authentication
    
    Args:
        app: Flask application instance
    """
    global firebase_app
    
    try:
        cred_path = app.config['FIREBASE_CREDENTIALS_PATH']
        
        if not os.path.exists(cred_path):
            logger.warning(f"Firebase credentials not found at {cred_path}")
            logger.warning("Authentication features will be disabled")
            return
        
        cred = credentials.Certificate(cred_path)
        firebase_app = firebase_admin.initialize_app(cred)
        
        logger.info("Firebase Admin SDK initialized successfully")
    
    except Exception as e:
        logger.error(f"Failed to initialize Firebase: {str(e)}")
        logger.warning("Application will continue without Firebase authentication")


def init_database(app):
    """
    Initialize SQLite database with SQLAlchemy
    
    Args:
        app: Flask application instance
    """
    global db_session
    
    try:
        # Create SQLAlchemy engine
        engine = create_engine(
            app.config['SQLALCHEMY_DATABASE_URI'],
            echo=app.config['SQLALCHEMY_ECHO'],
            pool_pre_ping=True
        )
        
        # Create session factory
        session_factory = sessionmaker(bind=engine)
        db_session = scoped_session(session_factory)
        
        # Store in app context for access in features
        app.db_engine = engine
        app.db_session = db_session
        
        logger.info(f"Database initialized: {app.config['SQLALCHEMY_DATABASE_URI']}")
        
        # Import base models and create tables
        from models.base import Base
        Base.metadata.create_all(engine)
        logger.info("Database tables created successfully")
    
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise


def register_error_handlers(app):
    """
    Register global error handlers for graceful error handling
    
    Args:
        app: Flask application instance
    """
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        if '/api/' in str(error):
            return jsonify({'error': 'Endpoint not found'}), 404
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        logger.error(f"Internal server error: {str(error)}")
        if db_session:
            db_session.rollback()
        
        if '/api/' in str(error):
            return jsonify({'error': 'Internal server error'}), 500
        return render_template('500.html'), 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        """Handle all unhandled exceptions"""
        logger.error(f"Unhandled exception: {str(error)}", exc_info=True)
        
        if db_session:
            db_session.rollback()
        
        return jsonify({'error': 'An unexpected error occurred'}), 500
    
    logger.info("Error handlers registered")


def load_features(app):
    """
    Fail-safe feature loading system
    Scans features/ directory and loads each feature module with exception isolation
    
    Args:
        app: Flask application instance
    """
    from features import FeatureRegistry
    
    try:
        registry = FeatureRegistry(app)
        loaded_count = registry.load_all_features()
        
        logger.info(f"Feature loading completed: {loaded_count} features loaded successfully")
        logger.info(f"Active features: {', '.join(registry.get_active_features())}")
        
        if registry.failed_features:
            logger.warning(f"Failed to load {len(registry.failed_features)} features:")
            for feature_name, error in registry.failed_features.items():
                logger.warning(f"  - {feature_name}: {error}")
    
    except Exception as e:
        logger.error(f"Feature loader crashed: {str(e)}")
        logger.warning("Application will continue without features")


def main():
    """Main application entry point"""
    # Get environment
    env = os.getenv('FLASK_ENV', 'development')
    
    # Create application
    app = create_app(env)
    
    # Run development server
    if app.config['DEBUG']:
        logger.info("Starting development server...")
        logger.info(f"Access the application at: http://{app.config['HOST']}:{app.config['PORT']}")
        app.run(
            host=app.config['HOST'],
            port=app.config['PORT'],
            debug=True
        )
    else:
        logger.info("Production mode - use a WSGI server (gunicorn, uwsgi)")
        return app


if __name__ == '__main__':
    main()
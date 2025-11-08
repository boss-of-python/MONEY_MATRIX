"""
Authentication Routes
Handles login, register, logout, password reset
"""

from flask import request, jsonify, render_template, redirect, url_for, session
from firebase_admin import auth
from models.user import User, UserSettings
from utils.validators import validate_email, validate_password
import logging

logger = logging.getLogger(__name__)


def register_routes(bp, app):
    """Register authentication routes"""
    
    @bp.route('/login', methods=['GET'])
    def login_page():
        """Render login page"""
        return render_template('login.html')
    
    @bp.route('/register', methods=['GET'])
    def register_page():
        """Render registration page"""
        return render_template('register.html')
    
    @bp.route('/reset-password', methods=['GET'])
    def reset_password_page():
        """Render password reset page"""
        return render_template('reset_password.html')
    
    @bp.route('/api/register', methods=['POST'])
    def register():
        """
        Register new user with Firebase
        POST /auth/api/register
        Body: {email, password, display_name}
        """
        try:
            data = request.get_json()
            email = data.get('email', '').strip()
            password = data.get('password', '')
            display_name = data.get('display_name', '').strip()
            
            # Validate email
            is_valid, error = validate_email(email)
            if not is_valid:
                return jsonify({'error': error}), 400
            
            # Validate password
            is_valid, error = validate_password(password)
            if not is_valid:
                return jsonify({'error': error}), 400
            
            # Create Firebase user
            user = auth.create_user(
                email=email,
                password=password,
                display_name=display_name
            )
            
            # Create local user record
            db_session = app.db_session
            new_user = User(
                firebase_uid=user.uid,
                email=email,
                display_name=display_name,
                is_active=True
            )
            db_session.add(new_user)
            
            # Create default user settings
            settings = UserSettings(
                firebase_uid=user.uid,
                theme='auto',
                currency='USD'
            )
            db_session.add(settings)
            
            db_session.commit()
            
            logger.info(f"New user registered: {email}")
            
            return jsonify({
                'success': True,
                'message': 'Registration successful',
                'uid': user.uid
            }), 201
        
        except auth.EmailAlreadyExistsError:
            return jsonify({'error': 'Email already registered'}), 400
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            if app.db_session:
                app.db_session.rollback()
            return jsonify({'error': 'Registration failed'}), 500
    
    @bp.route('/api/verify-token', methods=['POST'])
    def verify_token():
        """
        Verify Firebase ID token
        POST /auth/api/verify-token
        Body: {token}
        """
        try:
            data = request.get_json()
            id_token = data.get('token', '')
            
            if not id_token:
                return jsonify({'error': 'Token required'}), 400
            
            # Verify token with Firebase
            decoded_token = auth.verify_id_token(id_token)
            
            return jsonify({
                'success': True,
                'uid': decoded_token['uid'],
                'email': decoded_token.get('email')
            }), 200
        
        except Exception as e:
            logger.error(f"Token verification error: {str(e)}")
            return jsonify({'error': 'Invalid token'}), 401
    
    @bp.route('/api/reset-password', methods=['POST'])
    def request_password_reset():
        """
        Send password reset email
        POST /auth/api/reset-password
        Body: {email}
        """
        try:
            data = request.get_json()
            email = data.get('email', '').strip()
            
            # Validate email
            is_valid, error = validate_email(email)
            if not is_valid:
                return jsonify({'error': error}), 400
            
            # Generate password reset link (Firebase handles email sending)
            link = auth.generate_password_reset_link(email)
            
            logger.info(f"Password reset requested for: {email}")
            
            return jsonify({
                'success': True,
                'message': 'Password reset email sent'
            }), 200
        
        except auth.UserNotFoundError:
            # Don't reveal if email exists (security)
            return jsonify({
                'success': True,
                'message': 'If email exists, reset link has been sent'
            }), 200
        except Exception as e:
            logger.error(f"Password reset error: {str(e)}")
            return jsonify({'error': 'Failed to send reset email'}), 500
    
    @bp.route('/logout', methods=['POST'])
    def logout():
        """Logout user (clear session)"""
        session.clear()
        return jsonify({'success': True, 'message': 'Logged out'}), 200

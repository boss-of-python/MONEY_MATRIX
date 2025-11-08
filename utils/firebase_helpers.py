"""
Firebase Helper Functions
Utilities for Firebase Auth integration
"""

import logging
from typing import Optional, Dict

logger = logging.getLogger(__name__)


def verify_token(id_token: str) -> Optional[Dict]:
    """
    Verify Firebase ID token
    
    Args:
        id_token: Firebase ID token from client
    
    Returns:
        Decoded token dict if valid, None if invalid
    """
    try:
        from firebase_admin import auth
        
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    
    except Exception as e:
        logger.warning(f"Token verification failed: {str(e)}")
        return None


def get_user_from_token(id_token: str) -> Optional[Dict]:
    """
    Get user information from Firebase ID token
    
    Args:
        id_token: Firebase ID token
    
    Returns:
        User information dict or None
    """
    decoded_token = verify_token(id_token)
    
    if not decoded_token:
        return None
    
    return {
        'uid': decoded_token.get('uid'),
        'email': decoded_token.get('email'),
        'email_verified': decoded_token.get('email_verified'),
        'name': decoded_token.get('name'),
        'picture': decoded_token.get('picture')
    }


def create_custom_token(uid: str, additional_claims: Optional[Dict] = None) -> str:
    """
    Create a custom Firebase token
    
    Args:
        uid: User ID
        additional_claims: Additional claims to include in token
    
    Returns:
        Custom token string
    """
    try:
        from firebase_admin import auth
        
        token = auth.create_custom_token(uid, additional_claims)
        return token.decode('utf-8')
    
    except Exception as e:
        logger.error(f"Failed to create custom token: {str(e)}")
        raise


def set_admin_claim(uid: str):
    """
    Set admin custom claim for a user
    
    Args:
        uid: User ID
    """
    try:
        from firebase_admin import auth
        
        auth.set_custom_user_claims(uid, {'admin': True})
        logger.info(f"Admin claim set for user {uid}")
    
    except Exception as e:
        logger.error(f"Failed to set admin claim: {str(e)}")
        raise


def revoke_admin_claim(uid: str):
    """
    Revoke admin custom claim for a user
    
    Args:
        uid: User ID
    """
    try:
        from firebase_admin import auth
        
        auth.set_custom_user_claims(uid, {'admin': False})
        logger.info(f"Admin claim revoked for user {uid}")
    
    except Exception as e:
        logger.error(f"Failed to revoke admin claim: {str(e)}")
        raise

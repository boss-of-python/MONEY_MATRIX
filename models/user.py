"""
User Models
Extends Firebase Auth with local user data
"""

from sqlalchemy import Column, String, Boolean, DateTime
from datetime import datetime
from .base import Base, TimestampMixin


class User(Base, TimestampMixin):
    """
    User model - extends Firebase Auth
    Stores additional user profile information
    """
    __tablename__ = 'users'
    
    firebase_uid = Column(String(128), primary_key=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    display_name = Column(String(255))
    photo_url = Column(String(500))
    last_login = Column(DateTime)
    is_active = Column(Boolean, default=True, nullable=False)
    
    def __repr__(self):
        return f"<User {self.email}>"
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'firebase_uid': self.firebase_uid,
            'email': self.email,
            'display_name': self.display_name,
            'photo_url': self.photo_url,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class UserSettings(Base):
    """User preferences and settings"""
    __tablename__ = 'user_settings'
    
    firebase_uid = Column(String(128), primary_key=True, nullable=False)
    theme = Column(String(10), default='auto')  # 'light', 'dark', 'auto'
    currency = Column(String(3), default='USD')
    date_format = Column(String(20), default='MM/DD/YYYY')
    language = Column(String(5), default='en')
    
    def __repr__(self):
        return f"<UserSettings {self.firebase_uid}>"
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'theme': self.theme,
            'currency': self.currency,
            'date_format': self.date_format,
            'language': self.language
        }

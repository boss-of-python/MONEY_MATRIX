"""
SQLAlchemy Base Class
Foundation for all database models
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime
from datetime import datetime

# Create base class for all models
Base = declarative_base()


class TimestampMixin:
    """Mixin to add timestamp fields to models"""
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

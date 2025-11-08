"""
Transaction and Category Models
"""

from sqlalchemy import Column, Integer, String, Numeric, Date, Boolean, ForeignKey
from decimal import Decimal
from .base import Base, TimestampMixin


class Category(Base):
    """Transaction categories"""
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    firebase_uid = Column(String(128), nullable=True)  # NULL = default category
    name = Column(String(100), nullable=False)
    type = Column(String(10), nullable=False)  # 'income' or 'expense'
    icon = Column(String(50))
    color = Column(String(7))  # Hex color code
    is_default = Column(Boolean, default=False)
    
    def __repr__(self):
        return f"<Category {self.name} ({self.type})>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'icon': self.icon,
            'color': self.color,
            'is_default': self.is_default
        }


class Transaction(Base, TimestampMixin):
    """Financial transactions"""
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    firebase_uid = Column(String(128), nullable=False, index=True)
    amount = Column(Numeric(10, 2), nullable=False)
    type = Column(String(10), nullable=False)  # 'income' or 'expense'
    category_id = Column(Integer, ForeignKey('categories.id'))
    description = Column(String(500))
    date = Column(Date, nullable=False, index=True)
    is_deleted = Column(Boolean, default=False)
    
    def __repr__(self):
        return f"<Transaction {self.type} ${self.amount}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'amount': str(self.amount),
            'type': self.type,
            'category_id': self.category_id,
            'description': self.description,
            'date': self.date.isoformat() if self.date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

"""
Budget Model
"""

from sqlalchemy import Column, Integer, String, Numeric, Date, Boolean, ForeignKey
from .base import Base


class Budget(Base):
    """Budget tracking"""
    __tablename__ = 'budgets'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    firebase_uid = Column(String(128), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    limit_amount = Column(Numeric(10, 2), nullable=False)
    period = Column(String(20), nullable=False)  # 'weekly', 'monthly', 'yearly'
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<Budget {self.period} ${self.limit_amount}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'category_id': self.category_id,
            'limit_amount': str(self.limit_amount),
            'period': self.period,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'is_active': self.is_active
        }

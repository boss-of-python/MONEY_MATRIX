"""
Validation Utilities
Common validation functions for input data
"""

import re
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Tuple, Optional, Any


def validate_email(email: str) -> Tuple[bool, Optional[str]]:
    """
    Validate email format
    
    Args:
        email: Email string to validate
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not email:
        return False, "Email is required"
    
    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email):
        return False, "Invalid email format"
    
    if len(email) > 255:
        return False, "Email too long (max 255 characters)"
    
    return True, None


def validate_amount(amount: Any) -> Tuple[bool, Optional[str]]:
    """
    Validate monetary amount
    
    Args:
        amount: Amount to validate (can be string, int, float, Decimal)
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if amount is None or amount == '':
        return False, "Amount is required"
    
    try:
        # Convert to Decimal for precise decimal arithmetic
        decimal_amount = Decimal(str(amount))
        
        if decimal_amount <= 0:
            return False, "Amount must be greater than 0"
        
        if decimal_amount > Decimal('999999999.99'):
            return False, "Amount too large"
        
        # Check decimal places (max 2)
        if decimal_amount.as_tuple().exponent < -2:
            return False, "Amount can have maximum 2 decimal places"
        
        return True, None
    
    except (InvalidOperation, ValueError):
        return False, "Invalid amount format"


def validate_date(date_str: str, format_str: str = '%Y-%m-%d') -> Tuple[bool, Optional[str]]:
    """
    Validate date string
    
    Args:
        date_str: Date string to validate
        format_str: Expected date format (default: YYYY-MM-DD)
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not date_str:
        return False, "Date is required"
    
    try:
        parsed_date = datetime.strptime(date_str, format_str)
        
        # Check if date is not in the future
        if parsed_date.date() > datetime.now().date():
            return False, "Date cannot be in the future"
        
        # Check if date is not too old (100 years)
        min_date = datetime.now().replace(year=datetime.now().year - 100)
        if parsed_date < min_date:
            return False, "Date is too old"
        
        return True, None
    
    except ValueError:
        return False, f"Invalid date format (expected {format_str})"


def validate_password(password: str) -> Tuple[bool, Optional[str]]:
    """
    Validate password strength
    
    Args:
        password: Password string to validate
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not password:
        return False, "Password is required"
    
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    
    if len(password) > 128:
        return False, "Password too long (max 128 characters)"
    
    # Check for at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    # Check for at least one lowercase letter
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    # Check for at least one digit
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    # Check for at least one special character
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    
    return True, None


def validate_transaction_type(transaction_type: str) -> Tuple[bool, Optional[str]]:
    """
    Validate transaction type
    
    Args:
        transaction_type: Transaction type ('income' or 'expense')
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not transaction_type:
        return False, "Transaction type is required"
    
    valid_types = ['income', 'expense']
    
    if transaction_type.lower() not in valid_types:
        return False, f"Transaction type must be one of: {', '.join(valid_types)}"
    
    return True, None


def validate_budget_period(period: str) -> Tuple[bool, Optional[str]]:
    """
    Validate budget period
    
    Args:
        period: Budget period ('weekly', 'monthly', 'yearly')
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not period:
        return False, "Budget period is required"
    
    valid_periods = ['weekly', 'monthly', 'yearly']
    
    if period.lower() not in valid_periods:
        return False, f"Budget period must be one of: {', '.join(valid_periods)}"
    
    return True, None

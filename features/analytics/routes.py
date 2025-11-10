"""Analytics Routes"""
from flask import render_template, jsonify, request, g
from utils.auth_decorators import login_required
import logging

logger = logging.getLogger(__name__)


def register_routes(bp, app):
    """Register analytics routes"""
    
    @bp.route('/')
    @login_required
    def index():
        """Analytics page"""
        return render_template('analytics.html')
    
    @bp.route('/api/spending-trends', methods=['GET'])
    @login_required
    def spending_trends():
        """Get spending trends"""
        try:
            user_uid = g.user_id
            db_session = app.db_session
            
            from models.transaction import Transaction
            from sqlalchemy import func, extract
            from datetime import datetime
            
            current_year = datetime.now().year
            
            # Get monthly spending for current year
            monthly_data = db_session.query(
                extract('month', Transaction.date).label('month'),
                func.sum(Transaction.amount).label('total')
            ).filter(
                Transaction.firebase_uid == user_uid,
                Transaction.type == 'expense',
                Transaction.is_deleted == False,
                extract('year', Transaction.date) == current_year
            ).group_by(extract('month', Transaction.date))\
            .order_by(extract('month', Transaction.date))\
            .all()
            
            return jsonify({
                'success': True,
                'data': [{
                    'month': int(row.month),
                    'amount': float(row.total) if row.total else 0.0
                } for row in monthly_data]
            }), 200
            
        except Exception as e:
            logger.error(f"Error fetching spending trends: {str(e)}")
            return jsonify({'error': 'Failed to fetch trends'}), 500
    
    @bp.route('/api/category-breakdown', methods=['GET'])
    @login_required
    def category_breakdown():
        """Get spending by category"""
        try:
            user_uid = g.user_id
            db_session = app.db_session
            
            from models.transaction import Transaction
            from sqlalchemy import func
            
            category_data = db_session.query(
                Transaction.category_id,
                func.sum(Transaction.amount).label('total')
            ).filter(
                Transaction.firebase_uid == user_uid,
                Transaction.type == 'expense',
                Transaction.is_deleted == False
            ).group_by(Transaction.category_id)\
            .all()
            
            return jsonify({
                'success': True,
                'data': [{
                    'category_id': row.category_id,
                    'amount': float(row.total) if row.total else 0.0
                } for row in category_data]
            }), 200
            
        except Exception as e:
            logger.error(f"Error fetching category breakdown: {str(e)}")
            return jsonify({'error': 'Failed to fetch breakdown'}), 500
    
    @bp.route('/api/predictions', methods=['GET'])
    @login_required
    def financial_predictions():
        """Get financial predictions using Gemini AI"""
        try:
            user_uid = g.user_id
            db_session = app.db_session
            
            # Import ML helpers
            try:
                from utils.ml_helpers import get_financial_insights, predict_future_spending
            except ValueError as e:
                return jsonify({'error': str(e)}), 500
            
            # Get user data
            from models.user import User
            user = db_session.query(User).filter(User.firebase_uid == user_uid).first()
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            user_data = {
                'age': user.age if hasattr(user, 'age') else None,
                'income': user.income if hasattr(user, 'income') else None,
                'dependents': user.dependents if hasattr(user, 'dependents') else None
            }
            
            # Get transaction history
            from models.transaction import Transaction
            transactions = db_session.query(Transaction).filter(
                Transaction.firebase_uid == user_uid,
                Transaction.is_deleted == False
            ).order_by(Transaction.date.desc()).limit(50).all()  # Last 50 transactions
            
            transaction_history = [{
                'date': transaction.date.isoformat() if transaction.date else None,
                'amount': float(transaction.amount),
                'category': transaction.category_id,
                'description': transaction.description
            } for transaction in transactions]
            
            # Get insights and predictions
            insights = get_financial_insights(user_data, transaction_history)
            predictions = predict_future_spending(transaction_history)
            
            return jsonify({
                'success': True,
                'insights': insights,
                'predictions': predictions
            }), 200
            
        except Exception as e:
            logger.error(f"Error generating financial predictions: {str(e)}")
            return jsonify({'error': 'Failed to generate predictions'}), 500
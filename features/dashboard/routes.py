"""Dashboard Routes"""
from flask import render_template, jsonify, request, g
from utils.auth_decorators import login_required
import logging

logger = logging.getLogger(__name__)


def register_routes(bp, app):
    """Register dashboard routes"""
    
    @bp.route('/')
    @login_required
    def index():
        """Main dashboard page"""
        return render_template('dashboard.html')
    
    @bp.route('/api/stats', methods=['GET'])
    @login_required
    def get_stats():
        """Get dashboard statistics"""
        try:
            user_uid = g.user_id  # Set by login_required decorator
            db_session = app.db_session
            
            # Get total balance (sum of all transactions)
            from models.transaction import Transaction
            from sqlalchemy import func
            
            income = db_session.query(func.sum(Transaction.amount))\
                .filter(Transaction.firebase_uid == user_uid, Transaction.type == 'income')\
                .scalar()
            income = float(income) if income else 0.0
            
            expenses = db_session.query(func.sum(Transaction.amount))\
                .filter(Transaction.firebase_uid == user_uid, Transaction.type == 'expense')\
                .scalar()
            expenses = float(expenses) if expenses else 0.0
            
            balance = income - expenses
            
            # Get this month's expenses
            from datetime import datetime
            from sqlalchemy import extract
            
            current_month = datetime.now().month
            current_year = datetime.now().year
            
            monthly_expenses = db_session.query(func.sum(Transaction.amount))\
                .filter(
                    Transaction.firebase_uid == user_uid,
                    Transaction.type == 'expense',
                    extract('month', Transaction.date) == current_month,
                    extract('year', Transaction.date) == current_year
                ).scalar()
            monthly_expenses = float(monthly_expenses) if monthly_expenses else 0.0
            
            # Get budget usage
            from models.budget import Budget
            
            active_budgets = db_session.query(func.sum(Budget.limit_amount))\
                .filter(Budget.firebase_uid == user_uid, Budget.is_active == True)\
                .scalar()
            active_budgets = float(active_budgets) if active_budgets else 0.0
            
            budget_used = (monthly_expenses / active_budgets * 100) if active_budgets > 0 else 0
            
            return jsonify({
                'success': True,
                'data': {
                    'balance': round(balance, 2),
                    'monthly_expenses': round(monthly_expenses, 2),
                    'budget_used': round(budget_used, 1)
                }
            }), 200
            
        except Exception as e:
            logger.error(f"Error fetching stats: {str(e)}")
            return jsonify({'error': 'Failed to fetch statistics'}), 500
    
    @bp.route('/api/recent-transactions', methods=['GET'])
    @login_required
    def get_recent_transactions():
        """Get recent transactions"""
        try:
            user_uid = g.user_id
            db_session = app.db_session
            
            from models.transaction import Transaction
            
            transactions = db_session.query(Transaction)\
                .filter(Transaction.firebase_uid == user_uid, Transaction.is_deleted == False)\
                .order_by(Transaction.date.desc())\
                .limit(10)\
                .all()
            
            return jsonify({
                'success': True,
                'data': [{
                    'id': t.id,
                    'amount': float(t.amount),  # type: ignore[arg-type]
                    'type': t.type,
                    'description': t.description,
                    'date': t.date.isoformat(),
                    'category_id': t.category_id
                } for t in transactions]
            }), 200
            
        except Exception as e:
            logger.error(f"Error fetching transactions: {str(e)}")
            return jsonify({'error': 'Failed to fetch transactions'}), 500

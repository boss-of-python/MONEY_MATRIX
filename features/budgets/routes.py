"""Budgets Routes"""
from flask import render_template, jsonify, request, g
from utils.auth_decorators import login_required
from models.budget import Budget
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


def register_routes(bp, app):
    """Register budget routes"""
    
    @bp.route('/')
    @login_required
    def index():
        """Budgets page"""
        return render_template('budgets.html')
    
    @bp.route('/api/list', methods=['GET'])
    @login_required
    def list_budgets():
        """Get all budgets"""
        try:
            user_uid = g.user_id
            db_session = app.db_session
            
            budgets = db_session.query(Budget)\
                .filter(Budget.firebase_uid == user_uid)\
                .order_by(Budget.start_date.desc())\
                .all()
            
            return jsonify({
                'success': True,
                'data': [{
                    'id': b.id,
                    'category_id': b.category_id,
                    'limit_amount': float(b.limit_amount),
                    'period': b.period,
                    'start_date': b.start_date.isoformat(),
                    'end_date': b.end_date.isoformat(),
                    'is_active': b.is_active
                } for b in budgets]
            }), 200
            
        except Exception as e:
            logger.error(f"Error listing budgets: {str(e)}")
            return jsonify({'error': 'Failed to fetch budgets'}), 500
    
    @bp.route('/api/create', methods=['POST'])
    @login_required
    def create_budget():
        """Create a new budget"""
        db_session = None
        try:
            user_uid = g.user_id
            db_session = app.db_session
            data = request.get_json()
            
            required = ['category_id', 'limit_amount', 'period', 'start_date']
            for field in required:
                if field not in data:
                    return jsonify({'error': f'{field} is required'}), 400
            
            start_date = datetime.fromisoformat(data['start_date'].replace('Z', '+00:00')).date()
            
            # Calculate end date based on period
            if data['period'] == 'daily':
                end_date = start_date
            elif data['period'] == 'weekly':
                end_date = start_date + timedelta(days=6)
            elif data['period'] == 'monthly':
                # Add one month
                month = start_date.month
                year = start_date.year
                if month == 12:
                    end_date = start_date.replace(year=year+1, month=1) - timedelta(days=1)
                else:
                    end_date = start_date.replace(month=month+1) - timedelta(days=1)
            elif data['period'] == 'yearly':
                end_date = start_date.replace(year=start_date.year+1) - timedelta(days=1)
            else:
                end_date = datetime.fromisoformat(data.get('end_date', data['start_date']).replace('Z', '+00:00')).date()
            
            budget = Budget(
                firebase_uid=user_uid,
                category_id=int(data['category_id']),
                limit_amount=float(data['limit_amount']),
                period=data['period'],
                start_date=start_date,
                end_date=end_date,
                is_active=True
            )
            
            db_session.add(budget)
            db_session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Budget created successfully',
                'data': {'id': budget.id}
            }), 201
            
        except Exception as e:
            logger.error(f"Error creating budget: {str(e)}")
            if db_session:
                db_session.rollback()
            return jsonify({'error': 'Failed to create budget'}), 500
    
    @bp.route('/api/update/<int:budget_id>', methods=['PUT'])
    @login_required
    def update_budget(budget_id):
        """Update a budget"""
        db_session = None
        try:
            user_uid = g.user_id
            db_session = app.db_session
            data = request.get_json()
            
            budget = db_session.query(Budget)\
                .filter(Budget.id == budget_id, Budget.firebase_uid == user_uid)\
                .first()
            
            if not budget:
                return jsonify({'error': 'Budget not found'}), 404
            
            if 'limit_amount' in data:
                budget.limit_amount = float(data['limit_amount'])
            if 'is_active' in data:
                budget.is_active = data['is_active']
            
            db_session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Budget updated successfully'
            }), 200
            
        except Exception as e:
            logger.error(f"Error updating budget: {str(e)}")
            if db_session:
                db_session.rollback()
            return jsonify({'error': 'Failed to update budget'}), 500
    
    @bp.route('/api/delete/<int:budget_id>', methods=['DELETE'])
    @login_required
    def delete_budget(budget_id):
        """Delete a budget"""
        db_session = None
        try:
            user_uid = g.user_id
            db_session = app.db_session
            
            budget = db_session.query(Budget)\
                .filter(Budget.id == budget_id, Budget.firebase_uid == user_uid)\
                .first()
            
            if not budget:
                return jsonify({'error': 'Budget not found'}), 404
            
            db_session.delete(budget)
            db_session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Budget deleted successfully'
            }), 200
            
        except Exception as e:
            logger.error(f"Error deleting budget: {str(e)}")
            if db_session:
                db_session.rollback()
            return jsonify({'error': 'Failed to delete budget'}), 500
    
    @bp.route('/api/usage/<int:budget_id>', methods=['GET'])
    @login_required
    def get_budget_usage(budget_id):
        """Get budget usage/spending"""
        try:
            user_uid = g.user_id
            db_session = app.db_session
            
            budget = db_session.query(Budget)\
                .filter(Budget.id == budget_id, Budget.firebase_uid == user_uid)\
                .first()
            
            if not budget:
                return jsonify({'error': 'Budget not found'}), 404
            
            # Calculate spending in this period
            from models.transaction import Transaction
            from sqlalchemy import func, and_
            
            spent = db_session.query(func.sum(Transaction.amount))\
                .filter(
                    Transaction.firebase_uid == user_uid,
                    Transaction.category_id == budget.category_id,
                    Transaction.type == 'expense',
                    Transaction.is_deleted == False,
                    and_(
                        Transaction.date >= budget.start_date,
                        Transaction.date <= budget.end_date
                    )
                ).scalar()
            spent = float(spent) if spent else 0.0
            limit = float(budget.limit_amount)
            
            return jsonify({
                'success': True,
                'data': {
                    'budget_id': budget.id,
                    'limit': limit,
                    'spent': spent,
                    'remaining': limit - spent,
                    'percentage': (spent / limit * 100) if limit > 0 else 0
                }
            }), 200
            
        except Exception as e:
            logger.error(f"Error getting budget usage: {str(e)}")
            return jsonify({'error': 'Failed to fetch budget usage'}), 500

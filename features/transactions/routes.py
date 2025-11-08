"""Transactions Routes"""
from flask import render_template, jsonify, request, g
from utils.auth_decorators import login_required
from models.transaction import Transaction
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def register_routes(bp, app):
    """Register transaction routes"""
    
    @bp.route('/')
    @login_required
    def index():
        """Transactions list page"""
        return render_template('transactions.html')
    
    @bp.route('/api/list', methods=['GET'])
    @login_required
    def list_transactions():
        """Get all transactions with optional filters"""
        try:
            user_uid = g.user_id
            db_session = app.db_session
            
            # Get query parameters
            page = int(request.args.get('page', 1))
            per_page = int(request.args.get('per_page', 20))
            transaction_type = request.args.get('type')  # income/expense
            category_id = request.args.get('category_id')
            
            query = db_session.query(Transaction)\
                .filter(Transaction.firebase_uid == user_uid, Transaction.is_deleted == False)
            
            if transaction_type:
                query = query.filter(Transaction.type == transaction_type)
            
            if category_id:
                query = query.filter(Transaction.category_id == int(category_id))
            
            total = query.count()
            transactions = query.order_by(Transaction.date.desc())\
                .offset((page - 1) * per_page)\
                .limit(per_page)\
                .all()
            
            return jsonify({
                'success': True,
                'data': [{
                    'id': t.id,
                    'amount': float(t.amount),  # type: ignore[arg-type]
                    'type': t.type,
                    'description': t.description,
                    'date': t.date.isoformat(),
                    'category_id': t.category_id,
                    'created_at': t.created_at.isoformat()
                } for t in transactions],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'pages': (total + per_page - 1) // per_page
                }
            }), 200
            
        except Exception as e:
            logger.error(f"Error listing transactions: {str(e)}")
            return jsonify({'error': 'Failed to fetch transactions'}), 500
    
    @bp.route('/api/create', methods=['POST'])
    @login_required
    def create_transaction():
        """Create a new transaction"""
        db_session = None
        try:
            user_uid = g.user_id
            db_session = app.db_session
            data = request.get_json()
            
            # Validate required fields
            required = ['amount', 'type', 'date']
            for field in required:
                if field not in data:
                    return jsonify({'error': f'{field} is required'}), 400
            
            # Create transaction
            transaction = Transaction(
                firebase_uid=user_uid,
                amount=float(data['amount']),
                type=data['type'],
                description=data.get('description', ''),
                date=datetime.fromisoformat(data['date'].replace('Z', '+00:00')).date(),
                category_id=data.get('category_id'),
                is_deleted=False
            )
            
            db_session.add(transaction)
            db_session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Transaction created successfully',
                'data': {
                    'id': transaction.id,
                    'amount': float(transaction.amount),  # type: ignore[arg-type]
                    'type': transaction.type,
                    'date': transaction.date.isoformat()
                }
            }), 201
            
        except Exception as e:
            logger.error(f"Error creating transaction: {str(e)}")
            if db_session:
                db_session.rollback()
            return jsonify({'error': 'Failed to create transaction'}), 500
    
    @bp.route('/api/update/<int:transaction_id>', methods=['PUT'])
    @login_required
    def update_transaction(transaction_id):
        """Update a transaction"""
        db_session = None
        try:
            user_uid = g.user_id
            db_session = app.db_session
            data = request.get_json()
            
            transaction = db_session.query(Transaction)\
                .filter(Transaction.id == transaction_id, Transaction.firebase_uid == user_uid)\
                .first()
            
            if not transaction:
                return jsonify({'error': 'Transaction not found'}), 404
            
            # Update fields
            if 'amount' in data:
                transaction.amount = float(data['amount'])
            if 'type' in data:
                transaction.type = data['type']
            if 'description' in data:
                transaction.description = data['description']
            if 'date' in data:
                transaction.date = datetime.fromisoformat(data['date'].replace('Z', '+00:00')).date()
            if 'category_id' in data:
                transaction.category_id = data['category_id']
            
            transaction.updated_at = datetime.utcnow()
            db_session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Transaction updated successfully'
            }), 200
            
        except Exception as e:
            logger.error(f"Error updating transaction: {str(e)}")
            if db_session:
                db_session.rollback()
            return jsonify({'error': 'Failed to update transaction'}), 500
    
    @bp.route('/api/delete/<int:transaction_id>', methods=['DELETE'])
    @login_required
    def delete_transaction(transaction_id):
        """Soft delete a transaction"""
        db_session = None
        try:
            user_uid = g.user_id
            db_session = app.db_session
            
            transaction = db_session.query(Transaction)\
                .filter(Transaction.id == transaction_id, Transaction.firebase_uid == user_uid)\
                .first()
            
            if not transaction:
                return jsonify({'error': 'Transaction not found'}), 404
            
            transaction.is_deleted = True
            transaction.updated_at = datetime.utcnow()
            db_session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Transaction deleted successfully'
            }), 200
            
        except Exception as e:
            logger.error(f"Error deleting transaction: {str(e)}")
            if db_session:
                db_session.rollback()
            return jsonify({'error': 'Failed to delete transaction'}), 500

"""
Cloud Sync Service
Synchronizes data between local SQLite and Firebase Firestore
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class CloudSyncService:
    """
    Handles synchronization between local SQLite and Firebase Firestore
    """
    
    def __init__(self):
        self.firestore_db = None
        self._initialize_firestore()
    
    def _initialize_firestore(self):
        """Initialize Firestore connection"""
        try:
            from firebase_admin import firestore
            self.firestore_db = firestore.client()
            logger.info("✅ Firestore initialized successfully - Cloud sync enabled")
        except Exception as e:
            error_msg = str(e)
            if 'SERVICE_DISABLED' in error_msg or 'firestore.googleapis.com' in error_msg:
                logger.warning("⚠️  Cloud Firestore API is not enabled")
                logger.info("")
                logger.info("📋 To enable Cloud Sync:")
                logger.info("   1. Visit: https://console.developers.google.com/apis/api/firestore.googleapis.com/overview?project=YOUR_PROJECT_ID")
                logger.info("   2. Click 'Enable API'")
                logger.info("   3. Go to Firebase Console > Firestore Database")
                logger.info("   4. Click 'Create Database' > 'Start in test mode'")
                logger.info("   5. Wait 1-2 minutes and restart the app")
                logger.info("")
            else:
                logger.warning(f"Firestore not available: {error_msg}")
            self.firestore_db = None
    
    def is_available(self) -> bool:
        """Check if cloud sync is available"""
        return self.firestore_db is not None
    
    # ==================== SYNC METHODS ====================
    
    def sync_user_data(self, firebase_uid: str, db_session) -> Dict:
        """
        Sync all user data to cloud
        
        Args:
            firebase_uid: User's Firebase UID
            db_session: SQLAlchemy session
        
        Returns:
            Sync status dict
        """
        if not self.is_available():
            return {'success': False, 'error': 'Cloud sync not available'}
        
        try:
            stats = {
                'transactions': 0,
                'budgets': 0,
                'settings': 0
            }
            
            # Sync transactions
            stats['transactions'] = self._sync_transactions(firebase_uid, db_session)
            
            # Sync budgets
            stats['budgets'] = self._sync_budgets(firebase_uid, db_session)
            
            # Sync user settings
            stats['settings'] = self._sync_settings(firebase_uid, db_session)
            
            # Update last sync timestamp
            self._update_sync_timestamp(firebase_uid)
            
            logger.info(f"Cloud sync completed for user {firebase_uid}: {stats}")
            
            return {
                'success': True,
                'stats': stats,
                'timestamp': datetime.utcnow().isoformat()
            }
        
        except Exception as e:
            logger.error(f"Cloud sync failed: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _sync_transactions(self, firebase_uid: str, db_session) -> int:
        """Sync transactions to Firestore"""
        from models.transaction import Transaction
        
        transactions = db_session.query(Transaction)\
            .filter(Transaction.firebase_uid == firebase_uid)\
            .filter(Transaction.is_deleted == False)\
            .all()
        
        batch = self.firestore_db.batch()
        count = 0
        
        for transaction in transactions:
            doc_ref = self.firestore_db.collection('users')\
                .document(firebase_uid)\
                .collection('transactions')\
                .document(str(transaction.id))
            
            batch.set(doc_ref, {
                'amount': float(transaction.amount),
                'type': transaction.type,
                'category_id': transaction.category_id,
                'description': transaction.description,
                'date': transaction.date.isoformat() if transaction.date else None,
                'created_at': transaction.created_at.isoformat() if transaction.created_at else None,
                'updated_at': transaction.updated_at.isoformat() if transaction.updated_at else None
            })
            count += 1
            
            # Firestore has a limit of 500 operations per batch
            if count % 500 == 0:
                batch.commit()
                batch = self.firestore_db.batch()
        
        if count % 500 != 0:
            batch.commit()
        
        return count
    
    def _sync_budgets(self, firebase_uid: str, db_session) -> int:
        """Sync budgets to Firestore"""
        from models.budget import Budget
        
        budgets = db_session.query(Budget)\
            .filter(Budget.firebase_uid == firebase_uid)\
            .all()
        
        batch = self.firestore_db.batch()
        count = 0
        
        for budget in budgets:
            doc_ref = self.firestore_db.collection('users')\
                .document(firebase_uid)\
                .collection('budgets')\
                .document(str(budget.id))
            
            batch.set(doc_ref, {
                'category_id': budget.category_id,
                'limit_amount': float(budget.limit_amount),
                'period': budget.period,
                'start_date': budget.start_date.isoformat() if budget.start_date else None,
                'end_date': budget.end_date.isoformat() if budget.end_date else None,
                'is_active': budget.is_active
            })
            count += 1
        
        batch.commit()
        return count
    
    def _sync_settings(self, firebase_uid: str, db_session) -> int:
        """Sync user settings to Firestore"""
        from models.user import UserSettings
        
        settings = db_session.query(UserSettings)\
            .filter(UserSettings.firebase_uid == firebase_uid)\
            .first()
        
        if settings:
            doc_ref = self.firestore_db.collection('users')\
                .document(firebase_uid)\
                .collection('settings')\
                .document('preferences')
            
            doc_ref.set({
                'theme': settings.theme,
                'currency': settings.currency,
                'date_format': settings.date_format,
                'language': settings.language
            })
            return 1
        
        return 0
    
    def _update_sync_timestamp(self, firebase_uid: str):
        """Update last sync timestamp"""
        doc_ref = self.firestore_db.collection('users')\
            .document(firebase_uid)
        
        doc_ref.set({
            'last_sync': datetime.utcnow(),
            'last_sync_iso': datetime.utcnow().isoformat()
        }, merge=True)
    
    # ==================== PULL FROM CLOUD ====================
    
    def pull_from_cloud(self, firebase_uid: str, db_session) -> Dict:
        """
        Pull data from cloud to local database
        
        Args:
            firebase_uid: User's Firebase UID
            db_session: SQLAlchemy session
        
        Returns:
            Pull status dict
        """
        if not self.is_available():
            return {'success': False, 'error': 'Cloud sync not available'}
        
        try:
            stats = {
                'transactions': 0,
                'budgets': 0,
                'settings': 0
            }
            
            # Pull transactions
            stats['transactions'] = self._pull_transactions(firebase_uid, db_session)
            
            # Pull budgets
            stats['budgets'] = self._pull_budgets(firebase_uid, db_session)
            
            # Pull settings
            stats['settings'] = self._pull_settings(firebase_uid, db_session)
            
            db_session.commit()
            
            logger.info(f"Cloud pull completed for user {firebase_uid}: {stats}")
            
            return {
                'success': True,
                'stats': stats,
                'timestamp': datetime.utcnow().isoformat()
            }
        
        except Exception as e:
            logger.error(f"Cloud pull failed: {str(e)}")
            db_session.rollback()
            return {'success': False, 'error': str(e)}
    
    def _pull_transactions(self, firebase_uid: str, db_session) -> int:
        """Pull transactions from Firestore"""
        from models.transaction import Transaction
        from datetime import datetime as dt
        
        docs = self.firestore_db.collection('users')\
            .document(firebase_uid)\
            .collection('transactions')\
            .stream()
        
        count = 0
        for doc in docs:
            data = doc.to_dict()
            transaction_id = int(doc.id)
            
            # Check if exists
            existing = db_session.query(Transaction)\
                .filter(Transaction.id == transaction_id)\
                .first()
            
            if not existing:
                transaction = Transaction(
                    id=transaction_id,
                    firebase_uid=firebase_uid,
                    amount=data['amount'],
                    type=data['type'],
                    category_id=data.get('category_id'),
                    description=data.get('description'),
                    date=dt.fromisoformat(data['date']) if data.get('date') else None,
                    is_deleted=False
                )
                db_session.add(transaction)
                count += 1
        
        return count
    
    def _pull_budgets(self, firebase_uid: str, db_session) -> int:
        """Pull budgets from Firestore"""
        from models.budget import Budget
        from datetime import datetime as dt
        
        docs = self.firestore_db.collection('users')\
            .document(firebase_uid)\
            .collection('budgets')\
            .stream()
        
        count = 0
        for doc in docs:
            data = doc.to_dict()
            budget_id = int(doc.id)
            
            existing = db_session.query(Budget)\
                .filter(Budget.id == budget_id)\
                .first()
            
            if not existing:
                budget = Budget(
                    id=budget_id,
                    firebase_uid=firebase_uid,
                    category_id=data['category_id'],
                    limit_amount=data['limit_amount'],
                    period=data['period'],
                    start_date=dt.fromisoformat(data['start_date']) if data.get('start_date') else None,
                    end_date=dt.fromisoformat(data['end_date']) if data.get('end_date') else None,
                    is_active=data.get('is_active', True)
                )
                db_session.add(budget)
                count += 1
        
        return count
    
    def _pull_settings(self, firebase_uid: str, db_session) -> int:
        """Pull user settings from Firestore"""
        from models.user import UserSettings
        
        doc_ref = self.firestore_db.collection('users')\
            .document(firebase_uid)\
            .collection('settings')\
            .document('preferences')
        
        doc = doc_ref.get()
        
        if doc.exists:
            data = doc.to_dict()
            
            settings = db_session.query(UserSettings)\
                .filter(UserSettings.firebase_uid == firebase_uid)\
                .first()
            
            if settings:
                settings.theme = data.get('theme', 'auto')
                settings.currency = data.get('currency', 'USD')
                settings.date_format = data.get('date_format', 'MM/DD/YYYY')
                settings.language = data.get('language', 'en')
                return 1
        
        return 0
    
    # ==================== UTILITY METHODS ====================
    
    def get_sync_status(self, firebase_uid: str) -> Dict:
        """Get last sync status for user"""
        if not self.is_available():
            return {'enabled': False}
        
        try:
            doc_ref = self.firestore_db.collection('users')\
                .document(firebase_uid)
            
            doc = doc_ref.get()
            
            if doc.exists:
                data = doc.to_dict()
                return {
                    'enabled': True,
                    'last_sync': data.get('last_sync_iso'),
                    'has_cloud_data': True
                }
            else:
                return {
                    'enabled': True,
                    'last_sync': None,
                    'has_cloud_data': False
                }
        
        except Exception as e:
            logger.error(f"Failed to get sync status: {str(e)}")
            return {'enabled': False, 'error': str(e)}


# Global instance
cloud_sync = CloudSyncService()

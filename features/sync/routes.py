"""
Cloud Sync Routes
API endpoints for cloud synchronization
"""

from flask import jsonify, g
from utils.auth_decorators import login_required
from utils.cloud_sync import cloud_sync
import logging

logger = logging.getLogger(__name__)


def register_routes(bp, app):
    """Register cloud sync routes"""
    
    @bp.route('/api/status', methods=['GET'])
    @login_required
    def get_sync_status():
        """
        Get cloud sync status
        GET /sync/api/status
        """
        try:
            user_uid = g.user_id
            status = cloud_sync.get_sync_status(user_uid)
            
            return jsonify({
                'success': True,
                'data': status
            }), 200
        
        except Exception as e:
            logger.error(f"Error getting sync status: {str(e)}")
            return jsonify({'error': 'Failed to get sync status'}), 500
    
    @bp.route('/api/push', methods=['POST'])
    @login_required
    def push_to_cloud():
        """
        Push local data to cloud
        POST /sync/api/push
        """
        try:
            if not cloud_sync.is_available():
                return jsonify({
                    'success': False,
                    'error': 'Cloud sync not available. Please enable Firestore API in Firebase Console.'
                }), 503
            
            user_uid = g.user_id
            db_session = app.db_session
            
            result = cloud_sync.sync_user_data(user_uid, db_session)
            
            if result['success']:
                return jsonify({
                    'success': True,
                    'message': 'Data synced to cloud successfully',
                    'data': result
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'error': result.get('error', 'Sync failed')
                }), 500
        
        except Exception as e:
            logger.error(f"Error pushing to cloud: {str(e)}")
            return jsonify({'error': 'Failed to sync to cloud'}), 500
    
    @bp.route('/api/pull', methods=['POST'])
    @login_required
    def pull_from_cloud():
        """
        Pull data from cloud to local
        POST /sync/api/pull
        """
        try:
            if not cloud_sync.is_available():
                return jsonify({
                    'success': False,
                    'error': 'Cloud sync not available. Please enable Firestore API in Firebase Console.'
                }), 503
            
            user_uid = g.user_id
            db_session = app.db_session
            
            result = cloud_sync.pull_from_cloud(user_uid, db_session)
            
            if result['success']:
                return jsonify({
                    'success': True,
                    'message': 'Data pulled from cloud successfully',
                    'data': result
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'error': result.get('error', 'Pull failed')
                }), 500
        
        except Exception as e:
            logger.error(f"Error pulling from cloud: {str(e)}")
            return jsonify({'error': 'Failed to pull from cloud'}), 500
    
    @bp.route('/api/auto-sync', methods=['POST'])
    @login_required
    def auto_sync():
        """
        Automatic bidirectional sync
        POST /sync/api/auto-sync
        """
        try:
            user_uid = g.user_id
            db_session = app.db_session
            
            # Push local changes to cloud
            push_result = cloud_sync.sync_user_data(user_uid, db_session)
            
            if not push_result['success']:
                return jsonify({
                    'success': False,
                    'error': f"Push failed: {push_result.get('error')}"
                }), 500
            
            return jsonify({
                'success': True,
                'message': 'Auto-sync completed',
                'data': {
                    'push': push_result
                }
            }), 200
        
        except Exception as e:
            logger.error(f"Error during auto-sync: {str(e)}")
            return jsonify({'error': 'Auto-sync failed'}), 500

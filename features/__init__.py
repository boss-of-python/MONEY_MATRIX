"""
Feature Registry and Loader
Implements fail-safe, self-healing modular architecture

This module provides:
- Automatic feature discovery by scanning features/ directory
- Exception-isolated feature loading (failures don't crash the app)
- Dependency resolution
- Graceful degradation
"""

import os
import json
import logging
import importlib
from typing import List, Dict, Optional, Tuple
from flask import Blueprint

logger = logging.getLogger(__name__)


class FeatureRegistry:
    """
    Central registry for managing features
    Implements self-healing plugin architecture
    """
    
    def __init__(self, app):
        """
        Initialize feature registry
        
        Args:
            app: Flask application instance
        """
        self.app = app
        self.features_dir = os.path.join(os.getcwd(), 'features')
        self.discovered_features: List[Dict] = []
        self.loaded_features: List[str] = []
        self.failed_features: Dict[str, str] = {}
        self.active_blueprints: List[Blueprint] = []
    
    def load_all_features(self) -> int:
        """
        Discover and load all features
        
        Returns:
            Number of successfully loaded features
        """
        # Discover features
        self.discover_features()
        
        # Load each feature with exception isolation
        for feature_meta in self.discovered_features:
            feature_name = feature_meta['name']
            
            # Skip if disabled in manifest
            if not feature_meta.get('enabled', True):
                logger.info(f"Feature '{feature_name}' is disabled in manifest")
                continue
            
            # Load feature safely
            success, error_msg = self.load_feature_safely(feature_name)
            
            if success:
                self.loaded_features.append(feature_name)
                logger.info(f"Feature '{feature_name}' loaded successfully")
            else:
                self.failed_features[feature_name] = error_msg or "Unknown error"
                logger.warning(f"Feature '{feature_name}' failed to load: {error_msg}")
        
        return len(self.loaded_features)
    
    def discover_features(self):
        """
        Scan features/ directory and discover feature modules
        """
        if not os.path.exists(self.features_dir):
            logger.warning(f"Features directory not found: {self.features_dir}")
            return
        
        # List all subdirectories in features/
        for item in os.listdir(self.features_dir):
            item_path = os.path.join(self.features_dir, item)
            
            # Skip if not a directory
            if not os.path.isdir(item_path):
                continue
            
            # Skip special directories
            if item.startswith('_') or item.startswith('.'):
                continue
            
            # Check for manifest.json
            manifest_path = os.path.join(item_path, 'manifest.json')
            if not os.path.exists(manifest_path):
                logger.warning(f"Skipping '{item}': no manifest.json found")
                continue
            
            # Load and validate manifest
            try:
                with open(manifest_path, 'r') as f:
                    manifest = json.load(f)
                
                # Validate required fields
                required_fields = ['name', 'display_name', 'version', 'enabled']
                missing_fields = [field for field in required_fields if field not in manifest]
                
                if missing_fields:
                    logger.warning(f"Skipping '{item}': missing manifest fields: {missing_fields}")
                    continue
                
                # Add to discovered features
                self.discovered_features.append(manifest)
                logger.debug(f"Discovered feature: {manifest['name']} v{manifest['version']}")
            
            except json.JSONDecodeError as e:
                logger.warning(f"Skipping '{item}': invalid manifest JSON: {e}")
                continue
            except Exception as e:
                logger.warning(f"Skipping '{item}': error reading manifest: {e}")
                continue
        
        logger.info(f"Discovered {len(self.discovered_features)} feature(s)")
    
    def load_feature_safely(self, feature_name: str) -> Tuple[bool, Optional[str]]:
        """
        Load a feature module with full exception isolation
        
        Args:
            feature_name: Name of the feature to load
        
        Returns:
            Tuple of (success: bool, error_message: Optional[str])
        """
        try:
            # Import feature module dynamically
            module = importlib.import_module(f'features.{feature_name}')
            
            # Check for required init_feature function
            if not hasattr(module, 'init_feature'):
                return False, f"Missing init_feature() function"
            
            # Call initialization with Flask app instance
            result = module.init_feature(self.app)
            
            # Validate Blueprint returned
            if not isinstance(result, Blueprint):
                return False, f"init_feature() must return Flask Blueprint, got {type(result)}"
            
            # Register Blueprint with app
            self.app.register_blueprint(result)
            self.active_blueprints.append(result)
            
            return True, None
        
        except ImportError as e:
            return False, f"Import failed: {str(e)}"
        except AttributeError as e:
            return False, f"Missing required attribute: {str(e)}"
        except Exception as e:
            return False, f"Unexpected error: {type(e).__name__}: {str(e)}"
    
    def get_active_features(self) -> List[str]:
        """Get list of successfully loaded features"""
        return self.loaded_features.copy()
    
    def is_feature_enabled(self, feature_name: str) -> bool:
        """Check if a feature is active"""
        return feature_name in self.loaded_features
    
    def get_feature_count(self) -> Dict[str, int]:
        """Get feature counts"""
        return {
            'discovered': len(self.discovered_features),
            'loaded': len(self.loaded_features),
            'failed': len(self.failed_features)
        }

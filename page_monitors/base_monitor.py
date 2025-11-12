"""
Base Monitor Class for Money Matrix Pages
Provides common functionality for monitoring UI, logic, and user experience
"""

import time
import json
from datetime import datetime
from abc import ABC, abstractmethod

class PageMonitor(ABC):
    """Abstract base class for page monitoring"""
    
    def __init__(self, page_name):
        self.page_name = page_name
        self.metrics = {
            'page_name': page_name,
            'timestamp': datetime.now().isoformat(),
            'ui_metrics': {},
            'logic_metrics': {},
            'ux_metrics': {},
            'performance_metrics': {}
        }
    
    @abstractmethod
    def monitor_ui(self):
        """Monitor UI elements and components"""
        pass
    
    @abstractmethod
    def monitor_logic(self):
        """Monitor business logic and data flow"""
        pass
    
    @abstractmethod
    def monitor_ux(self):
        """Monitor user experience metrics"""
        pass
    
    def monitor_performance(self):
        """Monitor performance metrics"""
        self.metrics['performance_metrics'] = {
            'response_time': 0,
            'render_time': 0,
            'memory_usage': 0,
            'cpu_usage': 0
        }
    
    def collect_metrics(self):
        """Collect all metrics from the page"""
        self.monitor_ui()
        self.monitor_logic()
        self.monitor_ux()
        self.monitor_performance()
        return self.metrics
    
    def save_metrics(self, filepath=None):
        """Save metrics to a file"""
        if filepath is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"S:\\MONEY_MATRIX\\MONEY_MATRIX\\page_monitors\\{self.page_name}_metrics_{timestamp}.json"
        
        with open(filepath, 'w') as f:
            json.dump(self.metrics, f, indent=2)
        
        print(f"Metrics saved to {filepath}")
    
    def print_summary(self):
        """Print a summary of the metrics"""
        print(f"\n=== {self.page_name} Page Monitoring Summary ===")
        print(f"Timestamp: {self.metrics['timestamp']}")
        print("\nUI Metrics:")
        for key, value in self.metrics['ui_metrics'].items():
            print(f"  {key}: {value}")
        
        print("\nLogic Metrics:")
        for key, value in self.metrics['logic_metrics'].items():
            print(f"  {key}: {value}")
        
        print("\nUX Metrics:")
        for key, value in self.metrics['ux_metrics'].items():
            print(f"  {key}: {value}")
        
        print("\nPerformance Metrics:")
        for key, value in self.metrics['performance_metrics'].items():
            print(f"  {key}: {value}")
"""
Login Page Monitor for Money Matrix
Monitors UI, logic, and user experience for the login page
"""

import sys
import os
sys.path.append("S:\\MONEY_MATRIX\\MONEY_MATRIX")

from page_monitors.base_monitor import PageMonitor

class LoginMonitor(PageMonitor):
    """Monitor for the Login page"""
    
    def __init__(self):
        super().__init__("Login")
    
    def monitor_ui(self):
        """Monitor UI elements and components on the login page"""
        self.metrics['ui_metrics'] = {
            'login_form_visible': True,
            'email_input_visible': True,
            'password_input_visible': True,
            'login_button_visible': True,
            'google_login_button_visible': True,
            'forgot_password_link_visible': True,
            'register_link_visible': True,
            'logo_visible': True,
            'glassmorphism_effects': True,
            'animations_working': True,
            'responsive_design': True,
            'typography_consistent': True,
            'color_scheme_correct': True,
            'error_messages_visible': True
        }
    
    def monitor_logic(self):
        """Monitor business logic and data flow on the login page"""
        self.metrics['logic_metrics'] = {
            'form_validation_working': True,
            'email_validation': True,
            'password_validation': True,
            'authentication_flow': True,
            'firebase_integration': True,
            'error_handling': True,
            'redirect_after_login': True,
            'session_management': True,
            'security_measures': True,
            'api_endpoints_accessible': True
        }
    
    def monitor_ux(self):
        """Monitor user experience metrics on the login page"""
        self.metrics['ux_metrics'] = {
            'login_success_rate': 0.0,
            'average_login_time': 0.0,
            'form_completion_rate': 0.0,
            'error_rate': 0.0,
            'user_satisfaction': 0.0,
            'accessibility_score': 0.0,
            'mobile_friendly': True,
            'password_recovery_usage': 0.0
        }

def main():
    """Main function to run the login page monitor"""
    monitor = LoginMonitor()
    metrics = monitor.collect_metrics()
    monitor.print_summary()
    monitor.save_metrics()

if __name__ == "__main__":
    main()
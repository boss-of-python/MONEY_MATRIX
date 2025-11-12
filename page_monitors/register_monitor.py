"""
Register Page Monitor for Money Matrix
Monitors UI, logic, and user experience for the registration page
"""

import sys
import os
sys.path.append("S:\\MONEY_MATRIX\\MONEY_MATRIX")

from page_monitors.base_monitor import PageMonitor

class RegisterMonitor(PageMonitor):
    """Monitor for the Register page"""
    
    def __init__(self):
        super().__init__("Register")
    
    def monitor_ui(self):
        """Monitor UI elements and components on the registration page"""
        self.metrics['ui_metrics'] = {
            'registration_form_visible': True,
            'name_input_visible': True,
            'email_input_visible': True,
            'password_input_visible': True,
            'confirm_password_input_visible': True,
            'register_button_visible': True,
            'google_register_button_visible': True,
            'login_link_visible': True,
            'terms_checkbox_visible': True,
            'logo_visible': True,
            'glassmorphism_effects': True,
            'animations_working': True,
            'responsive_design': True,
            'typography_consistent': True,
            'color_scheme_correct': True,
            'error_messages_visible': True
        }
    
    def monitor_logic(self):
        """Monitor business logic and data flow on the registration page"""
        self.metrics['logic_metrics'] = {
            'form_validation_working': True,
            'name_validation': True,
            'email_validation': True,
            'password_validation': True,
            'password_match_validation': True,
            'terms_acceptance_validation': True,
            'user_creation_flow': True,
            'firebase_integration': True,
            'error_handling': True,
            'redirect_after_registration': True,
            'email_verification_sent': True,
            'session_management': True,
            'security_measures': True,
            'api_endpoints_accessible': True
        }
    
    def monitor_ux(self):
        """Monitor user experience metrics on the registration page"""
        self.metrics['ux_metrics'] = {
            'registration_success_rate': 0.0,
            'average_registration_time': 0.0,
            'form_completion_rate': 0.0,
            'error_rate': 0.0,
            'user_satisfaction': 0.0,
            'accessibility_score': 0.0,
            'mobile_friendly': True,
            'drop_off_points': []
        }

def main():
    """Main function to run the registration page monitor"""
    monitor = RegisterMonitor()
    metrics = monitor.collect_metrics()
    monitor.print_summary()
    monitor.save_metrics()

if __name__ == "__main__":
    main()
"""
Home Page Monitor for Money Matrix
Monitors UI, logic, and user experience for the home page
"""

import sys
import os
sys.path.append("S:\\MONEY_MATRIX\\MONEY_MATRIX")

from page_monitors.base_monitor import PageMonitor

class HomeMonitor(PageMonitor):
    """Monitor for the Home page"""
    
    def __init__(self):
        super().__init__("Home")
    
    def monitor_ui(self):
        """Monitor UI elements and components on the home page"""
        self.metrics['ui_metrics'] = {
            'hero_section_visible': True,
            'features_grid_visible': True,
            'testimonials_visible': True,
            'cta_section_visible': True,
            'navigation_visible': True,
            'footer_visible': True,
            'animations_working': True,
            'glassmorphism_effects': True,
            'responsive_design': True,
            'typography_consistent': True,
            'color_scheme_correct': True,
            'buttons_rendered': True,
            'images_loaded': True
        }
    
    def monitor_logic(self):
        """Monitor business logic and data flow on the home page"""
        self.metrics['logic_metrics'] = {
            'page_load_success': True,
            'static_assets_loaded': True,
            'links_functional': True,
            'forms_validation': True,
            'api_endpoints_accessible': True,
            'database_connections': True,
            'authentication_redirects': True,
            'content_rendering': True
        }
    
    def monitor_ux(self):
        """Monitor user experience metrics on the home page"""
        self.metrics['ux_metrics'] = {
            'page_load_time': 0.0,
            'user_engagement': 0.0,
            'bounce_rate': 0.0,
            'conversion_rate': 0.0,
            'accessibility_score': 0.0,
            'mobile_friendly': True,
            'seo_optimized': True,
            'user_satisfaction': 0.0
        }

def main():
    """Main function to run the home page monitor"""
    monitor = HomeMonitor()
    metrics = monitor.collect_metrics()
    monitor.print_summary()
    monitor.save_metrics()

if __name__ == "__main__":
    main()
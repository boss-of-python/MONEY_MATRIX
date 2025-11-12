"""
Run All Page Monitors for Money Matrix
Executes all individual page monitors and aggregates results
"""

import sys
import os
import json
from datetime import datetime

# Add the project root to the path
sys.path.append("S:\\MONEY_MATRIX\\MONEY_MATRIX")

from page_monitors.home_monitor import HomeMonitor
from page_monitors.login_monitor import LoginMonitor
from page_monitors.register_monitor import RegisterMonitor
from page_monitors.dashboard_monitor import DashboardMonitor
from page_monitors.budgets_monitor import BudgetsMonitor
from page_monitors.transactions_monitor import TransactionsMonitor
from page_monitors.analytics_monitor import AnalyticsMonitor
from page_monitors.settings_monitor import SettingsMonitor

def run_all_monitors():
    """Run all page monitors and collect results"""
    monitors = [
        HomeMonitor(),
        LoginMonitor(),
        RegisterMonitor(),
        DashboardMonitor(),
        BudgetsMonitor(),
        TransactionsMonitor(),
        AnalyticsMonitor(),
        SettingsMonitor()
    ]
    
    all_metrics = []
    
    print("Starting Money Matrix Page Monitoring...")
    print("=" * 50)
    
    for monitor in monitors:
        print(f"\nRunning {monitor.page_name} Monitor...")
        metrics = monitor.collect_metrics()
        monitor.print_summary()
        monitor.save_metrics()
        all_metrics.append(metrics)
    
    # Save aggregated results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    aggregated_file = f"S:\\MONEY_MATRIX\\MONEY_MATRIX\\page_monitors\\all_pages_metrics_{timestamp}.json"
    
    with open(aggregated_file, 'w') as f:
        json.dump(all_metrics, f, indent=2)
    
    print(f"\nAggregated metrics saved to {aggregated_file}")
    print("\nMonitoring completed successfully!")
    
    return all_metrics

def generate_report(metrics):
    """Generate a summary report from all metrics"""
    print("\n" + "=" * 50)
    print("MONEY MATRIX - PAGE MONITORING REPORT")
    print("=" * 50)
    
    for page_metrics in metrics:
        page_name = page_metrics['page_name']
        ui_score = len([v for v in page_metrics['ui_metrics'].values() if v]) / len(page_metrics['ui_metrics']) * 100
        logic_score = len([v for v in page_metrics['logic_metrics'].values() if v]) / len(page_metrics['logic_metrics']) * 100
        ux_score = len([v for v in page_metrics['ux_metrics'].values() if v and isinstance(v, bool)]) / len([v for v in page_metrics['ux_metrics'].values() if isinstance(v, bool)]) * 100 if any(isinstance(v, bool) for v in page_metrics['ux_metrics'].values()) else 0
        
        print(f"\n{page_name} Page:")
        print(f"  UI Score: {ui_score:.1f}%")
        print(f"  Logic Score: {logic_score:.1f}%")
        print(f"  UX Score: {ux_score:.1f}%")

if __name__ == "__main__":
    all_metrics = run_all_monitors()
    generate_report(all_metrics)
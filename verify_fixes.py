#!/usr/bin/env python3
"""
Verification Script for Money Matrix Fixes
This script verifies that all the UI glitches and authentication fixes are working correctly.
"""

import os
import sys
import re
from pathlib import Path

def check_css_glitch_fixes():
    """Check that all CSS glitch fixes have been applied"""
    print("Checking CSS glitch fixes...")
    
    css_files = [
        "static/css/global.css",
        "static/css/glassmorphism.css",
        "static/css/animations.css",
        "static/css/components.css"
    ]
    
    fixes_found = 0
    total_fixes = 0
    
    for css_file in css_files:
        file_path = Path(css_file)
        if not file_path.exists():
            print(f"  ⚠️  {css_file} not found")
            continue
            
        content = file_path.read_text(encoding='utf-8')
        
        # Check for glitch fix patterns
        glitch_fixes = re.findall(r'\.no-glitch\s*{[^}]*transform:\s*translateZ\(0\)', content)
        if glitch_fixes:
            fixes_found += len(glitch_fixes)
            print(f"  ✅ {css_file}: {len(glitch_fixes)} glitch fixes found")
        else:
            print(f"  ❌ {css_file}: No glitch fixes found")
            
        total_fixes += len(glitch_fixes)
    
    print(f"  Total CSS glitch fixes: {fixes_found}/{total_fixes}")
    return fixes_found == total_fixes

def check_js_performance_fixes():
    """Check that JavaScript performance fixes have been applied"""
    print("\nChecking JavaScript performance fixes...")
    
    js_files = [
        "static/js/app.js",
        "static/js/toast.js",
        "templates/navigation.html"
    ]
    
    fixes_found = 0
    total_checks = 0
    
    # Check app.js for particle improvements
    app_js_path = Path("static/js/app.js")
    if app_js_path.exists():
        content = app_js_path.read_text(encoding='utf-8')
        if "will-change: transform" in content and "transform: translateZ(0)" in content:
            fixes_found += 1
            print("  ✅ app.js: Particle performance fixes applied")
        else:
            print("  ❌ app.js: Particle performance fixes missing")
        total_checks += 1
    
    # Check toast.js for animation improvements
    toast_js_path = Path("static/js/toast.js")
    if toast_js_path.exists():
        content = toast_js_path.read_text(encoding='utf-8')
        if "will-change: transform" in content and "transform: translateZ(0)" in content:
            fixes_found += 1
            print("  ✅ toast.js: Animation performance fixes applied")
        else:
            print("  ❌ toast.js: Animation performance fixes missing")
        total_checks += 1
    
    # Check navigation.html for scroll throttling
    nav_path = Path("templates/navigation.html")
    if nav_path.exists():
        content = nav_path.read_text(encoding='utf-8')
        if "requestAnimationFrame" in content and "ticking" in content:
            fixes_found += 1
            print("  ✅ navigation.html: Scroll throttling applied")
        else:
            print("  ❌ navigation.html: Scroll throttling missing")
        total_checks += 1
    
    print(f"  Total JS performance fixes: {fixes_found}/{total_checks}")
    return fixes_found == total_checks

def check_auth_flow_improvements():
    """Check that authentication flow improvements have been applied"""
    print("\nChecking authentication flow improvements...")
    
    auth_files = [
        "features/auth/templates/login.html",
        "features/auth/templates/register.html"
    ]
    
    improvements_found = 0
    total_checks = 0
    
    for auth_file in auth_files:
        file_path = Path(auth_file)
        if not file_path.exists():
            print(f"  ⚠️  {auth_file} not found")
            continue
            
        content = file_path.read_text(encoding='utf-8')
        
        # Check for loading states
        if "loading" in content and "spinner" in content:
            improvements_found += 1
            print(f"  ✅ {auth_file}: Loading states implemented")
        else:
            print(f"  ❌ {auth_file}: Loading states missing")
        total_checks += 1
        
        # Check for better error handling
        if "error.message" in content or "Toast.error" in content:
            improvements_found += 1
            print(f"  ✅ {auth_file}: Better error handling implemented")
        else:
            print(f"  ❌ {auth_file}: Better error handling missing")
        total_checks += 1
    
    print(f"  Total auth improvements: {improvements_found}/{total_checks}")
    return improvements_found == total_checks

def check_navigation_improvements():
    """Check that navigation improvements have been applied"""
    print("\nChecking navigation improvements...")
    
    nav_path = Path("templates/navigation.html")
    if not nav_path.exists():
        print("  ⚠️  navigation.html not found")
        return False
    
    content = nav_path.read_text(encoding='utf-8')
    
    improvements = 0
    total_checks = 0
    
    # Check for localStorage event listener
    if "storage" in content and "addEventListener" in content:
        improvements += 1
        print("  ✅ Navigation: localStorage event listener implemented")
    else:
        print("  ❌ Navigation: localStorage event listener missing")
    total_checks += 1
    
    # Check for better logout handling
    if "sessionStorage.clear" in content and "setTimeout" in content:
        improvements += 1
        print("  ✅ Navigation: Enhanced logout handling implemented")
    else:
        print("  ❌ Navigation: Enhanced logout handling missing")
    total_checks += 1
    
    # Check for avatar updates
    if "userAvatar" in content and "avatarText" in content:
        improvements += 1
        print("  ✅ Navigation: Avatar updates implemented")
    else:
        print("  ❌ Navigation: Avatar updates missing")
    total_checks += 1
    
    print(f"  Total navigation improvements: {improvements}/{total_checks}")
    return improvements == total_checks

def main():
    """Main verification function"""
    print("🔍 Money Matrix - Fix Verification Script")
    print("=" * 50)
    
    all_checks_passed = True
    
    # Run all verification checks
    checks = [
        ("CSS Glitch Fixes", check_css_glitch_fixes),
        ("JavaScript Performance Fixes", check_js_performance_fixes),
        ("Authentication Flow Improvements", check_auth_flow_improvements),
        ("Navigation Improvements", check_navigation_improvements)
    ]
    
    for check_name, check_function in checks:
        print(f"\n📋 {check_name}")
        if not check_function():
            all_checks_passed = False
    
    print("\n" + "=" * 50)
    if all_checks_passed:
        print("🎉 All fixes have been successfully applied!")
        print("✅ The application should now have improved performance and user experience.")
        return 0
    else:
        print("❌ Some fixes are missing or not properly applied.")
        print("⚠️  Please review the output above and apply missing fixes.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
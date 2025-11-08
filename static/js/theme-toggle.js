/**
 * Theme Toggle
 * Dark/Light mode switcher
 */

class ThemeManager {
    constructor() {
        this.theme = localStorage.getItem('theme') || 'auto';
        this.initialize();
    }

    /**
     * Initialize theme
     */
    initialize() {
        this.applyTheme(this.theme);
        this.setupToggle();
        this.updateIcon();
        this.addThemeTransition();
        this.addThemeChangeEffect();
    }

    /**
     * Apply theme with smooth transition
     */
    applyTheme(theme) {
        // Add transition class for smooth theme switching
        document.documentElement.classList.add('theme-transition');
        
        document.documentElement.setAttribute('data-theme', theme);
        this.theme = theme;
        localStorage.setItem('theme', theme);
        
        // Add theme change ripple effect
        this.addThemeChangeRipple();
        
        // Remove transition class after animation completes
        setTimeout(() => {
            document.documentElement.classList.remove('theme-transition');
        }, 300);
    }

    /**
     * Toggle theme with animation
     */
    toggle() {
        const themes = ['light', 'dark', 'auto'];
        const currentIndex = themes.indexOf(this.theme);
        const nextIndex = (currentIndex + 1) % themes.length;
        const nextTheme = themes[nextIndex];
        
        // Add ripple effect to toggle button
        this.addRippleEffect();
        
        this.applyTheme(nextTheme);
        this.updateIcon();
        
        // Show toast notification
        if (window.Toast) {
            window.Toast.show(`Theme: ${nextTheme.charAt(0).toUpperCase() + nextTheme.slice(1)}`, 'info');
        }
    }

    /**
     * Update toggle icon with animation
     */
    updateIcon() {
        const icon = document.querySelector('#theme-toggle .theme-icon');
        if (!icon) return;

        const icons = {
            'light': '☀️',
            'dark': '🌙',
            'auto': '🌓'
        };

        // Add animation class
        icon.classList.add('theme-icon-change');
        
        // Update icon after a short delay for animation
        setTimeout(() => {
            icon.textContent = icons[this.theme] || '🌓';
            icon.classList.remove('theme-icon-change');
        }, 150);
    }

    /**
     * Setup toggle button
     */
    setupToggle() {
        const toggleBtn = document.getElementById('theme-toggle');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => this.toggle());
            
            // Add keyboard support
            toggleBtn.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    this.toggle();
                }
            });
            
            // Add hover effect
            toggleBtn.addEventListener('mouseenter', () => {
                toggleBtn.classList.add('theme-toggle-hover');
            });
            
            toggleBtn.addEventListener('mouseleave', () => {
                toggleBtn.classList.remove('theme-toggle-hover');
            });
        }
    }

    /**
     * Get current effective theme (resolves 'auto')
     */
    getEffectiveTheme() {
        if (this.theme === 'auto') {
            return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
        }
        return this.theme;
    }

    /**
     * Add theme transition styles
     */
    addThemeTransition() {
        if (!document.getElementById('theme-transition-styles')) {
            const style = document.createElement('style');
            style.id = 'theme-transition-styles';
            style.textContent = `
                .theme-transition * {
                    transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease !important;
                }
                
                .theme-icon-change {
                    animation: spin 0.3s ease;
                }
                
                .theme-toggle-hover {
                    transform: scale(1.1);
                    transition: transform 0.2s ease;
                }
                
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
            `;
            document.head.appendChild(style);
        }
    }

    /**
     * Add ripple effect to toggle button
     */
    addRippleEffect() {
        const toggleBtn = document.getElementById('theme-toggle');
        if (!toggleBtn) return;

        const ripple = document.createElement('span');
        ripple.classList.add('ripple');
        toggleBtn.appendChild(ripple);

        // Remove ripple after animation
        setTimeout(() => {
            if (ripple.parentNode) {
                ripple.parentNode.removeChild(ripple);
            }
        }, 600);
    }
    
    /**
     * Add theme change ripple effect across the screen
     */
    addThemeChangeRipple() {
        // Create ripple effect element
        const ripple = document.createElement('div');
        ripple.classList.add('theme-change-ripple');
        document.body.appendChild(ripple);
        
        // Remove after animation
        setTimeout(() => {
            if (ripple.parentNode) {
                ripple.parentNode.removeChild(ripple);
            }
        }, 1000);
    }
    
    /**
     * Add theme change effect styles
     */
    addThemeChangeEffect() {
        if (!document.getElementById('theme-change-effect')) {
            const style = document.createElement('style');
            style.id = 'theme-change-effect';
            style.textContent = `
                .theme-change-ripple {
                    position: fixed;
                    top: 50%;
                    left: 50%;
                    width: 0;
                    height: 0;
                    border-radius: 50%;
                    background: rgba(255, 255, 255, 0.1);
                    transform: translate(-50%, -50%);
                    animation: rippleEffect 0.8s ease-out;
                    pointer-events: none;
                    z-index: 9999;
                }
                
                [data-theme="dark"] .theme-change-ripple {
                    background: rgba(0, 0, 0, 0.2);
                }
                
                @keyframes rippleEffect {
                    0% {
                        width: 0;
                        height: 0;
                        opacity: 0.5;
                    }
                    100% {
                        width: 200vmax;
                        height: 200vmax;
                        opacity: 0;
                    }
                }
            `;
            document.head.appendChild(style);
        }
    }
}

// Initialize theme manager
window.themeManager = new ThemeManager();

// Listen for system theme changes
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    if (window.themeManager.theme === 'auto') {
        window.themeManager.applyTheme('auto');
    }
});

// Add global keyboard shortcut for theme toggle (Ctrl+Shift+T)
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.shiftKey && e.key === 'T') {
        e.preventDefault();
        if (window.themeManager) {
            window.themeManager.toggle();
        }
    }
});
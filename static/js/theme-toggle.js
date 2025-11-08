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
                    transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease !important;
                }
                
                .theme-icon-change {
                    animation: spin 0.3s ease;
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
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
    }

    /**
     * Apply theme
     */
    applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        this.theme = theme;
        localStorage.setItem('theme', theme);
    }

    /**
     * Toggle theme
     */
    toggle() {
        const themes = ['light', 'dark', 'auto'];
        const currentIndex = themes.indexOf(this.theme);
        const nextIndex = (currentIndex + 1) % themes.length;
        const nextTheme = themes[nextIndex];
        
        this.applyTheme(nextTheme);
        this.updateIcon();
        
        // Show toast notification
        if (window.Toast) {
            window.Toast.show(`Theme: ${nextTheme}`, 'info');
        }
    }

    /**
     * Update toggle icon
     */
    updateIcon() {
        const icon = document.querySelector('#theme-toggle .theme-icon');
        if (!icon) return;

        const icons = {
            'light': '☀️',
            'dark': '🌙',
            'auto': '🌓'
        };

        icon.textContent = icons[this.theme] || '🌓';
    }

    /**
     * Setup toggle button
     */
    setupToggle() {
        const toggleBtn = document.getElementById('theme-toggle');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => this.toggle());
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
}

// Initialize theme manager
window.themeManager = new ThemeManager();

// Listen for system theme changes
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    if (window.themeManager.theme === 'auto') {
        window.themeManager.applyTheme('auto');
    }
});

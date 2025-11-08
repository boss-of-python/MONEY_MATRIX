/**
 * Main Application JavaScript
 * Global initialization and utilities
 */

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

/**
 * Initialize application
 */
function initializeApp() {
    // Initialize theme
    initializeTheme();
    
    // Log app initialization
    console.log('Money Matrix initialized');
}

/**
 * Initialize theme from localStorage or system preference
 */
function initializeTheme() {
    const savedTheme = localStorage.getItem('theme') || 'auto';
    document.documentElement.setAttribute('data-theme', savedTheme);
}

/**
 * Format currency
 */
function formatCurrency(amount, currency = 'USD') {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: currency
    }).format(amount);
}

/**
 * Format date
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return new Intl.DateFormat('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    }).format(date);
}

/**
 * Debounce function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Show loading state
 */
function showLoading(element) {
    element.classList.add('loading');
    element.disabled = true;
}

/**
 * Hide loading state
 */
function hideLoading(element) {
    element.classList.remove('loading');
    element.disabled = false;
}

// Export utilities
window.MoneyMatrix = {
    formatCurrency,
    formatDate,
    debounce,
    showLoading,
    hideLoading
};

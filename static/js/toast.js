/**
 * Toast Notification System
 * Show success, error, warning, and info messages
 */

class Toast {
    static show(message, type = 'success', duration = 3000) {
        const container = document.getElementById('toast-container') || this.createContainer();
        const toast = this.createToast(message, type);
        
        container.appendChild(toast);
        
        // Trigger animation
        setTimeout(() => toast.classList.add('show'), 10);
        
        // Auto-remove after duration
        if (duration > 0) {
            setTimeout(() => {
                this.removeToast(toast);
            }, duration);
        }
        
        // Add close button functionality
        const closeBtn = toast.querySelector('.toast-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => this.removeToast(toast));
        }
        
        return toast;
    }

    static createContainer() {
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container';
        document.body.appendChild(container);
        return container;
    }

    static createToast(message, type) {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type} glass-effect`;
        
        const icons = {
            success: '✓',
            error: '✗',
            warning: '⚠',
            info: 'ℹ'
        };

        const colors = {
            success: '#10B981',
            error: '#EF4444',
            warning: '#F59E0B',
            info: '#3B82F6'
        };

        toast.innerHTML = `
            <div class="toast-icon">${icons[type]}</div>
            <div class="toast-content">
                <div class="toast-message">${message}</div>
            </div>
            <button class="toast-close">&times;</button>
        `;

        // Add hover pause functionality
        let timeoutId;
        toast.addEventListener('mouseenter', () => {
            if (timeoutId) clearTimeout(timeoutId);
        });
        
        toast.addEventListener('mouseleave', () => {
            timeoutId = setTimeout(() => {
                this.removeToast(toast);
            }, 2000);
        });
        
        return toast;
    }

    static removeToast(toast) {
        toast.classList.remove('show');
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300);
    }

    static success(message, duration) {
        return this.show(message, 'success', duration);
    }

    static error(message, duration) {
        return this.show(message, 'error', duration);
    }

    static warning(message, duration) {
        return this.show(message, 'warning', duration);
    }

    static info(message, duration) {
        return this.show(message, 'info', duration);
    }
    
    static loading(message = 'Loading...', duration = 0) {
        const toast = this.show(`
            <div class="toast-loading">
                <div class="spinner spinner-sm"></div>
                <span>${message}</span>
            </div>
        `, 'info', duration);
        
        toast.classList.add('toast-loading-container');
        return toast;
    }
}

// Export Toast globally
window.Toast = Toast;
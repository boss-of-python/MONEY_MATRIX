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
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, duration);
    }

    static createContainer() {
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.style.cssText = `
            position: fixed;
            top: 80px;
            right: 20px;
            z-index: 1200;
            display: flex;
            flex-direction: column;
            gap: 10px;
        `;
        document.body.appendChild(container);
        return container;
    }

    static createToast(message, type) {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        
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

        toast.style.cssText = `
            background: var(--color-card);
            color: var(--color-text);
            padding: 1rem 1.5rem;
            border-radius: 0.5rem;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            border-left: 4px solid ${colors[type]};
            display: flex;
            align-items: center;
            gap: 0.75rem;
            min-width: 300px;
            max-width: 500px;
            opacity: 0;
            transform: translateX(100%);
            transition: all 0.3s ease;
        `;

        toast.innerHTML = `
            <span style="
                width: 24px;
                height: 24px;
                border-radius: 50%;
                background: ${colors[type]};
                color: white;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                flex-shrink: 0;
            ">${icons[type]}</span>
            <span style="flex: 1;">${message}</span>
            <button onclick="this.parentElement.remove()" style="
                background: none;
                border: none;
                color: var(--color-text-secondary);
                cursor: pointer;
                font-size: 1.25rem;
                padding: 0;
                width: 20px;
                height: 20px;
            ">×</button>
        `;

        toast.classList.add('toast');
        
        return toast;
    }

    static success(message, duration) {
        this.show(message, 'success', duration);
    }

    static error(message, duration) {
        this.show(message, 'error', duration);
    }

    static warning(message, duration) {
        this.show(message, 'warning', duration);
    }

    static info(message, duration) {
        this.show(message, 'info', duration);
    }
}

// Add CSS for toast show animation
const style = document.createElement('style');
style.textContent = `
    .toast.show {
        opacity: 1 !important;
        transform: translateX(0) !important;
    }
`;
document.head.appendChild(style);

// Export Toast globally
window.Toast = Toast;

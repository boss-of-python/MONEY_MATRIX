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
    
    // Initialize smooth scrolling
    initializeSmoothScrolling();
    
    // Initialize animations
    initializeAnimations();
    
    // Initialize loading states
    initializeLoadingStates();
    
    // Initialize particles background
    initializeParticles();
    
    // Initialize performance monitoring
    initializePerformanceMonitoring();
    
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
 * Initialize smooth scrolling
 */
function initializeSmoothScrolling() {
    // Add smooth scrolling to all links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Initialize animations
 */
function initializeAnimations() {
    // Add intersection observer for scroll animations
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                // Add staggered animation for child elements
                const children = entry.target.querySelectorAll('*');
                children.forEach((child, index) => {
                    setTimeout(() => {
                        child.classList.add('animate-in-child');
                    }, index * 50);
                });
            }
        });
    }, observerOptions);
    
    // Observe elements with animation classes
    document.querySelectorAll('.fade-in, .slide-in-up, .slide-in-down, .scale-in, .staggered-children').forEach(el => {
        observer.observe(el);
    });
}

/**
 * Initialize loading states
 */
function initializeLoadingStates() {
    // Add loading indicators to buttons with data-loading attribute
    document.querySelectorAll('[data-loading]').forEach(button => {
        button.addEventListener('click', function() {
            const originalText = this.innerHTML;
            const loadingText = this.getAttribute('data-loading') || 'Loading...';
            
            this.innerHTML = `<span class="spinner spinner-sm"></span> ${loadingText}`;
            this.disabled = true;
            
            // Store original text for later restoration
            this.setAttribute('data-original-text', originalText);
        });
    });
}

/**
 * Initialize particles background
 */
function initializeParticles() {
    // Create a simple particle system for background
    const particlesContainer = document.createElement('div');
    particlesContainer.id = 'particles-background';
    particlesContainer.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        pointer-events: none;
        overflow: hidden;
    `;
    document.body.appendChild(particlesContainer);
    
    // Create particles
    for (let i = 0; i < 30; i++) {
        const particle = document.createElement('div');
        particle.style.cssText = `
            position: absolute;
            width: ${Math.random() * 5 + 1}px;
            height: ${Math.random() * 5 + 1}px;
            background: rgba(79, 70, 229, 0.3);
            border-radius: 50%;
            top: ${Math.random() * 100}%;
            left: ${Math.random() * 100}%;
            animation: floatParticle ${Math.random() * 10 + 10}s infinite ease-in-out;
            animation-delay: ${Math.random() * 5}s;
        `;
        particlesContainer.appendChild(particle);
    }
    
    // Add CSS for particle animation
    if (!document.getElementById('particles-styles')) {
        const style = document.createElement('style');
        style.id = 'particles-styles';
        style.textContent = `
            @keyframes floatParticle {
                0%, 100% {
                    transform: translate(0, 0);
                }
                25% {
                    transform: translate(${Math.random() * 20 - 10}px, ${Math.random() * 20 - 10}px);
                }
                50% {
                    transform: translate(${Math.random() * 30 - 15}px, ${Math.random() * 30 - 15}px);
                }
                75% {
                    transform: translate(${Math.random() * 20 - 10}px, ${Math.random() * 20 - 10}px);
                }
            }
        `;
        document.head.appendChild(style);
    }
}

/**
 * Initialize performance monitoring
 */
function initializePerformanceMonitoring() {
    // Log performance metrics
    if ('performance' in window) {
        window.addEventListener('load', () => {
            setTimeout(() => {
                const perfData = performance.getEntriesByType('navigation')[0];
                console.log('Page Load Time:', perfData.loadEventEnd - perfData.fetchStart, 'ms');
                console.log('DOM Content Loaded:', perfData.domContentLoadedEventEnd - perfData.fetchStart, 'ms');
            }, 0);
        });
    }
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
    return new Intl.DateTimeFormat('en-US', {
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
 * Throttle function
 */
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
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

/**
 * Show toast notification
 */
function showToast(message, type = 'info', duration = 3000) {
    if (window.Toast) {
        window.Toast.show(message, type, duration);
    } else {
        // Fallback to console
        console.log(`[${type.toUpperCase()}] ${message}`);
    }
}

/**
 * Get user info from localStorage
 */
function getUserInfo() {
    return {
        name: localStorage.getItem('userName') || 'User',
        email: localStorage.getItem('userEmail') || 'user@example.com',
        avatar: localStorage.getItem('userAvatar') || 'U'
    };
}

/**
 * Set user info in localStorage
 */
function setUserInfo(name, email, avatar) {
    localStorage.setItem('userName', name);
    localStorage.setItem('userEmail', email);
    localStorage.setItem('userAvatar', avatar);
}

/**
 * Animated scroll to element
 */
function scrollToElement(element, offset = 0) {
    const elementPosition = element.getBoundingClientRect().top;
    const offsetPosition = elementPosition + window.pageYOffset - offset;
    
    window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
    });
}

/**
 * Validate form field
 */
function validateField(field, rules) {
    const value = field.value.trim();
    let isValid = true;
    let errorMessage = '';
    
    // Required validation
    if (rules.required && !value) {
        isValid = false;
        errorMessage = 'This field is required';
    }
    
    // Email validation
    if (rules.email && value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
        isValid = false;
        errorMessage = 'Please enter a valid email address';
    }
    
    // Min length validation
    if (rules.minLength && value.length < rules.minLength) {
        isValid = false;
        errorMessage = `Minimum length is ${rules.minLength} characters`;
    }
    
    // Max length validation
    if (rules.maxLength && value.length > rules.maxLength) {
        isValid = false;
        errorMessage = `Maximum length is ${rules.maxLength} characters`;
    }
    
    // Custom validation
    if (rules.custom && typeof rules.custom === 'function') {
        const customResult = rules.custom(value);
        if (customResult !== true) {
            isValid = false;
            errorMessage = customResult || 'Invalid value';
        }
    }
    
    // Update UI
    const errorElement = field.parentNode.querySelector('.form-error');
    if (errorElement) {
        errorElement.textContent = isValid ? '' : errorMessage;
    }
    
    field.classList.toggle('invalid', !isValid);
    field.classList.toggle('valid', isValid);
    
    return { isValid, errorMessage };
}

/**
 * Validate entire form
 */
function validateForm(form, validationRules) {
    let isFormValid = true;
    const errors = {};
    
    Object.keys(validationRules).forEach(fieldName => {
        const field = form.querySelector(`[name="${fieldName}"]`);
        if (field) {
            const result = validateField(field, validationRules[fieldName]);
            if (!result.isValid) {
                isFormValid = false;
                errors[fieldName] = result.errorMessage;
            }
        }
    });
    
    return { isValid: isFormValid, errors };
}

// Export utilities
window.MoneyMatrix = {
    formatCurrency,
    formatDate,
    debounce,
    throttle,
    showLoading,
    hideLoading,
    showToast,
    getUserInfo,
    setUserInfo,
    scrollToElement,
    validateField,
    validateForm
};

// Add global event listeners
document.addEventListener('click', function(e) {
    // Handle loading button restoration
    if (e.target.hasAttribute('data-original-text')) {
        setTimeout(() => {
            e.target.innerHTML = e.target.getAttribute('data-original-text');
            e.target.disabled = false;
            e.target.removeAttribute('data-original-text');
        }, 2000);
    }
    
    // Add ripple effect to buttons
    if (e.target.closest('button, .btn')) {
        const button = e.target.closest('button, .btn');
        const ripple = document.createElement('span');
        ripple.classList.add('ripple');
        button.appendChild(ripple);
        
        // Remove ripple after animation
        setTimeout(() => {
            ripple.remove();
        }, 600);
    }
});
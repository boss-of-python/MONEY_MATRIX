/**
 * Navigation JavaScript
 * Handles navigation menu functionality
 */

// Initialize navigation when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    initializeNavigation();
});

/**
 * Initialize navigation functionality
 */
function initializeNavigation() {
    // Initialize mobile menu toggle
    initializeMobileMenu();
    
    // Initialize user dropdown
    initializeUserDropdown();
    
    // Initialize notification dropdown
    initializeNotificationDropdown();
    
    // Initialize navbar scroll effect
    initializeNavbarScrollEffect();
    
    // Initialize active link highlighting
    initializeActiveLinkHighlighting();
    
    // Initialize user info updates
    initializeUserInfoUpdates();
    
    console.log('Navigation initialized');
}

/**
 * Initialize mobile menu toggle
 */
function initializeMobileMenu() {
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const navLinks = document.getElementById('navLinks');
    
    if (mobileMenuToggle && navLinks) {
        mobileMenuToggle.addEventListener('click', function() {
            navLinks.classList.toggle('active');
            this.classList.toggle('active');
        });
        
        // Close mobile menu when clicking a link
        document.querySelectorAll('#navLinks a').forEach(link => {
            link.addEventListener('click', function() {
                // Add a small delay to ensure navigation works properly
                setTimeout(() => {
                    navLinks.classList.remove('active');
                    mobileMenuToggle.classList.remove('active');
                }, 100);
            });
        });
    }
}

/**
 * Initialize user dropdown
 */
function initializeUserDropdown() {
    const userMenuBtn = document.getElementById('userMenuBtn');
    const userDropdown = document.getElementById('userDropdown');
    const notificationDropdown = document.getElementById('notificationDropdown');
    
    if (userMenuBtn && userDropdown) {
        userMenuBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            userDropdown.classList.toggle('active');
            if (notificationDropdown) {
                notificationDropdown.classList.remove('active');
            }
        });
    }
}

/**
 * Initialize notification dropdown
 */
function initializeNotificationDropdown() {
    const notificationBtn = document.getElementById('notificationBtn');
    const notificationDropdown = document.getElementById('notificationDropdown');
    const userDropdown = document.getElementById('userDropdown');
    
    if (notificationBtn && notificationDropdown) {
        notificationBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            notificationDropdown.classList.toggle('active');
            if (userDropdown) {
                userDropdown.classList.remove('active');
            }
        });
    }
}

/**
 * Close dropdowns when clicking outside
 */
document.addEventListener('click', function(e) {
    if (!e.target.closest('.user-menu') && !e.target.closest('.notification-menu')) {
        const userDropdown = document.getElementById('userDropdown');
        const notificationDropdown = document.getElementById('notificationDropdown');
        
        if (userDropdown) {
            userDropdown.classList.remove('active');
        }
        
        if (notificationDropdown) {
            notificationDropdown.classList.remove('active');
        }
    }
});

/**
 * Logout function
 */
async function logout() {
    try {
        showLoadingState();
        
        // Try to logout from Firebase if available
        if (typeof firebase !== 'undefined' && firebase.auth) {
            try {
                await firebase.auth().signOut();
            } catch (firebaseError) {
                console.error('Firebase logout error:', firebaseError);
                // Continue with logout even if Firebase fails
            }
        }
        
        // Backend logout
        try {
            await fetch('/auth/logout', { 
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
        } catch (backendError) {
            console.error('Backend logout error:', backendError);
            // Continue with client-side logout even if backend fails
        }
        
        // Clear all user data from localStorage
        localStorage.removeItem('auth_token');
        localStorage.removeItem('user_email');
        localStorage.removeItem('user_name');
        localStorage.removeItem('user_avatar');
        
        // Clear session storage as well
        sessionStorage.clear();
        
        Toast.success('Logged out successfully');
        
        // Redirect to login page after a short delay to show success message
        setTimeout(() => {
            window.location.href = '/auth/login';
        }, 1000);
    } catch (error) {
        console.error('Logout failed:', error);
        Toast.error('Logout failed. Please try again.');
        hideLoadingState();
    }
}

/**
 * Show loading state for logout button
 */
function showLoadingState() {
    const logoutBtn = document.querySelector('.dropdown-item-danger');
    if (logoutBtn) {
        logoutBtn.innerHTML = '<span class="spinner spinner-sm"></span> Logging out...';
        logoutBtn.disabled = true;
    }
}

/**
 * Hide loading state for logout button
 */
function hideLoadingState() {
    const logoutBtn = document.querySelector('.dropdown-item-danger');
    if (logoutBtn) {
        logoutBtn.innerHTML = '<span class="dropdown-icon">🚪</span> Logout';
        logoutBtn.disabled = false;
    }
}

/**
 * Simulate notification updates
 */
function updateNotifications() {
    const notificationCount = document.getElementById('notificationCount');
    const notificationList = document.getElementById('notificationList');
    
    // Simulate new notifications
    const notifications = [
        { message: "Your monthly budget report is ready", time: "5 minutes ago" },
        { message: "New transaction added successfully", time: "1 hour ago" },
        { message: "Reminder: Review your budget", time: "1 day ago" }
    ];
    
    // Update count
    if (notificationCount) {
        notificationCount.textContent = notifications.length;
        notificationCount.style.display = notifications.length > 0 ? 'flex' : 'none';
    }
    
    // Update list with document fragment for better performance
    if (notificationList) {
        const fragment = document.createDocumentFragment();
        notifications.forEach(notification => {
            const item = document.createElement('div');
            item.className = 'notification-item';
            item.innerHTML = `
                <p>${notification.message}</p>
                <span class="notification-time">${notification.time}</span>
            `;
            fragment.appendChild(item);
        });
        
        // Clear and update list in one operation
        notificationList.innerHTML = '';
        notificationList.appendChild(fragment);
    }
}

/**
 * Initialize navbar scroll effect
 */
function initializeNavbarScrollEffect() {
    let ticking = false;
    
    function updateNavbar() {
        const navbar = document.querySelector('.navbar');
        if (navbar) {
            if (window.scrollY > 50) {
                navbar.classList.add('navbar-scrolled');
            } else {
                navbar.classList.remove('navbar-scrolled');
            }
        }
        ticking = false;
    }
    
    function requestTick() {
        if (!ticking) {
            requestAnimationFrame(updateNavbar);
            ticking = true;
        }
    }
    
    window.addEventListener('scroll', requestTick);
}

/**
 * Initialize active link highlighting
 */
function initializeActiveLinkHighlighting() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    // Remove any existing active classes
    navLinks.forEach(link => {
        link.classList.remove('active');
    });
    
    // Find the best matching link
    let bestMatch = null;
    let bestMatchLength = 0;
    
    navLinks.forEach(link => {
        const linkPath = link.getAttribute('href');
        if (linkPath && currentPath.startsWith(linkPath) && linkPath.length > bestMatchLength) {
            bestMatch = link;
            bestMatchLength = linkPath.length;
        }
    });
    
    // Special case for dashboard - if no specific match and we're at root, highlight dashboard
    if (!bestMatch && (currentPath === '/' || currentPath === '')) {
        const dashboardLink = document.querySelector('.nav-link-dashboard');
        if (dashboardLink) {
            bestMatch = dashboardLink;
        }
    }
    
    // Apply active class to best match
    if (bestMatch) {
        bestMatch.classList.add('active');
    }
}

/**
 * Initialize user info updates
 */
function initializeUserInfoUpdates() {
    // Update user info from localStorage on load
    updateUserInfo();
    
    // Listen for storage changes
    window.addEventListener('storage', function(e) {
        if (e.key === 'user_name' || e.key === 'user_email') {
            updateUserInfo();
        }
    });
}

/**
 * Update user info in navigation
 */
function updateUserInfo() {
    const userName = document.getElementById('userName');
    const userEmail = document.getElementById('userEmail');
    const userAvatar = document.querySelector('.user-avatar');
    const userAvatarLarge = document.querySelector('.user-avatar-large');
    
    if (userName && userEmail) {
        const name = localStorage.getItem('user_name') || 'User';
        const email = localStorage.getItem('user_email') || 'user@example.com';
        
        userName.textContent = name;
        userEmail.textContent = email;
        
        // Update avatar with first letter of name or email
        const avatarText = name.charAt(0).toUpperCase() || email.charAt(0).toUpperCase();
        if (userAvatar) userAvatar.textContent = avatarText;
        if (userAvatarLarge) userAvatarLarge.textContent = avatarText;
    }
}

// Export navigation functions
window.Navigation = {
    logout,
    updateNotifications,
    updateUserInfo
};
/* Coaching Portal JavaScript */

/**
 * Initialize tooltips and popovers
 */
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips if available
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize Bootstrap popovers if available
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});

/**
 * Form validation handler
 */
function validateForm(formElement) {
    let isValid = true;
    const inputs = formElement.querySelectorAll('input, select, textarea');

    inputs.forEach(input => {
        if (!input.checkValidity()) {
            isValid = false;
            input.classList.add('is-invalid');
        } else {
            input.classList.remove('is-invalid');
        }
    });

    if (!isValid) {
        formElement.classList.add('was-validated');
    }

    return isValid;
}

/**
 * Show loading state on button
 */
function showLoadingState(button) {
    const originalText = button.innerHTML;
    button.disabled = true;
    button.innerHTML = `
        <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
        Loading...
    `;
    button.dataset.originalText = originalText;
    return () => resetButtonState(button);
}

/**
 * Reset button to original state
 */
function resetButtonState(button) {
    button.disabled = false;
    button.innerHTML = button.dataset.originalText || 'Submit';
}

/**
 * Display alert message
 */
function showAlert(container, message, type = 'danger') {
    const alertId = 'alert-' + Date.now();
    const alertHTML = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert" id="${alertId}">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    
    const alertElement = document.createElement('div');
    alertElement.innerHTML = alertHTML;
    container.insertBefore(alertElement.firstElementChild, container.firstChild);

    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        const alert = document.getElementById(alertId);
        if (alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }
    }, 5000);
}

/**
 * Format currency
 */
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

/**
 * Format date
 */
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

/**
 * Get query parameter from URL
 */
function getQueryParameter(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
}

/**
 * Format phone number
 */
function formatPhoneNumber(input) {
    // Remove non-digits
    let value = input.value.replace(/\D/g, '');
    
    // Format as (XXX) XXX-XXXX
    if (value.length > 0) {
        if (value.length <= 3) {
            value = `(${value}`;
        } else if (value.length <= 6) {
            value = `(${value.slice(0, 3)}) ${value.slice(3)}`;
        } else {
            value = `(${value.slice(0, 3)}) ${value.slice(3, 6)}-${value.slice(6, 10)}`;
        }
    }
    
    input.value = value;
}

/**
 * Debounce function for search input
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
 * Fetch with error handling
 */
async function fetchWithErrorHandling(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || `HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Fetch error:', error);
        throw error;
    }
}

/**
 * Copy to clipboard
 */
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        console.log('Copied to clipboard');
    }).catch(err => {
        console.error('Failed to copy:', err);
    });
}

/**
 * Initialize Bootstrap table (if using DataTables)
 */
function initializeTable(tableElement) {
    if (typeof $ !== 'undefined' && $.fn.dataTable) {
        $(tableElement).DataTable({
            responsive: true,
            pageLength: 10,
            language: {
                search: "Filter records:"
            }
        });
    }
}

/**
 * Validate email format
 */
function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

/**
 * Validate phone number format
 */
function isValidPhoneNumber(phone) {
    const re = /^[\d\s\-\(\)\+]+$/;
    return re.test(phone) && phone.replace(/\D/g, '').length >= 10;
}

/**
 * Set active nav link
 */
function setActiveNavLink() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');

    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPath) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

// Initialize active nav link on page load
document.addEventListener('DOMContentLoaded', setActiveNavLink);

/**
 * Scroll to element smoothly
 */
function scrollToElement(selector) {
    const element = document.querySelector(selector);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

/**
 * Show/hide password toggle
 */
function togglePasswordVisibility(inputId) {
    const input = document.getElementById(inputId);
    if (input) {
        input.type = input.type === 'password' ? 'text' : 'password';
    }
}

// Export for use in other scripts
window.CoachingPortal = {
    validateForm,
    showLoadingState,
    resetButtonState,
    showAlert,
    formatCurrency,
    formatDate,
    getQueryParameter,
    formatPhoneNumber,
    debounce,
    fetchWithErrorHandling,
    copyToClipboard,
    isValidEmail,
    isValidPhoneNumber,
    scrollToElement,
    togglePasswordVisibility
};

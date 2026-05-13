// Custom JavaScript for Campus Lost & Found Portal

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Confirm delete actions
    var deleteButtons = document.querySelectorAll('a[href*="delete"]');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });

    // Image preview for file uploads
    var imageInputs = document.querySelectorAll('input[type="file"]');
    imageInputs.forEach(function(input) {
        input.addEventListener('change', function(e) {
            var file = e.target.files[0];
            if (file && file.type.startsWith('image/')) {
                var reader = new FileReader();
                reader.onload = function(e) {
                    // You can add image preview functionality here
                    console.log('Image selected:', file.name);
                };
                reader.readAsDataURL(file);
            }
        });
    });

    // Search form enhancement
    var searchForm = document.querySelector('form[action*="search"]');
    if (searchForm) {
        var searchInput = searchForm.querySelector('input[name="search_term"]');
        if (searchInput) {
            searchInput.addEventListener('input', function() {
                // Debounce search suggestions (placeholder)
                clearTimeout(window.searchTimeout);
                window.searchTimeout = setTimeout(function() {
                    // Implement search suggestions if needed
                }, 300);
            });
        }
    }

    // Dashboard analytics (mock data for demo)
    updateDashboardStats();

    // Dark mode toggle (placeholder for future implementation)
    var darkModeToggle = document.getElementById('darkModeToggle');
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
            localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
        });
    }

    // Load dark mode preference
    if (localStorage.getItem('darkMode') === 'true') {
        document.body.classList.add('dark-mode');
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            var target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Form validation enhancement
    var forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            var requiredFields = form.querySelectorAll('[required]');
            var isValid = true;
            
            requiredFields.forEach(function(field) {
                if (!field.value.trim()) {
                    field.classList.add('is-invalid');
                    isValid = false;
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                alert('Please fill in all required fields.');
            }
        });
    });

    // Activity feed updates (mock)
    setInterval(function() {
        // Simulate real-time updates
        console.log('Checking for updates...');
    }, 30000); // Check every 30 seconds
});

function updateDashboardStats() {
    // Mock function to update dashboard statistics
    // In a real app, this would fetch data from the server
    var statCards = document.querySelectorAll('.card .display-4');
    statCards.forEach(function(card) {
        // Simulate dynamic updates
        var currentValue = parseInt(card.textContent);
        // Random small changes for demo
        var change = Math.floor(Math.random() * 3) - 1; // -1, 0, or 1
        card.textContent = Math.max(0, currentValue + change);
    });
}

// Utility functions
function showNotification(message, type = 'info') {
    var alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    var container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
    }
    
    setTimeout(function() {
        var bsAlert = new bootstrap.Alert(alertDiv);
        bsAlert.close();
    }, 5000);
}

function formatDate(dateString) {
    var date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Export functions for potential use in other scripts
window.CampusLostFound = {
    showNotification: showNotification,
    formatDate: formatDate,
    updateDashboardStats: updateDashboardStats
};
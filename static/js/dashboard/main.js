document.addEventListener('DOMContentLoaded', function() {
    // Sidebar Toggle
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');
    const mainContent = document.querySelector('.main-content');

    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('active');
            mainContent.classList.toggle('sidebar-hidden');
        });
    }

    // Close sidebar on mobile when clicking outside
    document.addEventListener('click', (e) => {
        if (window.innerWidth <= 768) {
            if (!sidebar.contains(e.target) && !sidebarToggle.contains(e.target)) {
                sidebar.classList.remove('active');
            }
        }
    });

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // File Upload Preview
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const preview = document.querySelector(`#${this.dataset.preview}`);
                    if (preview) {
                        if (file.type.startsWith('image/')) {
                            preview.src = e.target.result;
                        } else {
                            preview.textContent = file.name;
                        }
                    }
                }.bind(this);
                reader.readAsDataURL(file);
            }
        });
    });

    // Form Validation
    const forms = document.querySelectorAll('form[data-validate]');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!this.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            this.classList.add('was-validated');
        });
    });

    // Real-time Password Strength Meter
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    passwordInputs.forEach(input => {
        input.addEventListener('input', function() {
            const strength = calculatePasswordStrength(this.value);
            const strengthMeter = document.querySelector(`#${this.dataset.strengthMeter}`);
            if (strengthMeter) {
                strengthMeter.style.width = `${strength}%`;
                strengthMeter.className = `progress-bar ${getStrengthClass(strength)}`;
            }
        });
    });

    // Notification System
    const notificationCount = document.getElementById('notification-count');
    if (notificationCount) {
        // Update notification count periodically
        setInterval(updateNotificationCount, 30000);
    }

    // Search Functionality
    const searchInput = document.querySelector('.search-box input');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                performSearch(this.value);
            }, 300);
        });
    }

    // Profile Completion Progress
    updateProfileProgress();

    // Dark Mode Toggle
    const themeToggle = document.getElementById('theme-toggle');
    const html = document.documentElement;
    
    // Check for saved theme preference
    const savedTheme = localStorage.getItem('theme') || 'light';
    html.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
    
    themeToggle.addEventListener('click', function(e) {
        e.preventDefault();
        const currentTheme = html.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        
        html.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(newTheme);
    });
});

// Helper Functions
function calculatePasswordStrength(password) {
    let strength = 0;
    if (password.length >= 8) strength += 20;
    if (password.match(/[a-z]/)) strength += 20;
    if (password.match(/[A-Z]/)) strength += 20;
    if (password.match(/[0-9]/)) strength += 20;
    if (password.match(/[^a-zA-Z0-9]/)) strength += 20;
    return strength;
}

function getStrengthClass(strength) {
    if (strength <= 20) return 'bg-danger';
    if (strength <= 40) return 'bg-warning';
    if (strength <= 60) return 'bg-info';
    if (strength <= 80) return 'bg-primary';
    return 'bg-success';
}

function updateNotificationCount() {
    fetch('/api/notifications/count/')
        .then(response => response.json())
        .then(data => {
            const notificationCount = document.getElementById('notification-count');
            if (notificationCount) {
                notificationCount.textContent = data.count;
                if (data.count > 0) {
                    notificationCount.classList.add('has-notifications');
                } else {
                    notificationCount.classList.remove('has-notifications');
                }
            }
        })
        .catch(error => console.error('Error fetching notification count:', error));
}

function performSearch(query) {
    if (query.length < 2) return;
    
    fetch(`/api/search/?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            updateSearchResults(data);
        })
        .catch(error => console.error('Error performing search:', error));
}

function updateSearchResults(results) {
    const searchResults = document.querySelector('.search-results');
    if (!searchResults) return;

    searchResults.innerHTML = '';
    results.forEach(result => {
        const resultItem = document.createElement('div');
        resultItem.className = 'search-result-item';
        resultItem.innerHTML = `
            <a href="${result.url}">
                <i class="${result.icon}"></i>
                <span>${result.title}</span>
            </a>
        `;
        searchResults.appendChild(resultItem);
    });
}

function updateProfileProgress() {
    const progressBar = document.querySelector('.profile-progress');
    if (!progressBar) return;

    const requiredFields = document.querySelectorAll('[data-required="true"]');
    const totalFields = requiredFields.length;
    let completedFields = 0;

    requiredFields.forEach(field => {
        if (field.value.trim() !== '') {
            completedFields++;
        }
    });

    const progress = (completedFields / totalFields) * 100;
    progressBar.style.width = `${progress}%`;
    progressBar.setAttribute('aria-valuenow', progress);
    progressBar.textContent = `${Math.round(progress)}%`;
}

function updateThemeIcon(theme) {
    const themeToggle = document.getElementById('theme-toggle');
    const icon = themeToggle.querySelector('i');
    
    if (theme === 'dark') {
        icon.classList.remove('fa-moon');
        icon.classList.add('fa-sun');
        themeToggle.querySelector('span').textContent = 'Light Mode';
    } else {
        icon.classList.remove('fa-sun');
        icon.classList.add('fa-moon');
        themeToggle.querySelector('span').textContent = 'Dark Mode';
    }
} 
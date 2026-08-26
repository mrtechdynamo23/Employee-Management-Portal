/* ============================================
   EMPLOYEEHUB — MAIN JS (Global)
   ============================================ */

// Theme Management (Dark Mode)
function toggleTheme() {
    const html = document.documentElement;
    const current = html.getAttribute('data-theme');
    const newTheme = current === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('employeehub-theme', newTheme);

    // Update icon
    const icon = document.getElementById('themeIcon');
    if (icon) {
        icon.className = newTheme === 'dark' ? 'bi bi-sun' : 'bi bi-moon-stars';
    }

    // Update toggle checkbox in settings
    const toggle = document.getElementById('darkModeToggle');
    if (toggle) toggle.checked = newTheme === 'dark';
}

// Apply saved theme on load
document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('employeehub-theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);

    const icon = document.getElementById('themeIcon');
    if (icon) {
        icon.className = savedTheme === 'dark' ? 'bi bi-sun' : 'bi bi-moon-stars';
    }

    const toggle = document.getElementById('darkModeToggle');
    if (toggle) toggle.checked = savedTheme === 'dark';
});

// Auto-dismiss flash messages
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        const flashContainer = document.getElementById('flashContainer');
        if (flashContainer) {
            flashContainer.style.transition = 'opacity 0.5s';
            flashContainer.style.opacity = '0';
            setTimeout(() => flashContainer.remove(), 500);
        }
    }, 5000);
});

// Sidebar toggle for mobile
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    if (sidebar) {
        sidebar.classList.toggle('open');
    }
}

// Close sidebar when clicking outside on mobile
document.addEventListener('click', (e) => {
    const sidebar = document.getElementById('sidebar');
    const toggle = document.getElementById('sidebarToggle');
    if (sidebar && toggle && window.innerWidth <= 991) {
        if (!sidebar.contains(e.target) && !toggle.contains(e.target)) {
            sidebar.classList.remove('open');
        }
    }
});

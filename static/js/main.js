document.addEventListener('DOMContentLoaded', function () {
    const sidebarCollapse = document.getElementById('sidebarCollapse');
    const sidebar = document.getElementById('sidebar');
    const content = document.getElementById('content');

    if (sidebarCollapse) {
        sidebarCollapse.addEventListener('click', function () {
            // Toggle classes for desktop and mobile
            sidebar.classList.toggle('collapsed');
            content.classList.toggle('expanded');
            
            // For mobile view (overlay effect)
            if (window.innerWidth <= 992) {
                sidebar.classList.toggle('active');
            }
        });
    }

    // Close sidebar on mobile when clicking outside
    document.addEventListener('click', function (event) {
        if (window.innerWidth <= 992) {
            if (sidebar && !sidebar.contains(event.target) && sidebarCollapse && !sidebarCollapse.contains(event.target) && sidebar.classList.contains('active')) {
                sidebar.classList.remove('active');
            }
        }
    });

    // Logout Notification
    const logoutBtn = document.querySelector('a[href*="logout"]');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function() {
            toastr.info("Signing out of ALKHAMS secure session...");
        });
    }
});

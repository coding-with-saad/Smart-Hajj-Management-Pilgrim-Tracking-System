document.addEventListener('DOMContentLoaded', function() {
    
    // Fetch real data from API
    function fetchDashboardData() {
        fetch('/api/dashboard/stats')
            .then(response => response.json())
            .then(res => {
                if (res.status === 'success') {
                    updateDashboardUI(res.data);
                }
            })
            .catch(error => {
                console.warn('Backend API error, using mock fallback for presentation.');
                toastr.warning("Live statistics unavailable. Using presentation fallback data.");
                const mockStats = {
                    total_pilgrims: 150,
                    total_revenue: 4500000,
                    active_packages: 3,
                    payment_distribution: { paid: 95, partial: 30, pending: 25 }
                };
                updateDashboardUI(mockStats);
            });
    }

    fetchDashboardData();

    function updateDashboardUI(data) {
        // Update Stat Numbers
        document.getElementById('stat-pilgrims').textContent = (data.total_pilgrims || 0).toLocaleString();
        document.getElementById('stat-revenue').textContent = '$' + (data.total_revenue || 0).toLocaleString();
        document.getElementById('stat-packages').textContent = data.active_packages || 0;
        document.getElementById('stat-pending').textContent = (data.payment_distribution.pending + data.payment_distribution.partial) || 0;

        // Render Chart
        const ctx = document.getElementById('paymentChart').getContext('2d');
        
        if (window.myPaymentChart) {
            window.myPaymentChart.destroy();
        }

        window.myPaymentChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Paid', 'Partial', 'Pending'],
                datasets: [{
                    data: [
                        data.payment_distribution.paid,
                        data.payment_distribution.partial,
                        data.payment_distribution.pending
                    ],
                    backgroundColor: ['#198754', '#ffc107', '#dc3545'],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom' }
                }
            }
        });
    }
});

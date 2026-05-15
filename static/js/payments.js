document.addEventListener('DOMContentLoaded', function() {
    const paymentTableBody = document.getElementById('paymentTableBody');

    function fetchPayments() {
        fetch('/api/payments')
            .then(response => response.json())
            .then(res => {
                if (res.status === 'success') {
                    renderPayments(res.data);
                }
            })
            .catch(error => {
                console.error('Error fetching payments:', error);
            });
    }

    function renderPayments(payments) {
        paymentTableBody.innerHTML = '';
        if (payments.length === 0) {
            paymentTableBody.innerHTML = '<tr><td colspan="6" class="text-center">No transactions found</td></tr>';
            return;
        }

        payments.forEach(p => {
            const row = `
                <tr>
                    <td><strong>${p.transaction_id}</strong></td>
                    <td>${p.pilgrim_name}</td>
                    <td class="fw-bold">$${p.amount.toLocaleString()}</td>
                    <td><span class="badge bg-light text-dark border"><i class="fas fa-money-bill-wave me-1"></i> ${p.method}</span></td>
                    <td>${p.date}</td>
                    <td><span class="badge ${getStatusClass(p.status)}">${p.status}</span></td>
                </tr>
            `;
            paymentTableBody.insertAdjacentHTML('beforeend', row);
        });
    }

    function getStatusClass(status) {
        switch(status) {
            case 'Paid': return 'bg-success';
            case 'Partial': return 'bg-warning text-dark';
            case 'Pending': return 'bg-danger';
            default: return 'bg-secondary';
        }
    }

    fetchPayments();
});

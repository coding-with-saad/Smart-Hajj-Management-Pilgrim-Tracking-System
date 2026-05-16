document.addEventListener('DOMContentLoaded', function() {
    const paymentTableBody = document.getElementById('paymentTableBody');
    let allPayments = []; // Cache for lookup

    function fetchPayments() {
        fetch('/api/payments')
            .then(response => response.json())
            .then(res => {
                if (res.status === 'success') {
                    allPayments = res.data;
                    renderPayments(allPayments);
                }
            })
            .catch(error => {
                console.error('Error fetching payments:', error);
            });
    }

    function renderPayments(payments) {
        paymentTableBody.innerHTML = '';
        if (payments.length === 0) {
            paymentTableBody.innerHTML = '<tr><td colspan="6" class="text-center text-muted p-4">No financial records found</td></tr>';
            return;
        }

        payments.forEach(p => {
            const row = `
                <tr>
                    <td class="ps-4"><strong>${p.transaction_id}</strong></td>
                    <td>${p.pilgrim_name}</td>
                    <td class="fw-bold">$${(p.amount || 0).toLocaleString()}</td>
                    <td><span class="badge bg-light text-dark border"><i class="fas fa-money-check-alt me-1 text-primary"></i> ${p.method}</span></td>
                    <td>${p.date || 'Processing'}</td>
                    <td><span class="badge ${getStatusClass(p.status)}">${p.status}</span></td>
                </tr>
            `;
            paymentTableBody.insertAdjacentHTML('beforeend', row);
        });
    }

    // Status Lookup Logic
    const btnLookup = document.getElementById('btnLookup');
    const lookupInput = document.getElementById('lookupName');
    const statusResult = document.getElementById('statusResult');
    const resultStatus = document.getElementById('resultStatus');
    const resultBadge = document.getElementById('resultBadge');
    const statusBox = document.getElementById('statusBox');

    if (btnLookup) {
        btnLookup.addEventListener('click', function() {
            const query = lookupInput.value.toLowerCase().trim();
            if (!query) return;

            const record = allPayments.find(p => p.pilgrim_name.toLowerCase().includes(query));

            statusResult.classList.remove('d-none');
            if (record) {
                resultStatus.textContent = record.pilgrim_name;
                resultBadge.textContent = record.status;
                resultBadge.className = `badge rounded-pill px-3 py-2 mt-2 ${getStatusClass(record.status)}`;
                statusBox.style.background = "#f8fafc";
            } else {
                resultStatus.textContent = "Record Not Found";
                resultBadge.textContent = "N/A";
                resultBadge.className = "badge bg-secondary rounded-pill px-3 py-2 mt-2";
                statusBox.style.background = "#fff1f2";
            }
        });
    }

    function getStatusClass(status) {
        switch(status) {
            case 'Paid': 
            case 'Fully Paid': return 'bg-success';
            case 'Partial': 
            case 'Partial Payment': return 'bg-warning text-dark';
            case 'Pending': 
            case 'Payment Pending': return 'bg-danger';
            default: return 'bg-secondary';
        }
    }

    fetchPayments();
});

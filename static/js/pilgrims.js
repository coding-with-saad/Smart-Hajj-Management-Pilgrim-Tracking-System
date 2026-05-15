document.addEventListener('DOMContentLoaded', function() {
    const pilgrimTableBody = document.getElementById('pilgrimTableBody');
    const searchInput = document.getElementById('pilgrimSearch');
    const packageFilter = document.getElementById('packageFilter');
    const registrationForm = document.getElementById('registrationForm');
    const editForm = document.getElementById('editForm');
    
    let allPilgrims = []; // Local cache for filtering

    // Fetch Pilgrims from API
    function fetchPilgrims() {
        fetch('/api/pilgrims')
            .then(response => response.json())
            .then(res => {
                if (res.status === 'success') {
                    allPilgrims = res.data;
                    renderTable(allPilgrims);
                }
            })
            .catch(error => {
                console.error('Error fetching pilgrims:', error);
                allPilgrims = [
                    { pilgrim_id: 'PIL-001', name: 'Malik Saad Khawar', passport: 'AB1234567', package: 'VIP', status: 'Paid' }
                ];
                renderTable(allPilgrims);
            });
    }

    fetchPilgrims();

    // Filter Logic
    function filterPilgrims() {
        const query = searchInput.value.toLowerCase();
        const pkg = packageFilter.value;

        const filtered = allPilgrims.filter(p => {
            const name = p.name || "";
            const passport = p.passport || "";
            const id = p.pilgrim_id || "";
            
            const matchesSearch = name.toLowerCase().includes(query) || 
                                  passport.toLowerCase().includes(query) ||
                                  id.toLowerCase().includes(query);
            const matchesPackage = pkg === "" || p.package === pkg;
            return matchesSearch && matchesPackage;
        });

        renderTable(filtered);
    }

    searchInput.addEventListener('input', filterPilgrims);
    packageFilter.addEventListener('change', filterPilgrims);

    function renderTable(data) {
        pilgrimTableBody.innerHTML = '';
        if (data.length === 0) {
            pilgrimTableBody.innerHTML = '<tr><td colspan="6" class="text-center text-muted">No pilgrims found</td></tr>';
            return;
        }
        data.forEach(p => {
            const row = `
                <tr>
                    <td><strong>${p.pilgrim_id}</strong></td>
                    <td>${p.name}</td>
                    <td>${p.passport}</td>
                    <td><span class="badge bg-info text-dark">${p.package || 'N/A'}</span></td>
                    <td><span class="badge ${getStatusClass(p.status || 'Pending')}">${p.status || 'Pending'}</span></td>
                    <td class="text-end">
                        <div class="btn-group btn-group-sm">
                            <a href="/qr_details/${p.pilgrim_id}" class="btn btn-outline-secondary" title="View QR"><i class="fas fa-qrcode"></i></a>
                            <button class="btn btn-outline-primary" title="Edit" onclick="openEditModal('${p.pilgrim_id}')"><i class="fas fa-edit"></i></button>
                            <button class="btn btn-outline-danger" title="Delete" onclick="deletePilgrim('${p.pilgrim_id}')"><i class="fas fa-trash"></i></button>
                        </div>
                    </td>
                </tr>
            `;
            pilgrimTableBody.insertAdjacentHTML('beforeend', row);
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

    // Registration Form
    if (registrationForm) {
        registrationForm.addEventListener('submit', function (event) {
            event.preventDefault();
            if (!registrationForm.checkValidity()) {
                event.stopPropagation();
                registrationForm.classList.add('was-validated');
                return;
            }

            const formData = {
                name: document.getElementById('fullName').value,
                passport: document.getElementById('passportNumber').value,
                cnic: document.getElementById('cnicNumber').value,
                package: document.getElementById('packageType').value,
                contact: document.getElementById('contactNumber').value,
                status: "Pending"
            };

            fetch('/api/pilgrims', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(res => {
                if (res.status === 'success') {
                    const modal = bootstrap.Modal.getInstance(document.getElementById('registrationModal'));
                    modal.hide();
                    registrationForm.reset();
                    registrationForm.classList.remove('was-validated');
                    fetchPilgrims();
                } else {
                    alert('Error: ' + res.message);
                }
            });
        });
    }

    // Edit Form Logic
    window.openEditModal = function(id) {
        const pilgrim = allPilgrims.find(p => p.pilgrim_id === id);
        if (!pilgrim) return;

        document.getElementById('editPilgrimId').value = id;
        document.getElementById('editFullName').value = pilgrim.name || '';
        document.getElementById('editPassportNumber').value = pilgrim.passport || '';
        document.getElementById('editPackageType').value = pilgrim.package || '';
        document.getElementById('editContactNumber').value = pilgrim.contact || '';
        document.getElementById('editStatus').value = pilgrim.status || 'Pending';

        const editModal = new bootstrap.Modal(document.getElementById('editModal'));
        editModal.show();
    };

    if (editForm) {
        editForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const id = document.getElementById('editPilgrimId').value;
            
            const updatedData = {
                name: document.getElementById('editFullName').value,
                passport: document.getElementById('editPassportNumber').value,
                package: document.getElementById('editPackageType').value,
                contact: document.getElementById('editContactNumber').value,
                status: document.getElementById('editStatus').value
            };

            fetch(`/api/pilgrims/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(updatedData)
            })
            .then(response => response.json())
            .then(res => {
                if (res.status === 'success') {
                    const modal = bootstrap.Modal.getInstance(document.getElementById('editModal'));
                    modal.hide();
                    fetchPilgrims();
                    alert('Pilgrim updated successfully!');
                } else {
                    alert('Error: ' + res.message);
                }
            });
        });
    }

    window.deletePilgrim = function(id) {
        if (confirm('Are you sure you want to delete this pilgrim?')) {
            fetch(`/api/pilgrims/${id}`, { method: 'DELETE' })
                .then(response => response.json())
                .then(res => {
                    if (res.status === 'success') {
                        fetchPilgrims();
                    }
                });
        }
    };
});

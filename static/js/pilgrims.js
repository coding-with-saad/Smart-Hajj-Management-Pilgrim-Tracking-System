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
                allPilgrims = [];
                renderTable(allPilgrims);
                toastr.error("Failed to connect to the database.");
            });
    }

    fetchPilgrims();

    // URL Parameter Detection for Discount (Appeal Flow)
    const urlParams = new URLSearchParams(window.location.search);
    const dtype = urlParams.get('dtype');
    const dval = urlParams.get('dval');
    const pilgrimName = urlParams.get('name');
    const gsize = parseInt(urlParams.get('gsize')) || 1;

    if (dtype && dval) {
        document.getElementById('discountBanner').classList.remove('d-none');
        document.getElementById('priceSummary').classList.remove('d-none');
        
        const bannerText = document.querySelector('#discountBanner p');
        if (dtype === 'percent') {
            bannerText.textContent = `Your registration is flagged for a ${dval}% reduction.`;
        } else if (dtype === 'flat') {
            bannerText.textContent = `Your registration is flagged for a $${dval} reduction.`;
        } else if (dtype === 'group') {
            bannerText.textContent = `Group Discount Applied: $${dval} off for the total group of ${gsize}.`;
            document.getElementById('groupInfo').classList.remove('d-none');
            document.getElementById('groupSizeValue').textContent = gsize;
        }

        if (pilgrimName) {
            document.getElementById('fullName').value = decodeURIComponent(pilgrimName);
            const registrationModal = new bootstrap.Modal(document.getElementById('registrationModal'));
            registrationModal.show();
            toastr.info("Discount parameters applied automatically.");
        }
    }

    // Toggle Deposit field based on status (Registration)
    const regStatus = document.getElementById('regStatus');
    const depositContainer = document.getElementById('depositContainer');
    if (regStatus) {
        regStatus.addEventListener('change', function() {
            if (this.value === 'Partial Payment') {
                depositContainer.classList.remove('d-none');
                document.getElementById('initialDeposit').setAttribute('required', 'required');
            } else {
                depositContainer.classList.add('d-none');
                document.getElementById('initialDeposit').removeAttribute('required');
            }
        });
    }

    // Toggle Deposit field based on status (Edit)
    const editStatus = document.getElementById('editStatus');
    const editDepositContainer = document.getElementById('editDepositContainer');
    if (editStatus) {
        editStatus.addEventListener('change', function() {
            if (this.value === 'Partial Payment') {
                editDepositContainer.classList.remove('d-none');
            } else {
                editDepositContainer.classList.add('d-none');
            }
        });
    }

    // Dynamic Price Calculation
    const packageTypeSelect = document.getElementById('packageType');
    const prices = {
        "Social (Low Income)": 1500,
        "Economy": 3000,
        "VIP": 7500,
        "Premium": 12000
    };

    function calculateFinalPrice() {
        const selectedPackage = packageTypeSelect.value;
        const basePrice = prices[selectedPackage] || 0;
        const totalBasePrice = basePrice * gsize;
        
        let discountAmt = 0;
        if (dtype === 'percent') {
            discountAmt = (totalBasePrice * parseInt(dval)) / 100;
        } else if (dtype === 'flat' || dtype === 'group') {
            discountAmt = parseInt(dval);
        }

        const finalAmt = Math.max(0, totalBasePrice - discountAmt);

        document.getElementById('originalPrice').textContent = `$${totalBasePrice.toLocaleString()}`;
        document.getElementById('discountAmount').textContent = `-$${discountAmt.toLocaleString()}`;
        document.getElementById('finalPrice').textContent = `$${finalAmt.toLocaleString()}`;
    }

    if (packageTypeSelect) {
        packageTypeSelect.addEventListener('change', calculateFinalPrice);
    }

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
    
    // Add 'Enter' key support for search
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            filterPilgrims();
            toastr.info("Search results updated.");
        }
    });

    function renderTable(data) {
        pilgrimTableBody.innerHTML = '';
        if (data.length === 0) {
            pilgrimTableBody.innerHTML = '<tr><td colspan="6" class="text-center text-muted p-4">No pilgrims found in directory</td></tr>';
            return;
        }
        data.forEach(p => {
            const row = `
                <tr>
                    <td class="ps-4"><strong>${p.pilgrim_id}</strong></td>
                    <td>${p.name}</td>
                    <td>${p.passport}</td>
                    <td><span class="badge bg-light text-dark border">${p.package || 'N/A'}</span></td>
                    <td><span class="badge ${getStatusClass(p.status || 'Pending')}">${p.status || 'Pending'}</span></td>
                    <td class="text-end pe-4">
                        <div class="d-flex justify-content-end gap-2">
                            <a href="/qr_details/${p.pilgrim_id}" class="btn-action bg-light text-secondary" title="View Digital Pass"><i class="fas fa-qrcode"></i></a>
                            <button class="btn-action bg-light text-primary" title="Update Record" onclick="openEditModal('${p.pilgrim_id}')"><i class="fas fa-edit"></i></button>
                            <button class="btn-action bg-light text-danger" title="Remove Pilgrim" onclick="deletePilgrim('${p.pilgrim_id}')"><i class="fas fa-trash"></i></button>
                        </div>
                    </td>
                </tr>
            `;
            pilgrimTableBody.insertAdjacentHTML('beforeend', row);
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
                status: document.getElementById('regStatus').value,
                initial_deposit: document.getElementById('initialDeposit').value || 0,
                group_size: gsize,
                discount_type: dtype || 'none',
                discount_value: dval ? parseInt(dval) : 0
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
                    window.history.replaceState({}, document.title, window.location.pathname);
                    fetchPilgrims();
                    toastr.success(`Pilgrim "${formData.name}" registered. Initial financial records created.`);
                } else {
                    toastr.error(res.message);
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
        
        // Handle deposit field visibility and value
        const deposit = pilgrim.initial_deposit || 0;
        document.getElementById('editInitialDeposit').value = deposit;
        if (pilgrim.status === 'Partial Payment') {
            editDepositContainer.classList.remove('d-none');
        } else {
            editDepositContainer.classList.add('d-none');
        }

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
                status: document.getElementById('editStatus').value,
                initial_deposit: document.getElementById('editInitialDeposit').value || 0
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
                    toastr.success(`Records for pilgrim ID ${id} updated.`);
                } else {
                    toastr.error(`Error: ${res.message}`);
                }
            });
        });
    }

    window.deletePilgrim = function(id) {
        if (confirm(`Are you sure you want to permanently delete Pilgrim ${id}?`)) {
            fetch(`/api/pilgrims/${id}`, { method: 'DELETE' })
                .then(response => response.json())
                .then(res => {
                    if (res.status === 'success') {
                        fetchPilgrims();
                        toastr.warning(`Pilgrim ${id} removed.`);
                    } else {
                        toastr.error("Failed to delete record.");
                    }
                });
        }
    };
});

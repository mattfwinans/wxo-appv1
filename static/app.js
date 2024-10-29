document.addEventListener('DOMContentLoaded', loadVendors);

function loadVendors() {
    fetch('/api/vendors')
        .then(response => response.json())
        .then(data => {
            const vendorList = document.getElementById('vendors-list');
            vendorList.innerHTML = '';
            data.forEach(vendor => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${vendor.id}</td>
                    <td>${vendor.vendor}</td>
                    <td>${vendor.price}</td>
                    <td>${vendor.date}</td>
                    <td>
                        <button onclick="deleteVendor(${vendor.id})">Delete</button>
                    </td>
                `;
                vendorList.appendChild(row);
            });
        });
}

function addVendor() {
    const vendor = document.getElementById('vendor').value;
    const price = document.getElementById('price').value;
    const date = document.getElementById('date').value;

    fetch('/api/vendors', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ vendor, price, date })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        loadVendors();
    });
}

function deleteVendor(id) {
    fetch(`/api/vendors/${id}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        loadVendors();
    });
}
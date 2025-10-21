// static/js/billing.js
document.addEventListener('DOMContentLoaded', function() {
    console.log('Billing page loaded');
    
    // Get all elements
    const customerMobile = document.getElementById('customerMobile');
    const customerName = document.getElementById('customerName');
    const customerEmail = document.getElementById('customerEmail');
    const customerId = document.getElementById('customerId');
    const checkCustomerBtn = document.getElementById('checkCustomer');
    const serviceCategory = document.getElementById('serviceCategory');
    const serviceItem = document.getElementById('serviceItem');
    const serviceQuantity = document.getElementById('serviceQuantity');
    const addServiceBtn = document.getElementById('addService');
    const servicesList = document.getElementById('servicesList');
    const noServicesMessage = document.getElementById('noServicesMessage');
    const generateBillBtn = document.getElementById('generateBill');
    const downloadPdfBtn = document.getElementById('downloadPdf');
    const shareWhatsAppBtn = document.getElementById('shareWhatsApp');
    const newBillBtn = document.getElementById('newBill');
    const billActions = document.getElementById('billActions');
    const billSuccess = document.getElementById('billSuccess');
    const billNumber = document.getElementById('billNumber');

    // Summary elements
    const subtotalEl = document.getElementById('subtotal');
    const taxAmountEl = document.getElementById('taxAmount');
    const discountAmountEl = document.getElementById('discountAmount');
    const totalAmountEl = document.getElementById('totalAmount');

    // State
    let selectedServices = [];
    let currentBillId = null;

    // Initialize event listeners
    initializeEventListeners();

    function initializeEventListeners() {
        console.log('Initializing event listeners');
        
        // Check Customer button
        if (checkCustomerBtn) {
            checkCustomerBtn.addEventListener('click', checkCustomer);
        }

        // Service Category change
        if (serviceCategory) {
            serviceCategory.addEventListener('change', loadServicesByCategory);
        }

        // Add Service button
        if (addServiceBtn) {
            addServiceBtn.addEventListener('click', addService);
        }

        // Generate Bill button
        if (generateBillBtn) {
            generateBillBtn.addEventListener('click', generateBill);
        }

        // New Bill button
        if (newBillBtn) {
            newBillBtn.addEventListener('click', resetForm);
        }

        // Real-time validation
        if (customerMobile) {
            customerMobile.addEventListener('input', updateGenerateBillButton);
        }
        if (customerName) {
            customerName.addEventListener('input', updateGenerateBillButton);
        }
    }

    function loadServicesByCategory() {
        const categoryId = serviceCategory.value;
        console.log('Category changed:', categoryId);
        
        // Clear service dropdown
        serviceItem.innerHTML = '<option value="">Select Service</option>';
        
        if (!categoryId) {
            addServiceBtn.disabled = true;
            return;
        }

        // Show loading
        const loadingSpinner = document.getElementById('serviceLoading');
        if (loadingSpinner) {
            loadingSpinner.style.display = 'block';
        }
        addServiceBtn.disabled = true;

        // Fetch services from API
        fetch(`/billing/get-services/?category_id=${categoryId}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('Services loaded:', data);
                
                if (data.services && data.services.length > 0) {
                    data.services.forEach(service => {
                        const option = document.createElement('option');
                        option.value = service.id;
                        option.textContent = `${service.name} - ₹${service.price}`;
                        option.setAttribute('data-price', service.price);
                        option.setAttribute('data-name', service.name);
                        serviceItem.appendChild(option);
                    });
                    addServiceBtn.disabled = false;
                    showToast('Services loaded successfully', 'success');
                } else {
                    const option = document.createElement('option');
                    option.value = '';
                    option.textContent = 'No services found in this category';
                    serviceItem.appendChild(option);
                    addServiceBtn.disabled = true;
                    showToast('No services found in this category', 'warning');
                }
            })
            .catch(error => {
                console.error('Error loading services:', error);
                const option = document.createElement('option');
                option.value = '';
                option.textContent = 'Error loading services';
                serviceItem.appendChild(option);
                showToast('Error loading services. Please try again.', 'error');
            })
            .finally(() => {
                if (loadingSpinner) {
                    loadingSpinner.style.display = 'none';
                }
            });
    }

    function checkCustomer() {
        const mobile = customerMobile.value.trim();
        
        if (!mobile) {
            alert('Please enter mobile number');
            return;
        }

        if (mobile.length !== 10) {
            alert('Please enter a valid 10-digit mobile number');
            return;
        }

        checkCustomerBtn.disabled = true;
        checkCustomerBtn.innerHTML = 'Checking...';

        const formData = new FormData();
        formData.append('mobile', mobile);

        fetch('/billing/get-customer-info/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken()
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log('Customer check response:', data);
            
            if (data.exists) {
                customerName.value = data.name;
                customerEmail.value = data.email || '';
                customerId.value = data.id;
                checkCustomerBtn.innerHTML = 'Customer Found ✓';
                checkCustomerBtn.classList.remove('btn-outline-primary');
                checkCustomerBtn.classList.add('btn-success');
                showToast('Customer found!', 'success');
            } else {
                customerName.value = '';
                customerEmail.value = '';
                customerId.value = '';
                customerName.focus();
                checkCustomerBtn.innerHTML = 'New Customer';
                checkCustomerBtn.classList.remove('btn-outline-primary', 'btn-success');
                checkCustomerBtn.classList.add('btn-warning');
                showToast('New customer - please fill details', 'info');
            }
            updateGenerateBillButton();
        })
        .catch(error => {
            console.error('Error checking customer:', error);
            alert('Error checking customer information');
            checkCustomerBtn.innerHTML = 'Check Customer';
            checkCustomerBtn.classList.remove('btn-success', 'btn-warning');
            checkCustomerBtn.classList.add('btn-outline-primary');
        })
        .finally(() => {
            checkCustomerBtn.disabled = false;
        });
    }

    function addService() {
        const serviceId = serviceItem.value;
        const quantity = parseInt(serviceQuantity.value) || 1;
        
        if (!serviceId) {
            alert('Please select a service');
            return;
        }

        const selectedOption = serviceItem.options[serviceItem.selectedIndex];
        const serviceName = selectedOption.getAttribute('data-name');
        const price = parseFloat(selectedOption.getAttribute('data-price'));

        // Check if service already exists
        const existingIndex = selectedServices.findIndex(s => s.id == serviceId);
        
        if (existingIndex > -1) {
            // Update quantity
            selectedServices[existingIndex].quantity += quantity;
            showToast(`Updated ${serviceName} quantity to ${selectedServices[existingIndex].quantity}`, 'info');
        } else {
            // Add new service
            selectedServices.push({
                id: parseInt(serviceId),
                name: serviceName,
                price: price,
                quantity: quantity
            });
            showToast(`Added ${serviceName}`, 'success');
        }

        updateServicesList();
        updateBillingSummary();
        updateGenerateBillButton();

        // Reset service selection
        serviceItem.value = '';
        serviceQuantity.value = 1;
    }

    function updateServicesList() {
        servicesList.innerHTML = '';

        if (selectedServices.length === 0) {
            noServicesMessage.classList.remove('d-none');
            servicesList.appendChild(noServicesMessage);
            return;
        }

        noServicesMessage.classList.add('d-none');

        selectedServices.forEach((service, index) => {
            const serviceElement = document.createElement('div');
            serviceElement.className = 'service-item';
            serviceElement.innerHTML = `
                <div class="service-info">
                    <div class="service-name">${service.name}</div>
                    <div class="service-details">₹${service.price} × ${service.quantity}</div>
                </div>
                <div class="service-total">₹${(service.price * service.quantity).toFixed(2)}</div>
                <button class="remove-service" data-index="${index}">
                    <i class="fa fa-times"></i>
                </button>
            `;
            servicesList.appendChild(serviceElement);
        });

        // Add remove event listeners
        document.querySelectorAll('.remove-service').forEach(button => {
            button.addEventListener('click', function() {
                const index = parseInt(this.getAttribute('data-index'));
                removeService(index);
            });
        });
    }

    function removeService(index) {
        const removedService = selectedServices[index];
        selectedServices.splice(index, 1);
        updateServicesList();
        updateBillingSummary();
        updateGenerateBillButton();
        showToast(`Removed ${removedService.name}`, 'warning');
    }

    function updateBillingSummary() {
        const subtotal = selectedServices.reduce((total, service) => {
            return total + (service.price * service.quantity);
        }, 0);

        const taxAmount = subtotal * 0.05;
        const discount = 0;
        const totalAmount = subtotal + taxAmount - discount;

        subtotalEl.textContent = `₹${subtotal.toFixed(2)}`;
        taxAmountEl.textContent = `₹${taxAmount.toFixed(2)}`;
        discountAmountEl.textContent = `₹${discount.toFixed(2)}`;
        totalAmountEl.textContent = `₹${totalAmount.toFixed(2)}`;
    }

    function updateGenerateBillButton() {
        const hasCustomer = customerName.value.trim() && customerMobile.value.trim();
        const hasServices = selectedServices.length > 0;
        
        generateBillBtn.disabled = !(hasCustomer && hasServices);
    }

    function saveCustomer() {
        const name = customerName.value.trim();
        const email = customerEmail.value.trim();
        const mobile = customerMobile.value.trim();

        if (!name || !mobile) {
            return Promise.reject('Please enter customer name and mobile number');
        }

        const formData = new FormData();
        formData.append('name', name);
        formData.append('email', email);
        formData.append('mobile', mobile);

        return fetch('/billing/save-customer/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken()
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                customerId.value = data.customer_id;
                return data.customer_id;
            } else {
                throw new Error(data.error || 'Failed to save customer');
            }
        });
    }

    function generateBill() {
        console.log('Generating bill...');
        
        // First save customer if needed
        if (!customerId.value) {
            saveCustomer()
                .then(customerId => generateBillWithCustomer(customerId))
                .catch(error => alert(error));
        } else {
            generateBillWithCustomer(customerId.value);
        }
    }

    function generateBillWithCustomer(customerId) {
        if (selectedServices.length === 0) {
            alert('Please add at least one service');
            return;
        }

        const billData = {
            customer_id: parseInt(customerId),
            services: selectedServices,
            discount: 0
        };

        console.log('Sending bill data:', billData);

        generateBillBtn.disabled = true;
        generateBillBtn.innerHTML = 'Generating Bill...';

        fetch('/billing/generate-bill/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify(billData)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Bill generation response:', data);
            
            if (data.success) {
                currentBillId = data.bill_id;
                billNumber.textContent = `Bill Number: ${data.bill_number}`;
                billSuccess.classList.remove('d-none');
                billActions.classList.remove('d-none');
                generateBillBtn.classList.add('d-none');
                
                showToast('Bill generated successfully!', 'success');

                // Set up download and share buttons
                downloadPdfBtn.onclick = () => {
                    window.open(`/billing/download-pdf/${currentBillId}/`, '_blank');
                };

                shareWhatsAppBtn.onclick = () => {
                    shareViaWhatsApp(currentBillId);
                };
            } else {
                throw new Error(data.error || 'Failed to generate bill');
            }
        })
        .catch(error => {
            console.error('Error generating bill:', error);
            alert('Error: ' + error.message);
        })
        .finally(() => {
            generateBillBtn.disabled = false;
            generateBillBtn.innerHTML = 'Generate Bill';
        });
    }

    function shareViaWhatsApp(billId) {
        fetch(`/billing/share-whatsapp/${billId}/`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.open(data.whatsapp_url, '_blank');
                } else {
                    throw new Error(data.error || 'Failed to share via WhatsApp');
                }
            })
            .catch(error => {
                console.error('Error sharing via WhatsApp:', error);
                alert('Error sharing via WhatsApp: ' + error.message);
            });
    }

    function resetForm() {
        // Reset all form fields
        customerMobile.value = '';
        customerName.value = '';
        customerEmail.value = '';
        customerId.value = '';
        selectedServices = [];
        currentBillId = null;
        serviceCategory.value = '';
        serviceItem.innerHTML = '<option value="">Select Service</option>';
        serviceQuantity.value = '1';

        // Reset buttons
        checkCustomerBtn.innerHTML = 'Check Customer';
        checkCustomerBtn.classList.remove('btn-warning', 'btn-success');
        checkCustomerBtn.classList.add('btn-outline-primary');

        // Hide success message and actions
        billSuccess.classList.add('d-none');
        billActions.classList.add('d-none');
        generateBillBtn.classList.remove('d-none');

        // Update UI
        updateServicesList();
        updateBillingSummary();
        updateGenerateBillButton();

        showToast('Form reset successfully', 'info');
    }

    function showToast(message, type = 'info') {
        // Create a simple toast notification
        const toast = document.createElement('div');
        toast.className = `alert alert-${type} alert-dismissible fade show`;
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            min-width: 250px;
        `;
        toast.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(toast);
        
        // Auto remove after 3 seconds
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 3000);
    }

    function getCSRFToken() {
        const name = 'csrftoken';
        let cookieValue = null;
        
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Initial setup
    updateGenerateBillButton();
    console.log('Billing system initialized successfully');
});
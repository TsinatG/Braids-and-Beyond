// Booking functionality for the Hair Salon website

document.addEventListener('DOMContentLoaded', function() {
    // Get form elements
    const serviceSelect = document.getElementById('service');
    const stylistSelect = document.getElementById('stylist');
    const dateInput = document.getElementById('date');
    const timeInput = document.getElementById('time');
    
    // Initialize date picker if available
    if (dateInput) {
        // Set minimum date to today
        const today = new Date();
        const yyyy = today.getFullYear();
        const mm = String(today.getMonth() + 1).padStart(2, '0');
        const dd = String(today.getDate()).padStart(2, '0');
        const formattedDate = `${yyyy}-${mm}-${dd}`;
        dateInput.setAttribute('min', formattedDate);
        
        // If using Bootstrap Datepicker (optional)
        if (typeof $.fn.datepicker !== 'undefined') {
            $(dateInput).datepicker({
                format: 'yyyy-mm-dd',
                startDate: 'today',
                autoclose: true
            });
        }
    }
    
    // Service selection
    const serviceCards = document.querySelectorAll('.service-card');
    serviceCards.forEach(card => {
        card.addEventListener('click', function() {
            // Remove active class from all cards
            serviceCards.forEach(c => c.classList.remove('active', 'border-primary'));
            
            // Add active class to selected card
            this.classList.add('active', 'border-primary');
            
            // Update hidden input or select
            if (serviceSelect) {
                serviceSelect.value = this.dataset.serviceId;
            }
            
            // Update summary
            const serviceSummary = document.getElementById('selected-service');
            if (serviceSummary) {
                const serviceName = this.querySelector('h3').textContent;
                serviceSummary.querySelector('span').textContent = serviceName;
            }
            
            checkBookingEligibility();
        });
    });
    
    // Stylist selection
    const stylistCards = document.querySelectorAll('.stylist-card');
    stylistCards.forEach(card => {
        card.addEventListener('click', function() {
            // Remove active class from all cards
            stylistCards.forEach(c => c.classList.remove('active', 'border-primary'));
            
            // Add active class to selected card
            this.classList.add('active', 'border-primary');
            
            // Update hidden input or select
            if (stylistSelect) {
                stylistSelect.value = this.dataset.stylistId;
            }
            
            // Update summary
            const stylistSummary = document.getElementById('selected-stylist');
            if (stylistSummary) {
                const stylistName = this.querySelector('h3').textContent;
                stylistSummary.querySelector('span').textContent = stylistName;
            }
            
            checkBookingEligibility();
        });
    });
    
    // Date selection
    if (dateInput) {
        dateInput.addEventListener('change', function() {
            // Update summary
            const dateSummary = document.getElementById('selected-date');
            if (dateSummary) {
                dateSummary.querySelector('span').textContent = this.value;
            }
            
            // If a stylist is selected, fetch available times
            if (stylistSelect && stylistSelect.value) {
                fetchAvailableTimes(this.value, stylistSelect.value);
            }
            
            checkBookingEligibility();
        });
    }
    
    // Time selection
    if (timeInput) {
        timeInput.addEventListener('change', function() {
            // Update summary
            const timeSummary = document.getElementById('selected-time');
            if (timeSummary) {
                timeSummary.querySelector('span').textContent = this.value;
            }
            
            checkBookingEligibility();
        });
    }
    
    // Fetch available times based on date and stylist
    function fetchAvailableTimes(date, stylistId) {
        const timeSlots = document.getElementById('time-slots-container');
        if (!timeSlots) return;
        
        timeSlots.innerHTML = '<div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div>';
        
        fetch(`/available_times?date=${date}&stylist_id=${stylistId}`)
            .then(response => response.json())
            .then(data => {
                timeSlots.innerHTML = '';
                
                if (data.times.length === 0) {
                    timeSlots.innerHTML = '<p class="text-center">No available times for this date</p>';
                    return;
                }
                
                const timeButtonsContainer = document.createElement('div');
                timeButtonsContainer.className = 'time-buttons d-flex flex-wrap gap-2';
                
                data.times.forEach(time => {
                    const button = document.createElement('button');
                    button.type = 'button';
                    button.className = 'btn btn-outline-primary time-button';
                    button.textContent = time;
                    button.dataset.time = time;
                    
                    button.addEventListener('click', function() {
                        // Remove active class from all time buttons
                        document.querySelectorAll('.time-button').forEach(btn => {
                            btn.classList.remove('active');
                        });
                        
                        // Add active class to selected button
                        this.classList.add('active');
                        
                        // Update hidden input
                        if (timeInput) {
                            timeInput.value = this.dataset.time;
                            
                            // Trigger change event
                            const event = new Event('change');
                            timeInput.dispatchEvent(event);
                        }
                    });
                    
                    timeButtonsContainer.appendChild(button);
                });
                
                timeSlots.appendChild(timeButtonsContainer);
            })
            .catch(error => {
                console.error('Error fetching available times:', error);
                timeSlots.innerHTML = '<p class="text-center text-danger">Error loading available times</p>';
            });
    }
    
    // Check if all required fields are filled to enable booking button
    function checkBookingEligibility() {
        const continueButton = document.getElementById('continue-booking');
        if (!continueButton) return;
        
        const serviceSelected = serviceSelect && serviceSelect.value;
        const stylistSelected = stylistSelect && stylistSelect.value;
        const dateSelected = dateInput && dateInput.value;
        const timeSelected = timeInput && timeInput.value;
        
        if (serviceSelected && stylistSelected && dateSelected && timeSelected) {
            continueButton.classList.remove('disabled');
            continueButton.classList.add('btn-primary');
            continueButton.classList.remove('btn-secondary');
        } else {
            continueButton.classList.add('disabled');
            continueButton.classList.remove('btn-primary');
            continueButton.classList.add('btn-secondary');
        }
    }
    
    // Form validation
    const bookingForm = document.querySelector('form');
    if (bookingForm) {
        bookingForm.addEventListener('submit', function(event) {
            let isValid = true;
            
            // Check if service is selected
            if (serviceSelect && serviceSelect.value === '') {
                isValid = false;
                showError(serviceSelect, 'Please select a service');
            }
            
            // Check if stylist is selected
            if (stylistSelect && stylistSelect.value === '') {
                isValid = false;
                showError(stylistSelect, 'Please select a stylist');
            }
            
            // Check if date is selected
            if (dateInput && dateInput.value === '') {
                isValid = false;
                showError(dateInput, 'Please select a date');
            }
            
            // Check if time is selected
            if (timeInput && timeInput.value === '') {
                isValid = false;
                showError(timeInput, 'Please select a time');
            }
            
            if (!isValid) {
                event.preventDefault();
            }
        });
    }
    
    // Helper function to show error
    function showError(element, message) {
        // Remove any existing error message
        const existingError = element.nextElementSibling;
        if (existingError && existingError.classList.contains('invalid-feedback')) {
            existingError.remove();
        }
        
        // Add Bootstrap validation classes
        element.classList.add('is-invalid');
        
        // Create error message
        const errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback';
        errorDiv.textContent = message;
        
        // Insert after the element
        element.parentNode.insertBefore(errorDiv, element.nextSibling);
        
        // Remove error after 3 seconds
        setTimeout(() => {
            element.classList.remove('is-invalid');
            if (errorDiv.parentNode) {
            errorDiv.remove();
            }
        }, 3000);
    }
}); 
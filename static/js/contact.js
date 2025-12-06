// Contact page specific functionality
class ContactPageManager {
    constructor() {
        this.form = document.getElementById('contact-form');
        this.faqItems = document.querySelectorAll('.faq-item');
        this.mapElement = document.getElementById('map-container');
        this.init();
    }
    
    init() {
        if (this.form) {
            this.setupContactForm();
        }
        
        if (this.faqItems.length > 0) {
            this.setupFAQ();
        }
        
        if (this.mapElement) {
            this.setupMap();
        }
        
        this.setupDepartmentContacts();
        this.setupCharacterCounter();
    }
    
    setupContactForm() {
        const formHandler = new FormHandler('contact-form');
        
        // Add custom validation
        this.form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            // Get form data
            const formData = new FormData(this.form);
            const data = Object.fromEntries(formData);
            
            // Additional validation
            if (!this.validateContactForm(data)) {
                return;
            }
            
            // Show loading
            const submitBtn = this.form.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i> Sending...';
            submitBtn.disabled = true;
            
            try {
                const response = await fetch(this.form.action, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': this.getCSRFToken(),
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                    body: formData
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    showNotification('Message sent successfully! We\'ll get back to you soon.', 'success');
                    this.form.reset();
                    
                    // Reset character counter
                    const messageField = this.form.querySelector('textarea[name="message"]');
                    if (messageField) {
                        this.updateCharacterCounter(messageField);
                    }
                } else {
                    showNotification(result.error || 'Failed to send message. Please try again.', 'error');
                    
                    // Show field errors
                    if (result.errors) {
                        Object.entries(result.errors).forEach(([field, error]) => {
                            const fieldElement = this.form.querySelector(`[name="${field}"]`);
                            if (fieldElement) {
                                this.showFieldError(fieldElement, error);
                            }
                        });
                    }
                }
            } catch (error) {
                showNotification('Network error. Please check your connection.', 'error');
            } finally {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }
        });
    }
    
    validateContactForm(data) {
        let isValid = true;
        
        // Name validation
        if (!data.name || data.name.trim().length < 2) {
            this.showFieldError(this.form.querySelector('[name="name"]'), 'Please enter your full name');
            isValid = false;
        }
        
        // Email validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!data.email || !emailRegex.test(data.email)) {
            this.showFieldError(this.form.querySelector('[name="email"]'), 'Please enter a valid email address');
            isValid = false;
        }
        
        // Message validation
        if (!data.message || data.message.trim().length < 10) {
            this.showFieldError(this.form.querySelector('[name="message"]'), 'Please enter a message (minimum 10 characters)');
            isValid = false;
        }
        
        return isValid;
    }
    
    showFieldError(field, message) {
        // Clear previous error
        this.clearFieldError(field);
        
        // Add error class
        field.classList.add('border-red-500', 'focus:border-red-500', 'focus:ring-red-500');
        
        // Create error message
        const errorDiv = document.createElement('div');
        errorDiv.className = 'mt-1 text-sm text-red-600 flex items-center';
        errorDiv.innerHTML = `
            <i class="fas fa-exclamation-circle mr-2"></i>
            ${message}
        `;
        
        // Insert after field
        field.parentNode.appendChild(errorDiv);
    }
    
    clearFieldError(field) {
        field.classList.remove('border-red-500', 'focus:border-red-500', 'focus:ring-red-500');
        const errorDiv = field.parentNode.querySelector('.text-red-600');
        if (errorDiv) {
            errorDiv.remove();
        }
    }
    
    setupFAQ() {
        this.faqItems.forEach(item => {
            const question = item.querySelector('.faq-question');
            const answer = item.querySelector('.faq-answer');
            const chevron = item.querySelector('.fa-chevron-down');
            
            if (!question || !answer) return;
            
            question.addEventListener('click', () => {
                const isOpen = answer.classList.contains('max-h-0');
                
                // Close all other FAQs
                this.faqItems.forEach(otherItem => {
                    if (otherItem !== item) {
                        const otherAnswer = otherItem.querySelector('.faq-answer');
                        const otherChevron = otherItem.querySelector('.fa-chevron-down');
                        otherAnswer.classList.add('max-h-0');
                        otherAnswer.classList.remove('max-h-96', 'py-4');
                        if (otherChevron) {
                            otherChevron.classList.remove('rotate-180');
                        }
                    }
                });
                
                // Toggle current FAQ
                if (isOpen) {
                    answer.classList.remove('max-h-0');
                    answer.classList.add('max-h-96', 'py-4');
                    if (chevron) {
                        chevron.classList.add('rotate-180');
                    }
                } else {
                    answer.classList.add('max-h-0');
                    answer.classList.remove('max-h-96', 'py-4');
                    if (chevron) {
                        chevron.classList.remove('rotate-180');
                    }
                }
            });
        });
    }
    
    setupMap() {
        // Placeholder for Google Maps integration
        // You'll need to add your Google Maps API key
        this.mapElement.innerHTML = `
            <div class="w-full h-full bg-gradient-to-br from-sky-100 to-sky-200 rounded-xl flex items-center justify-center">
                <div class="text-center p-8">
                    <i class="fas fa-map-marker-alt text-5xl text-sky-600 mb-4"></i>
                    <h3 class="text-xl font-bold text-slate-800 mb-2">Our Location</h3>
                    <p class="text-slate-600 mb-4">Addis Ababa, Ethiopia</p>
                    <a href="https://maps.google.com/?q=Addis+Ababa,Ethiopia" 
                       target="_blank"
                       class="inline-flex items-center bg-sky-600 hover:bg-sky-700 text-white px-6 py-3 rounded-lg font-semibold transition duration-300">
                        <i class="fas fa-directions mr-2"></i>
                        Get Directions
                    </a>
                </div>
            </div>
        `;
        
        // For actual Google Maps integration:
        // 1. Add API key to settings
        // 2. Uncomment and configure:
        /*
        if (typeof google !== 'undefined') {
            const map = new google.maps.Map(this.mapElement, {
                center: { lat: 9.032, lng: 38.746 }, // Addis Ababa coordinates
                zoom: 14,
                styles: [...]
            });
            
            new google.maps.Marker({
                position: { lat: 9.032, lng: 38.746 },
                map: map,
                title: 'EIP Ethiopia'
            });
        }
        */
    }
    
    setupDepartmentContacts() {
        // Make department contact buttons functional
        document.querySelectorAll('.department-contact').forEach(button => {
            button.addEventListener('click', () => {
                const email = button.getAttribute('data-email');
                const subject = button.getAttribute('data-subject') || 'Inquiry';
                
                if (email) {
                    window.location.href = `mailto:${email}?subject=${encodeURIComponent(subject)}`;
                }
            });
        });
    }
    
    setupCharacterCounter() {
        const messageField = this.form?.querySelector('textarea[name="message"]');
        if (!messageField) return;
        
        // Create counter display
        const counter = document.createElement('div');
        counter.className = 'text-sm text-slate-500 mt-1 text-right';
        counter.id = 'character-counter';
        messageField.parentNode.appendChild(counter);
        
        // Update function
        const updateCounter = () => {
            const length = messageField.value.length;
            const maxLength = messageField.maxLength || 1000;
            counter.textContent = `${length}/${maxLength} characters`;
            
            // Change color based on length
            if (length > maxLength * 0.9) {
                counter.classList.add('text-red-500');
                counter.classList.remove('text-slate-500', 'text-sky-600');
            } else if (length > maxLength * 0.7) {
                counter.classList.add('text-sky-600');
                counter.classList.remove('text-slate-500', 'text-red-500');
            } else {
                counter.classList.add('text-slate-500');
                counter.classList.remove('text-red-500', 'text-sky-600');
            }
        };
        
        // Initial update
        updateCounter();
        
        // Update on input
        messageField.addEventListener('input', updateCounter);
        messageField.addEventListener('keyup', updateCounter);
        messageField.addEventListener('change', updateCounter);
    }
    
    getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    }
}

// Initialize contact page
if (document.querySelector('body.contact-page') || window.location.pathname.includes('/contact')) {
    document.addEventListener('DOMContentLoaded', () => {
        window.contactPageManager = new ContactPageManager();
    });
}
// Form handling utilities

class FormHandler {
    constructor(formId) {
        this.form = document.getElementById(formId);
        this.csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
        this.init();
    }
    
    init() {
        if (!this.form) return;
        
        this.form.addEventListener('submit', this.handleSubmit.bind(this));
        this.initValidation();
    }
    
    initValidation() {
        // Add real-time validation
        this.form.querySelectorAll('[data-validate]').forEach(input => {
            input.addEventListener('blur', () => this.validateField(input));
            input.addEventListener('input', () => this.clearError(input));
        });
    }
    
    validateField(field) {
        const value = field.value.trim();
        const type = field.dataset.validate;
        
        let isValid = true;
        let errorMessage = '';
        
        switch(type) {
            case 'email':
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                isValid = emailRegex.test(value);
                errorMessage = 'Please enter a valid email address';
                break;
                
            case 'required':
                isValid = value.length > 0;
                errorMessage = 'This field is required';
                break;
                
            case 'phone':
                const phoneRegex = /^[\d\s\-\+\(\)]{10,}$/;
                isValid = phoneRegex.test(value.replace(/\s/g, ''));
                errorMessage = 'Please enter a valid phone number';
                break;
        }
        
        if (!isValid) {
            this.showFieldError(field, errorMessage);
            return false;
        }
        
        this.clearError(field);
        return true;
    }
    
    showFieldError(field, message) {
        this.clearError(field);
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'mt-1 text-sm text-red-600';
        errorDiv.innerHTML = `<i class="fas fa-exclamation-circle mr-1"></i> ${message}`;
        
        field.classList.add('border-red-500');
        field.parentNode.appendChild(errorDiv);
    }
    
    clearError(field) {
        field.classList.remove('border-red-500');
        const errorDiv = field.parentNode.querySelector('.text-red-600');
        if (errorDiv) {
            errorDiv.remove();
        }
    }
    
    async handleSubmit(e) {
        e.preventDefault();
        
        // Validate all fields
        let isValid = true;
        this.form.querySelectorAll('[data-validate]').forEach(field => {
            if (!this.validateField(field)) {
                isValid = false;
            }
        });
        
        if (!isValid) {
            showNotification('Please fix the errors in the form', 'error');
            return;
        }
        
        // Show loading state
        const submitBtn = this.form.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i> Processing...';
        submitBtn.disabled = true;
        
        try {
            const formData = new FormData(this.form);
            
            const response = await fetch(this.form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            
            const data = await response.json();
            
            if (response.ok) {
                showNotification(data.message || 'Form submitted successfully!', 'success');
                this.form.reset();
            } else {
                showNotification(data.error || 'Submission failed', 'error');
                
                // Show field errors if provided
                if (data.errors) {
                    Object.keys(data.errors).forEach(fieldName => {
                        const field = this.form.querySelector(`[name="${fieldName}"]`);
                        if (field) {
                            this.showFieldError(field, data.errors[fieldName]);
                        }
                    });
                }
            }
        } catch (error) {
            showNotification('Network error. Please try again.', 'error');
        } finally {
            // Reset button
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }
    }
}

// Initialize form handlers
document.addEventListener('DOMContentLoaded', function() {
    // Initialize contact form
    if (document.getElementById('contact-form')) {
        new FormHandler('contact-form');
    }
    
    // Initialize vacancy application form
    if (document.getElementById('application-form')) {
        new FormHandler('application-form');
    }
    
    // Initialize file upload preview
    initFileUploadPreview();
});

function initFileUploadPreview() {
    const fileInputs = document.querySelectorAll('input[type="file"][data-preview]');
    
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const previewId = this.dataset.preview;
            const previewElement = document.getElementById(previewId);
            const file = this.files[0];
            
            if (!file || !previewElement) return;
            
            // Clear previous preview
            previewElement.innerHTML = '';
            
            // Create preview based on file type
            if (file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const img = document.createElement('img');
                    img.src = e.target.result;
                    img.className = 'max-w-full h-auto rounded';
                    previewElement.appendChild(img);
                };
                reader.readAsDataURL(file);
            } else {
                const fileInfo = document.createElement('div');
                fileInfo.className = 'p-3 bg-gray-100 rounded';
                fileInfo.innerHTML = `
                    <i class="fas fa-file mr-2"></i>
                    <span class="font-medium">${file.name}</span>
                    <span class="text-gray-600 text-sm ml-2">(${(file.size / 1024).toFixed(1)} KB)</span>
                `;
                previewElement.appendChild(fileInfo);
            }
        });
    });
}
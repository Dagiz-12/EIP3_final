// Navigation and dropdown functionality
document.addEventListener('DOMContentLoaded', function() {
    // Enhanced dropdown functionality
    const dropdownContainers = document.querySelectorAll('.nav-dropdown-container');
    
    dropdownContainers.forEach(container => {
        const button = container.querySelector('button');
        const dropdown = container.querySelector('.nav-dropdown');
        const chevron = container.querySelector('.fas');
        
        let hideTimeout;
        let showTimeout;
        
        // Show dropdown
        const showDropdown = () => {
            clearTimeout(hideTimeout);
            showTimeout = setTimeout(() => {
                dropdown.classList.remove('hidden');
                chevron.classList.add('rotate-180');
                button.setAttribute('aria-expanded', 'true');
            }, 150);
        };
        
        // Hide dropdown
        const hideDropdown = () => {
            clearTimeout(showTimeout);
            hideTimeout = setTimeout(() => {
                dropdown.classList.add('hidden');
                chevron.classList.remove('rotate-180');
                button.setAttribute('aria-expanded', 'false');
            }, 300);
        };
        
        // Desktop hover events
        container.addEventListener('mouseenter', showDropdown);
        container.addEventListener('mouseleave', hideDropdown);
        
        // Keep dropdown open when hovering over it
        dropdown.addEventListener('mouseenter', () => {
            clearTimeout(hideTimeout);
        });
        
        dropdown.addEventListener('mouseleave', hideDropdown);
        
        // Touch devices: toggle on click
        button.addEventListener('click', (e) => {
            if (window.innerWidth < 768) {
                e.preventDefault();
                const isExpanded = button.getAttribute('aria-expanded') === 'true';
                if (isExpanded) {
                    hideDropdown();
                } else {
                    showDropdown();
                }
            }
        });
    });
});
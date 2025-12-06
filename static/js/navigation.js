// Enhanced navigation with reliable dropdowns
class NavigationManager {
    constructor() {
        this.dropdowns = new Map();
        this.init();
    }
    
    init() {
        this.setupDropdowns();
        this.setupMobileMenu();
        this.setupScrollEffects();
        this.setupTouchHandlers();
    }
    
    setupDropdowns() {
        document.querySelectorAll('.nav-dropdown-container').forEach(container => {
            const button = container.querySelector('button');
            const dropdown = container.querySelector('.nav-dropdown');
            const chevron = container.querySelector('.fas.fa-chevron-down');
            
            if (!button || !dropdown) return;
            
            const dropdownId = dropdown.id;
            this.dropdowns.set(dropdownId, { container, button, dropdown, chevron });
            
            // Desktop hover
            container.addEventListener('mouseenter', () => this.showDropdown(dropdownId));
            container.addEventListener('mouseleave', () => this.hideDropdown(dropdownId));
            
            // Mobile click
            button.addEventListener('click', (e) => {
                if (window.innerWidth < 768) {
                    e.preventDefault();
                    e.stopPropagation();
                    this.toggleDropdown(dropdownId);
                }
            });
            
            // Close dropdowns when clicking outside
            document.addEventListener('click', (e) => {
                if (!container.contains(e.target)) {
                    this.hideDropdown(dropdownId);
                }
            });
        });
    }
    
    showDropdown(id) {
        if (window.innerWidth < 768) return;
        
        const dropdown = this.dropdowns.get(id);
        if (!dropdown) return;
        
        // Close other dropdowns
        this.dropdowns.forEach((d, key) => {
            if (key !== id && !d.dropdown.classList.contains('hidden')) {
                this.hideDropdown(key);
            }
        });
        
        dropdown.dropdown.classList.remove('hidden', 'opacity-0', 'invisible');
        dropdown.dropdown.classList.add('opacity-100', 'visible');
        if (dropdown.chevron) {
            dropdown.chevron.classList.add('rotate-180');
        }
        dropdown.button.setAttribute('aria-expanded', 'true');
    }
    
    hideDropdown(id) {
        const dropdown = this.dropdowns.get(id);
        if (!dropdown) return;
        
        dropdown.dropdown.classList.add('opacity-0', 'invisible');
        dropdown.dropdown.classList.remove('opacity-100', 'visible');
        
        // Delay hiding for smooth animation
        setTimeout(() => {
            if (dropdown.dropdown.classList.contains('opacity-0')) {
                dropdown.dropdown.classList.add('hidden');
            }
        }, 300);
        
        if (dropdown.chevron) {
            dropdown.chevron.classList.remove('rotate-180');
        }
        dropdown.button.setAttribute('aria-expanded', 'false');
    }
    
    toggleDropdown(id) {
        const dropdown = this.dropdowns.get(id);
        if (!dropdown) return;
        
        const isHidden = dropdown.dropdown.classList.contains('hidden');
        if (isHidden) {
            this.showDropdown(id);
        } else {
            this.hideDropdown(id);
        }
    }
    
    setupMobileMenu() {
        const mobileMenuButton = document.getElementById('mobile-menu-button');
        const mobileMenu = document.getElementById('mobile-menu');
        
        if (mobileMenuButton && mobileMenu) {
            mobileMenuButton.addEventListener('click', () => {
                mobileMenu.classList.toggle('hidden');
                const icon = mobileMenuButton.querySelector('i');
                if (icon.classList.contains('fa-bars')) {
                    icon.classList.replace('fa-bars', 'fa-times');
                } else {
                    icon.classList.replace('fa-times', 'fa-bars');
                }
            });
        }
    }
    
    setupScrollEffects() {
        const nav = document.querySelector('nav');
        if (!nav) return;
        
        let lastScroll = 0;
        window.addEventListener('scroll', () => {
            const currentScroll = window.pageYOffset;
            
            // Add shadow on scroll
            if (currentScroll > 50) {
                nav.classList.add('shadow-lg', 'bg-white/95', 'backdrop-blur-sm');
                nav.classList.remove('py-4');
                nav.classList.add('py-3');
            } else {
                nav.classList.remove('shadow-lg', 'bg-white/95', 'backdrop-blur-sm', 'py-3');
                nav.classList.add('py-4');
            }
            
            // Hide/show on scroll direction
            if (currentScroll > lastScroll && currentScroll > 100) {
                nav.style.transform = 'translateY(-100%)';
            } else {
                nav.style.transform = 'translateY(0)';
            }
            
            lastScroll = currentScroll;
        });
    }
    
    setupTouchHandlers() {
        // Prevent body scroll when mobile menu is open
        document.addEventListener('touchmove', (e) => {
            const mobileMenu = document.getElementById('mobile-menu');
            if (mobileMenu && !mobileMenu.classList.contains('hidden')) {
                e.preventDefault();
            }
        }, { passive: false });
    }
}

// Initialize navigation
document.addEventListener('DOMContentLoaded', () => {
    window.navigationManager = new NavigationManager();
});
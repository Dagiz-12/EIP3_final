// Home page specific JavaScript with accurate counting
class HomePageManager {
    constructor() {
        this.counters = [];
        this.init();
    }
    
    init() {
        this.setupAccurateCounters();
        this.initSwiperSliders();
        this.initNewsletterPopup();
        this.initScrollAnimations();
        this.fetchRealStatistics();
    }
    
    setupAccurateCounters() {
        // These will be updated with real data from fetchRealStatistics()
        this.counters = Array.from(document.querySelectorAll('.counter')).map(counter => ({
            element: counter,
            target: parseInt(counter.getAttribute('data-target')) || 0,
            suffix: counter.getAttribute('data-suffix') || '',
            duration: 2500, // ms
            decimal: counter.hasAttribute('data-decimal'),
            prefix: counter.getAttribute('data-prefix') || ''
        }));
        
        // Start observing counters
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const counterIndex = this.counters.findIndex(c => c.element === entry.target);
                    if (counterIndex !== -1 && !this.counters[counterIndex].animated) {
                        this.animateCounter(this.counters[counterIndex]);
                        this.counters[counterIndex].animated = true;
                    }
                }
            });
        }, { threshold: 0.5, rootMargin: '0px 0px -100px 0px' });
        
        this.counters.forEach(counter => observer.observe(counter.element));
    }
    
    animateCounter(counter) {
        let start = 0;
        const increment = counter.target / (counter.duration / 16); // 60fps
        const element = counter.element;
        
        const update = () => {
            start += increment;
            if (start < counter.target) {
                let displayValue = Math.floor(start);
                if (counter.decimal) {
                    displayValue = start.toFixed(1);
                }
                element.textContent = counter.prefix + displayValue + counter.suffix;
                requestAnimationFrame(update);
            } else {
                let finalValue = counter.target;
                if (counter.decimal) {
                    finalValue = counter.target.toFixed(1);
                }
                element.textContent = counter.prefix + finalValue + counter.suffix;
            }
        };
        
        requestAnimationFrame(update);
    }
    
    async fetchRealStatistics() {
        try {
            const response = await fetch('/api/statistics/');
            if (response.ok) {
                const data = await response.json();
                
                // Update counters with real data
                this.counters.forEach((counter, index) => {
                    let realValue = 0;
                    const elementId = counter.element.id || counter.element.parentElement.textContent.toLowerCase();
                    
                    if (elementId.includes('year') || elementId.includes('service')) {
                        // Years of service (since 1991)
                        const currentYear = new Date().getFullYear();
                        realValue = currentYear - 1991; // Established in 1991
                    } else if (elementId.includes('project')) {
                        realValue = data.projects_count || 50;
                    } else if (elementId.includes('people') || elementId.includes('impacted')) {
                        realValue = data.people_impacted || 100000;
                    } else if (elementId.includes('partner')) {
                        realValue = data.partners_count || 25;
                    }
                    
                    // Update counter if real value is different
                    if (realValue > 0 && realValue !== counter.target) {
                        counter.target = realValue;
                        counter.element.setAttribute('data-target', realValue);
                        
                        // Re-animate if already visible
                        if (!counter.element.getAttribute('data-original')) {
                            counter.element.setAttribute('data-original', 'true');
                            this.animateCounter(counter);
                        }
                    }
                });
            }
        } catch (error) {
            console.log('Using default counter values');
        }
    }
    
    initSwiperSliders() {
        // Hero Slider
        if (document.querySelector('.hero-slider .swiper-container')) {
            this.heroSwiper = new Swiper('.hero-slider .swiper-container', {
                loop: true,
                speed: 800,
                autoplay: {
                    delay: 6000,
                    disableOnInteraction: false,
                    pauseOnMouseEnter: true,
                },
                pagination: {
                    el: '.swiper-pagination',
                    clickable: true,
                    dynamicBullets: true,
                },
                navigation: {
                    nextEl: '.swiper-button-next',
                    prevEl: '.swiper-button-prev',
                },
                effect: 'fade',
                fadeEffect: {
                    crossFade: true
                },
                parallax: true,
                on: {
                    init: function () {
                        this.el.classList.add('swiper-initialized');
                    },
                }
            });
        }
        
        // Partners Carousel
        if (document.querySelector('.partners-carousel .swiper-container')) {
            this.partnersSwiper = new Swiper('.partners-carousel .swiper-container', {
                slidesPerView: 2,
                spaceBetween: 30,
                loop: true,
                autoplay: {
                    delay: 4000,
                    disableOnInteraction: false,
                },
                breakpoints: {
                    640: { slidesPerView: 3, spaceBetween: 20 },
                    768: { slidesPerView: 4, spaceBetween: 25 },
                    1024: { slidesPerView: 5, spaceBetween: 30 },
                    1280: { slidesPerView: 6, spaceBetween: 35 },
                },
                navigation: {
                    nextEl: '.partners-carousel .swiper-button-next',
                    prevEl: '.partners-carousel .swiper-button-prev',
                },
            });
        }
    }
    
    initNewsletterPopup() {
        const popup = document.getElementById('newsletter-popup');
        const closeBtn = popup?.querySelector('[onclick]');
        
        // Show after 8 seconds if not closed before
        setTimeout(() => {
            if (popup && !localStorage.getItem('eip_newsletter_closed')) {
                popup.classList.remove('hidden');
                document.body.style.overflow = 'hidden';
            }
        }, 8000);
        
        // Close functionality
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                popup.classList.add('hidden');
                document.body.style.overflow = '';
                localStorage.setItem('eip_newsletter_closed', 'true');
            });
        }
        
        // Close on background click
        popup?.addEventListener('click', (e) => {
            if (e.target === popup) {
                popup.classList.add('hidden');
                document.body.style.overflow = '';
                localStorage.setItem('eip_newsletter_closed', 'true');
            }
        });
        
        // Popup form submission
        const popupForm = document.getElementById('popup-newsletter-form');
        if (popupForm) {
            popupForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                await this.handleNewsletterSubmit(popupForm, 'popup');
            });
        }
        
        // CTA form submission
        const ctaForm = document.getElementById('newsletter-cta-form');
        if (ctaForm) {
            ctaForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                await this.handleNewsletterSubmit(ctaForm, 'cta');
            });
        }
    }
    
    async handleNewsletterSubmit(form, type = 'popup') {
        const emailInput = form.querySelector('input[type="email"]');
        const submitBtn = form.querySelector('button[type="submit"]');
        const messageEl = document.getElementById(`${type}-newsletter-message`);
        
        if (!emailInput || !submitBtn) return;
        
        const email = emailInput.value.trim();
        const originalText = submitBtn.innerHTML;
        
        // Validate email
        if (!this.validateEmail(email)) {
            this.showMessage(messageEl, 'Please enter a valid email address', 'error');
            return;
        }
        
        // Show loading
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i> Subscribing...';
        submitBtn.disabled = true;
        
        try {
            const response = await fetch('/api/subscribe/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken(),
                },
                body: JSON.stringify({ email })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                this.showMessage(messageEl, data.message || 'Successfully subscribed!', 'success');
                emailInput.value = '';
                
                // Close popup if successful
                if (type === 'popup') {
                    const popup = document.getElementById('newsletter-popup');
                    popup.classList.add('hidden');
                    document.body.style.overflow = '';
                    localStorage.setItem('eip_newsletter_closed', 'true');
                }
            } else {
                this.showMessage(messageEl, data.error || 'Subscription failed', 'error');
            }
        } catch (error) {
            this.showMessage(messageEl, 'Network error. Please try again.', 'error');
        } finally {
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }
    }
    
    validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }
    
    getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    }
    
    showMessage(element, message, type = 'info') {
        if (!element) return;
        
        element.textContent = message;
        element.className = `mt-2 text-sm ${type === 'success' ? 'text-green-600' : 'text-red-600'}`;
        element.classList.remove('hidden');
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            element.classList.add('hidden');
        }, 5000);
    }
    
    initScrollAnimations() {
        // Add scroll-triggered animations
        const animateOnScroll = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-popUp');
                    animateOnScroll.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });
        
        // Observe all elements with animation classes
        document.querySelectorAll('.animate-on-scroll').forEach(el => {
            animateOnScroll.observe(el);
        });
    }
}

// Initialize home page
document.addEventListener('DOMContentLoaded', () => {
    window.homePageManager = new HomePageManager();
});
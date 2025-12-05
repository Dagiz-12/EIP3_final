// Home page specific JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Animated counters
    const counters = document.querySelectorAll('.counter');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counter = entry.target;
                const target = parseInt(counter.getAttribute('data-target'));
                const suffix = counter.getAttribute('data-suffix') || '';
                const duration = 2000;
                const step = target / (duration / 16);
                let current = 0;
                
                const updateCounter = () => {
                    current += step;
                    if (current < target) {
                        counter.textContent = Math.floor(current) + suffix;
                        requestAnimationFrame(updateCounter);
                    } else {
                        counter.textContent = target + suffix;
                    }
                };
                
                updateCounter();
                observer.unobserve(counter);
            }
        });
    }, { threshold: 0.5 });
    
    counters.forEach(counter => observer.observe(counter));
    
    // Initialize Swiper for hero slider
    const heroSwiper = new Swiper('.hero-slider .swiper-container', {
        loop: true,
        autoplay: {
            delay: 5000,
            disableOnInteraction: false,
        },
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        effect: 'fade',
        fadeEffect: {
            crossFade: true
        },
        speed: 1000,
    });
    
    // Initialize partners carousel
    const partnersSwiper = new Swiper('.partners-carousel .swiper-container', {
        slidesPerView: 2,
        spaceBetween: 20,
        loop: true,
        autoplay: {
            delay: 3000,
            disableOnInteraction: false,
        },
        navigation: {
            nextEl: '.partners-carousel .swiper-button-next',
            prevEl: '.partners-carousel .swiper-button-prev',
        },
        breakpoints: {
            640: { slidesPerView: 3 },
            1024: { slidesPerView: 4 },
            1280: { slidesPerView: 5 },
        },
    });
    
    // Newsletter pop-up (shows after 5 seconds)
    setTimeout(() => {
        const popup = document.getElementById('newsletter-popup');
        if (popup && !localStorage.getItem('newsletterClosed')) {
            popup.classList.remove('hidden');
        }
    }, 5000);
    
    // Close popup and remember preference
    document.getElementById('newsletter-popup')?.addEventListener('click', function(e) {
        if (e.target === this) {
            this.classList.add('hidden');
            localStorage.setItem('newsletterClosed', 'true');
        }
    });
    
    // Popup newsletter form
    document.getElementById('popup-newsletter-form')?.addEventListener('submit', async function(e) {
        e.preventDefault();
        const email = this.querySelector('input[type="email"]').value;
        
        try {
            const response = await fetch('/api/subscribe/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value || ''
                },
                body: JSON.stringify({ email: email })
            });
            
            if (response.ok) {
                showNotification('Thank you for subscribing!', 'success');
                document.getElementById('newsletter-popup').classList.add('hidden');
                localStorage.setItem('newsletterClosed', 'true');
            } else {
                showNotification('Subscription failed. Please try again.', 'error');
            }
        } catch (error) {
            showNotification('Network error. Please try again.', 'error');
        }
    });
});
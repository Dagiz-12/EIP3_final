// Home page specific JavaScript

function initHeroSlider() {
    const sliderElement = document.querySelector('.swiper-container');
    if (!sliderElement) return;
    
    // Dynamically load Swiper only on home page
    const swiperCSS = document.createElement('link');
    swiperCSS.rel = 'stylesheet';
    swiperCSS.href = 'https://unpkg.com/swiper/swiper-bundle.min.css';
    document.head.appendChild(swiperCSS);
    
    const swiperScript = document.createElement('script');
    swiperScript.src = 'https://unpkg.com/swiper/swiper-bundle.min.js';
    swiperScript.onload = function() {
        new Swiper('.swiper-container', {
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
            speed: 800,
        });
    };
    document.body.appendChild(swiperScript);
}

function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fadeInUp');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe elements for animation
    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        observer.observe(el);
    });
}

// Counter animation for statistics
function initCounters() {
    const counterElements = document.querySelectorAll('.counter');
    if (!counterElements.length) return;
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = entry.target;
                const finalValue = parseInt(target.dataset.value);
                const duration = 2000; // 2 seconds
                const increment = finalValue / (duration / 16); // 60fps
                let currentValue = 0;
                
                const timer = setInterval(() => {
                    currentValue += increment;
                    if (currentValue >= finalValue) {
                        target.textContent = finalValue.toLocaleString() + (target.dataset.suffix || '');
                        clearInterval(timer);
                    } else {
                        target.textContent = Math.floor(currentValue).toLocaleString();
                    }
                }, 16);
                
                observer.unobserve(target);
            }
        });
    }, { threshold: 0.5 });
    
    counterElements.forEach(el => observer.observe(el));
}

// Initialize home page features
document.addEventListener('DOMContentLoaded', function() {
    initHeroSlider();
    initScrollAnimations();
    initCounters();
});
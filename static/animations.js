/**
 * SunDevil Circles - Animation Controller
 * Handles scroll-triggered animations and interactive effects
 */

document.addEventListener('DOMContentLoaded', function () {
    // ============================================
    // INTERSECTION OBSERVER FOR SCROLL ANIMATIONS
    // ============================================

    const observerOptions = {
        threshold: 0.15,
        rootMargin: '0px 0px -80px 0px'
    };

    const animationObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                // Only animate once
                animationObserver.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Elements to animate on scroll
    const animatedElements = [
        '.step-card',
        '.safety-content',
        '.safety-feature-card',
        '.quote-box',
        '.cta-section',
        '.site-footer'
    ];

    animatedElements.forEach(selector => {
        document.querySelectorAll(selector).forEach(el => {
            animationObserver.observe(el);
        });
    });

    // ============================================
    // NAVBAR SCROLL EFFECT
    // ============================================

    const navbar = document.querySelector('.navbar');

    if (navbar) {
        let lastScrollY = window.scrollY;

        const handleScroll = () => {
            const currentScrollY = window.scrollY;

            // Add scrolled class when scrolled down
            if (currentScrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }

            lastScrollY = currentScrollY;
        };

        // Throttle scroll events for performance
        let ticking = false;
        window.addEventListener('scroll', () => {
            if (!ticking) {
                window.requestAnimationFrame(() => {
                    handleScroll();
                    ticking = false;
                });
                ticking = true;
            }
        }, { passive: true });

        // Initial check
        handleScroll();
    }

    // ============================================
    // BUTTON RIPPLE EFFECT (Optional enhancement)
    // ============================================

    const buttons = document.querySelectorAll('.btn-hero-primary, .btn-primary, .btn-hero-secondary');

    buttons.forEach(button => {
        button.addEventListener('click', function (e) {
            // Create ripple element
            const ripple = document.createElement('span');
            ripple.classList.add('ripple-effect');

            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;

            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';

            this.appendChild(ripple);

            // Remove ripple after animation
            setTimeout(() => ripple.remove(), 600);
        });
    });

    // ============================================
    // SMOOTH SCROLL FOR ANCHOR LINKS
    // ============================================

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                e.preventDefault();
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // ============================================
    // FEATURE PILL HOVER SOUND (Optional - disabled by default)
    // ============================================

    // Uncomment to enable subtle hover feedback
    // const featurePills = document.querySelectorAll('.feature-pill');
    // featurePills.forEach(pill => {
    //     pill.addEventListener('mouseenter', () => {
    //         // Optional: Add haptic feedback or sound
    //     });
    // });

    // ============================================
    // LAZY LOAD IMAGES WITH FADE-IN
    // ============================================

    const lazyImages = document.querySelectorAll('img[data-src]');

    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.add('loaded');
                    imageObserver.unobserve(img);
                }
            });
        });

        lazyImages.forEach(img => imageObserver.observe(img));
    }

    // ============================================
    // PARALLAX EFFECT FOR HERO (Subtle)
    // ============================================

    const heroSection = document.querySelector('.hero');
    const heroBg = document.querySelector('.hero-bg');

    if (heroSection && heroBg) {
        window.addEventListener('scroll', () => {
            const scrolled = window.scrollY;
            if (scrolled < window.innerHeight) {
                // Subtle parallax - bg moves slower than scroll
                heroBg.style.transform = `translateY(${scrolled * 0.3}px)`;
            }
        }, { passive: true });
    }

    // ============================================
    // STAGGER ANIMATION HELPER
    // ============================================

    function staggerAnimation(elements, delayIncrement = 100) {
        elements.forEach((el, index) => {
            el.style.transitionDelay = `${index * delayIncrement}ms`;
        });
    }

    // Apply stagger to safety feature cards
    const safetyCards = document.querySelectorAll('.safety-feature-card');
    staggerAnimation(safetyCards, 100);

    // Apply stagger to step cards
    const stepCards = document.querySelectorAll('.step-card');
    staggerAnimation(stepCards, 100);

    console.log('SunDevil Circles animations initialized');
});

// ============================================
// ADD RIPPLE EFFECT STYLES DYNAMICALLY
// ============================================

const rippleStyles = document.createElement('style');
rippleStyles.textContent = `
    .ripple-effect {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: scale(0);
        animation: ripple 0.6s linear;
        pointer-events: none;
    }
    
    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    .btn-hero-primary,
    .btn-primary,
    .btn-hero-secondary {
        position: relative;
        overflow: hidden;
    }
`;
document.head.appendChild(rippleStyles);


***

## **MASTER PROMPT FOR AI AGENT: SunDevil Circles Homepage Transitions**

You are implementing modern, smooth CSS and JavaScript transitions for the SunDevil Circles homepage at `http://127.0.0.1:5000/`. 

### **CRITICAL REQUIREMENTS - READ FIRST**

1. **DO NOT CHANGE THE EXISTING LAYOUT OR STYLING** - Only add transition/animation properties
2. **DO NOT modify positioning, spacing, colors, fonts, or any visual design elements**
3. **DO NOT touch the working navigation buttons** (Get Support, Browse Resources, Find Groups, My Groups, Find Peers, My Peers, Dashboard)
4. **DO NOT modify the footer navigation buttons** (How It Works, Safety & Privacy, Resources) - they are working correctly
5. **ONLY add smooth transitions and animations to enhance the user experience**
6. **Move Profile button closer to Log Out button** - Add `margin-left: auto;` to the Profile link to create visual separation from center nav items

***

### **NAVIGATION BAR SPACING FIX**

```css
/* Create visual grouping: Left (Logo + Main Nav) | Right (Profile + Log Out + Dashboard) */
nav a[href="/profile"] {
  margin-left: auto; /* Push Profile to the right, creating gap from center nav */
}

nav a[href="/logout"] {
  margin-left: 0.5rem; /* Keep Log Out close to Profile */
}

nav a[href="/decision"] {
  margin-left: 0.75rem; /* Slight space before Dashboard button */
}
```

***

### **ANIMATION PRINCIPLES**

- **Timing**: 0.3-0.6s for interactions, 0.6-0.8s for entrance animations
- **Easing**: Use `ease-out` for entrances, `ease-in-out` for hovers
- **Performance**: Only animate `transform` and `opacity` (GPU-accelerated)
- **Accessibility**: Respect `prefers-reduced-motion` media query
- **Balance**: Modern and smooth, not dramatic or simplistic

***

### **SPECIFIC IMPLEMENTATIONS**

### 1. **Hero Section Animations**

```css
/* Staggered fade-in with slide-up - ANIMATION ONLY, NO LAYOUT CHANGES */
@keyframes fadeSlideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Apply to hero heading - Target by existing class/ID */
.hero-title, h1:has(+ p) {
  animation: fadeSlideUp 0.8s cubic-bezier(0.4, 0.0, 0.2, 1) forwards;
  animation-delay: 0.2s;
  opacity: 0;
}

/* Apply to hero subtitle */
.hero-subtitle, .hero-title + p {
  animation: fadeSlideUp 0.8s cubic-bezier(0.4, 0.0, 0.2, 1) forwards;
  animation-delay: 0.4s;
  opacity: 0;
}

/* Button hover effect - NO SIZE/POSITION CHANGES */
button, .cta-button, a[href="/decision"] {
  transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
}

button:hover, .cta-button:hover, a[href="/decision"]:hover {
  transform: scale(1.05);
  box-shadow: 0 8px 16px rgba(139, 35, 50, 0.3);
}

/* Subtle parallax on hero background */
.hero-section {
  transition: transform 0.5s ease-out;
}
```

### 2. **Navigation Bar Transitions**

```css
/* Scroll-based backdrop blur - NO LAYOUT CHANGES */
nav {
  transition: backdrop-filter 0.3s ease, background-color 0.3s ease;
}

nav.scrolled {
  backdrop-filter: blur(10px);
  background-color: rgba(255, 255, 255, 0.95);
}

/* Nav link hover with underline slide - ANIMATION ONLY */
nav a {
  position: relative;
  transition: color 0.3s ease;
}

nav a::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 2px;
  background: currentColor;
  transition: width 0.3s ease-out;
}

nav a:hover::after {
  width: 100%;
}

/* JavaScript to add 'scrolled' class */
window.addEventListener('scroll', () => {
  const nav = document.querySelector('nav');
  if (window.scrollY > 50) {
    nav.classList.add('scrolled');
  } else {
    nav.classList.remove('scrolled');
  }
});
```

### 3. **Crisis Banner Animation**

```css
/* Slide-down entrance - ANIMATION ONLY */
#crisisBanner {
  animation: slideDown 0.5s ease-out;
}

@keyframes slideDown {
  from {
    transform: translateY(-100%);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

/* Subtle pulse on shield icon */
#crisisBanner svg, #crisisBanner .icon {
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.05);
    opacity: 0.85;
  }
}
```

### 4. **Feature Pills (Privacy-First, Student Supporters, Culturally-Aware)**

```css
/* Staggered float-up animation - ANIMATION ONLY */
.feature-pill, [class*="privacy"], [class*="supporter"], [class*="cultural"] {
  opacity: 0;
  animation: floatUp 0.6s ease-out forwards;
  transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
}

.feature-pill:nth-child(1) { animation-delay: 0.6s; }
.feature-pill:nth-child(2) { animation-delay: 0.75s; }
.feature-pill:nth-child(3) { animation-delay: 0.9s; }

@keyframes floatUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Hover lift effect - ANIMATION ONLY */
.feature-pill:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
}

.feature-pill:hover .icon, .feature-pill:hover svg {
  transform: scale(1.15);
  transition: transform 0.3s ease;
}
```

### 5. **How It Works Cards (4-Step Process)**

```javascript
// Intersection Observer for scroll-triggered animations
const observerOptions = {
  threshold: 0.2,
  rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry, index) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('animate-in');
      observer.unobserve(entry.target); // Animate once
    }
  });
}, observerOptions);

// Observe all step cards
document.querySelectorAll('.step-card, [class*="step"]').forEach(card => {
  observer.observe(card);
});
```

```css
/* Step cards alternating slide-in - ANIMATION ONLY */
.step-card, #how-it-works > div {
  opacity: 0;
  transform: translateX(-50px);
  transition: all 0.6s cubic-bezier(0.4, 0.0, 0.2, 1);
}

.step-card:nth-child(even) {
  transform: translateX(50px);
}

.step-card.animate-in {
  opacity: 1;
  transform: translateX(0);
}

/* Staggered delays */
.step-card:nth-child(1).animate-in { transition-delay: 0s; }
.step-card:nth-child(2).animate-in { transition-delay: 0.15s; }
.step-card:nth-child(3).animate-in { transition-delay: 0.3s; }
.step-card:nth-child(4).animate-in { transition-delay: 0.45s; }

/* Card hover effect - ANIMATION ONLY */
.step-card {
  transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
}

.step-card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}

/* Number badge animation on hover */
.step-number, [class*="badge"] {
  transition: transform 0.3s ease;
}

.step-card:hover .step-number {
  transform: scale(1.1) rotate(5deg);
}

/* Icon bounce on hover */
.step-icon, .step-card svg {
  transition: transform 0.3s ease;
}

.step-card:hover .step-icon {
  animation: bounce 0.6s ease;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}
```

### 6. **"Peer Support, Not Therapy" Section**

```css
/* Fade-in on scroll - ANIMATION ONLY */
.testimonial-section, #safety {
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.8s ease-out;
}

.testimonial-section.animate-in {
  opacity: 1;
  transform: translateY(0);
}

/* Gradient shift on "not therapy" emphasis */
.emphasis-text, [class*="not-therapy"] {
  background: linear-gradient(90deg, #8B2332, #FFC627);
  background-size: 200% 100%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: gradientShift 3s ease infinite;
}

@keyframes gradientShift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

/* Quote fade-in */
blockquote::before, .testimonial-quote::before {
  opacity: 0.2;
  animation: fadeIn 1s ease 0.5s forwards;
}

@keyframes fadeIn {
  to { opacity: 0.2; }
}
```

### 7. **Feature Grid Cards (Privacy Protected, Student Supporters, etc.)**

```css
/* Grid item staggered appearance - ANIMATION ONLY */
.feature-card, .feature-grid > div {
  opacity: 0;
  transform: scale(0.9);
  transition: all 0.5s cubic-bezier(0.4, 0.0, 0.2, 1);
}

.feature-card.animate-in {
  opacity: 1;
  transform: scale(1);
}

.feature-card:nth-child(1).animate-in { transition-delay: 0s; }
.feature-card:nth-child(2).animate-in { transition-delay: 0.1s; }
.feature-card:nth-child(3).animate-in { transition-delay: 0.2s; }
.feature-card:nth-child(4).animate-in { transition-delay: 0.3s; }

/* Card hover effect - ANIMATION ONLY, NO LAYOUT CHANGES */
.feature-card {
  transition: transform 0.3s ease-in-out, background-color 0.3s ease, box-shadow 0.3s ease;
  border: 2px solid transparent;
  border-transition: border-color 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
  background-color: rgba(139, 35, 50, 0.05);
  border-color: rgba(139, 35, 50, 0.2);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.feature-card:hover .icon, .feature-card:hover svg {
  transform: scale(1.2);
  filter: brightness(1.2);
  transition: all 0.3s ease;
}
```

### 8. **CTA Section ("Ready to Find Your Circle?")**

```css
/* Fade-in and scale-up - ANIMATION ONLY */
.cta-section {
  opacity: 0;
  transform: scale(0.95);
  transition: all 0.8s cubic-bezier(0.4, 0.0, 0.2, 1);
}

.cta-section.animate-in {
  opacity: 1;
  transform: scale(1);
}

/* Button shimmer effect on hover */
.cta-button, a[href="/decision"] {
  position: relative;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.cta-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.5s ease;
}

.cta-button:hover::before {
  left: 100%;
}

.cta-button:hover {
  transform: scale(1.05);
  box-shadow: 0 12px 24px rgba(139, 35, 50, 0.4);
}
```

### 9. **Footer Animations**

```css
/* Footer fade-in - ANIMATION ONLY */
footer {
  opacity: 0;
  transition: opacity 0.6s ease;
}

footer.animate-in {
  opacity: 1;
}

/* Footer link underline animation */
footer a {
  position: relative;
  transition: color 0.3s ease;
}

footer a::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 1px;
  background: currentColor;
  transition: width 0.3s ease-out;
}

footer a:hover::after {
  width: 100%;
}

/* Heart pulse animation */
.heart-icon, footer [class*="heart"] {
  display: inline-block;
  animation: heartbeat 1.5s ease-in-out infinite;
}

@keyframes heartbeat {
  0%, 100% { transform: scale(1); }
  10%, 30% { transform: scale(1.
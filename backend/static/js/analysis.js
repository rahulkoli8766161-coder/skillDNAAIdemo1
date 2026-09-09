/**
 * SkillDNA-AI — Analysis Page JavaScript
 * Handles AI analysis trigger, loading animation, and results rendering
 */

document.addEventListener('DOMContentLoaded', () => {
    initAnalysisPage();
    initScoreCircle();
    initSkillBars();
});

/**
 * Initialize analysis page interactions
 */
function initAnalysisPage() {
    // Animate cards on scroll
    const cards = document.querySelectorAll('.glass-card');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    cards.forEach((card, i) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = `all 0.6s ease ${i * 0.1}s`;
        observer.observe(card);
    });
}

/**
 * Animate the circular score indicator
 */
function initScoreCircle() {
    const circle = document.querySelector('.progress-circle');
    const scoreDisplay = document.querySelector('.score-number');

    if (!circle || !scoreDisplay) return;

    const score = parseInt(scoreDisplay.dataset.score || '0', 10);
    const circumference = 2 * Math.PI * 70; // radius = 70
    const offset = circumference - (score / 100) * circumference;

    // Set initial state
    circle.style.strokeDasharray = circumference;
    circle.style.strokeDashoffset = circumference;

    // Animate after a short delay
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    circle.style.transition = 'stroke-dashoffset 2s cubic-bezier(0.34, 1.56, 0.64, 1)';
                    circle.style.strokeDashoffset = offset;
                    animateScoreNumber(scoreDisplay, score);
                }, 300);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    observer.observe(scoreDisplay.closest('.score-circle') || scoreDisplay);
}

/**
 * Animate score number counting up
 */
function animateScoreNumber(element, target) {
    let current = 0;
    const duration = 2000;
    const stepTime = duration / target;

    const timer = setInterval(() => {
        current++;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        element.innerHTML = `${current}<span>%</span>`;
    }, stepTime);
}

/**
 * Animate skill bars
 */
function initSkillBars() {
    const bars = document.querySelectorAll('.skill-bar-fill');
    if (bars.length === 0) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const bar = entry.target;
                const width = bar.dataset.width || '0';
                setTimeout(() => {
                    bar.style.width = width + '%';
                }, 200);
                observer.unobserve(bar);
            }
        });
    }, { threshold: 0.2 });

    bars.forEach(bar => observer.observe(bar));
}

/**
 * Show loading overlay when triggering analysis
 */
function triggerAnalysis(form) {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.classList.add('active');
    }
    return true; // Allow form submission
}

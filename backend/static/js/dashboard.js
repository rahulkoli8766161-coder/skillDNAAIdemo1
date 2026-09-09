/**
 * SkillDNA-AI — Dashboard JavaScript
 * Handles analysis trigger, loading animation modal, counter animations, and card hover effects
 */

document.addEventListener('DOMContentLoaded', () => {
    initAnalyzeTrigger();
    initCounterAnimations();
});

/**
 * Handle AI Analysis button trigger and show full-screen AI loading overlay
 */
function initAnalyzeTrigger() {
    const analyzeForm = document.getElementById('analyze-form');
    const analyzeBtn = document.getElementById('run-analysis-btn');

    if (!analyzeForm) return;

    analyzeForm.addEventListener('submit', () => {
        showLoadingOverlay();
    });

    if (analyzeBtn) {
        analyzeBtn.addEventListener('click', () => {
            showLoadingOverlay();
        });
    }
}

/**
 * Show full screen AI analysis loading overlay
 */
function showLoadingOverlay() {
    let overlay = document.getElementById('ai-loading-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'ai-loading-overlay';
        overlay.style.cssText = `
            position: fixed;
            inset: 0;
            z-index: 9999;
            background: rgba(3, 5, 9, 0.92);
            backdrop-filter: blur(25px);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: #ffffff;
            font-family: var(--font-cyber);
            text-align: center;
        `;
        overlay.innerHTML = `
            <div style="position: relative; width: 100px; height: 100px; margin-bottom: 2rem;">
                <div style="position: absolute; inset: 0; border: 3px solid transparent; border-top-color: var(--cyan-glow); border-bottom-color: var(--blue-electric); border-radius: 50%; animation: spin 1s linear infinite;"></div>
                <div style="position: absolute; inset: 15px; border: 3px solid transparent; border-left-color: var(--purple-glow); border-right-color: var(--emerald-glow); border-radius: 50%; animation: spinReverse 1.5s linear infinite;"></div>
                <i class="fa-solid fa-dna text-cyan" style="font-size: 2.2rem; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); animation: pulseGlow 1.5s ease-in-out infinite;"></i>
            </div>
            <h2 class="title-glow text-gradient" style="font-size: 1.8rem; margin-bottom: 0.8rem;">GENOME SEQUENCE ANALYSIS IN PROGRESS</h2>
            <p id="ai-loading-status" style="color: var(--cyan-glow); font-size: 1.1rem; letter-spacing: 0.05em;">Parsing Profile Data & Skills Matrix...</p>
            <style>
                @keyframes spin { to { transform: rotate(360deg); } }
                @keyframes spinReverse { to { transform: rotate(-360deg); } }
                @keyframes pulseGlow { 0%, 100% { opacity: 0.6; } 50% { opacity: 1; filter: drop-shadow(0 0 15px var(--cyan-glow)); } }
            </style>
        `;
        document.body.appendChild(overlay);
    } else {
        overlay.style.display = 'flex';
    }

    // Dynamic loading messages step-through
    const statusText = document.getElementById('ai-loading-status');
    const messages = [
        "Parsing Profile Data & Skills Matrix...",
        "Extracting Skill Gaps vs Market Standards...",
        "Synthesizing Technical Match Score...",
        "Generating Personalized Learning Roadmap..."
    ];
    let idx = 0;
    setInterval(() => {
        idx = (idx + 1) % messages.length;
        if (statusText) statusText.textContent = messages[idx];
    }, 1200);
}

/**
 * Animated counter effect for metric numbers
 */
function initCounterAnimations() {
    const counters = document.querySelectorAll('.animate-counter');
    counters.forEach(counter => {
        const target = parseInt(counter.dataset.target || counter.textContent, 10);
        if (isNaN(target)) return;

        let count = 0;
        const speed = target / 30;
        const updateCount = () => {
            count += speed;
            if (count < target) {
                counter.textContent = Math.ceil(count);
                setTimeout(updateCount, 30);
            } else {
                counter.textContent = target;
            }
        };
        updateCount();
    });
}

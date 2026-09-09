/**
 * SkillDNA-AI — Advanced Neural Constellation Background System
 * Creates an immersive, interactive particle network with:
 * - Floating luminous particles (neurons)
 * - Dynamic connection lines between nearby particles (synapses)
 * - Mouse-reactive energy flare & attraction zone
 * - Pulsing hub nodes with depth-of-field parallax
 * - Ambient floating micro-particles (stars)
 * - Smooth performance-optimized animation loop
 */

document.addEventListener('DOMContentLoaded', () => {
    initCyberCanvas();
    initPasswordToggle();
    initOptionTabs();
    initFlashDismiss();
    initNavbarMobile();
});

/* ============================================
   1. Neural Constellation Canvas Animation
   ============================================ */
function initCyberCanvas() {
    const canvas = document.getElementById('cyber-canvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let W = canvas.width = window.innerWidth;
    let H = canvas.height = window.innerHeight;
    let animationId;

    // --- Configuration ---
    const CONFIG = {
        particleCount: Math.min(Math.floor((W * H) / 12000), 120),
        connectionDistance: 180,
        mouseRadius: 250,
        mouseForce: 0.04,
        particleMinSize: 1.2,
        particleMaxSize: 3.5,
        hubCount: 5,
        hubSize: 5,
        microParticleCount: 60,
        speedFactor: 0.35,
        glowIntensity: 0.85
    };

    // --- Mouse Tracker ---
    let mouse = { x: W / 2, y: H / 2, active: false };

    window.addEventListener('mousemove', (e) => {
        mouse.x = e.clientX;
        mouse.y = e.clientY;
        mouse.active = true;
    });
    window.addEventListener('mouseleave', () => { mouse.active = false; });

    // --- Resize Handler ---
    let resizeTimeout;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            W = canvas.width = window.innerWidth;
            H = canvas.height = window.innerHeight;
            initParticles();
        }, 200);
    });

    // --- Color Palette ---
    const COLORS = {
        cyan: { r: 0, g: 240, b: 255 },
        blue: { r: 0, g: 119, b: 255 },
        purple: { r: 138, g: 43, b: 226 },
        teal: { r: 0, g: 200, b: 220 },
        white: { r: 200, g: 220, b: 255 }
    };

    const colorKeys = Object.keys(COLORS);

    function getRandomColor() {
        return COLORS[colorKeys[Math.floor(Math.random() * colorKeys.length)]];
    }

    // --- Particle Class ---
    class Particle {
        constructor(isHub = false) {
            this.reset(isHub);
        }

        reset(isHub = false) {
            this.x = Math.random() * W;
            this.y = Math.random() * H;
            this.isHub = isHub;
            this.size = isHub
                ? CONFIG.hubSize + Math.random() * 2
                : CONFIG.particleMinSize + Math.random() * (CONFIG.particleMaxSize - CONFIG.particleMinSize);

            const speed = CONFIG.speedFactor * (isHub ? 0.3 : (0.5 + Math.random() * 0.8));
            const angle = Math.random() * Math.PI * 2;
            this.vx = Math.cos(angle) * speed;
            this.vy = Math.sin(angle) * speed;

            this.color = isHub ? COLORS.cyan : getRandomColor();
            this.baseOpacity = isHub ? 0.9 : (0.3 + Math.random() * 0.5);
            this.opacity = this.baseOpacity;
            this.pulsePhase = Math.random() * Math.PI * 2;
            this.pulseSpeed = 0.01 + Math.random() * 0.02;
            this.depth = isHub ? 1 : (0.3 + Math.random() * 0.7); // parallax depth
        }

        update() {
            // Pulse glow
            this.pulsePhase += this.pulseSpeed;
            const pulseFactor = 0.7 + 0.3 * Math.sin(this.pulsePhase);
            this.opacity = this.baseOpacity * pulseFactor;
            this.currentSize = this.size * (0.85 + 0.15 * Math.sin(this.pulsePhase));

            // Mouse interaction
            if (mouse.active) {
                const dx = mouse.x - this.x;
                const dy = mouse.y - this.y;
                const dist = Math.sqrt(dx * dx + dy * dy);

                if (dist < CONFIG.mouseRadius) {
                    const force = (1 - dist / CONFIG.mouseRadius) * CONFIG.mouseForce;
                    this.vx += dx * force * 0.015;
                    this.vy += dy * force * 0.015;

                    // Brighten near mouse
                    this.opacity = Math.min(this.opacity + (1 - dist / CONFIG.mouseRadius) * 0.4, 1);
                }
            }

            // Apply velocity with friction
            this.x += this.vx;
            this.y += this.vy;
            this.vx *= 0.995;
            this.vy *= 0.995;

            // Wrap around screen edges with soft padding
            const pad = 50;
            if (this.x < -pad) this.x = W + pad;
            if (this.x > W + pad) this.x = -pad;
            if (this.y < -pad) this.y = H + pad;
            if (this.y > H + pad) this.y = -pad;
        }

        draw(ctx) {
            const { r, g, b } = this.color;

            // Outer glow
            if (this.isHub || this.currentSize > 2.5) {
                const glowRadius = this.currentSize * (this.isHub ? 8 : 4);
                const glow = ctx.createRadialGradient(this.x, this.y, 0, this.x, this.y, glowRadius);
                glow.addColorStop(0, `rgba(${r}, ${g}, ${b}, ${this.opacity * 0.35})`);
                glow.addColorStop(0.5, `rgba(${r}, ${g}, ${b}, ${this.opacity * 0.1})`);
                glow.addColorStop(1, 'transparent');
                ctx.fillStyle = glow;
                ctx.beginPath();
                ctx.arc(this.x, this.y, glowRadius, 0, Math.PI * 2);
                ctx.fill();
            }

            // Core particle
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.currentSize, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(${r}, ${g}, ${b}, ${this.opacity})`;
            ctx.fill();

            // Bright inner dot
            if (this.currentSize > 1.8) {
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.currentSize * 0.4, 0, Math.PI * 2);
                ctx.fillStyle = `rgba(255, 255, 255, ${this.opacity * 0.7})`;
                ctx.fill();
            }
        }
    }

    // --- Micro Particle (ambient stars) ---
    class MicroParticle {
        constructor() {
            this.x = Math.random() * W;
            this.y = Math.random() * H;
            this.size = 0.3 + Math.random() * 1.0;
            this.opacity = 0.1 + Math.random() * 0.3;
            this.twinklePhase = Math.random() * Math.PI * 2;
            this.twinkleSpeed = 0.005 + Math.random() * 0.015;
            this.vy = -0.05 - Math.random() * 0.1;
        }

        update() {
            this.twinklePhase += this.twinkleSpeed;
            this.y += this.vy;
            if (this.y < -10) {
                this.y = H + 10;
                this.x = Math.random() * W;
            }
        }

        draw(ctx) {
            const alpha = this.opacity * (0.5 + 0.5 * Math.sin(this.twinklePhase));
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(180, 210, 255, ${alpha})`;
            ctx.fill();
        }
    }

    // --- Initialize Particles ---
    let particles = [];
    let microParticles = [];

    function initParticles() {
        particles = [];
        microParticles = [];

        // Hub nodes
        for (let i = 0; i < CONFIG.hubCount; i++) {
            particles.push(new Particle(true));
        }
        // Regular particles
        for (let i = 0; i < CONFIG.particleCount; i++) {
            particles.push(new Particle(false));
        }
        // Micro ambient particles
        for (let i = 0; i < CONFIG.microParticleCount; i++) {
            microParticles.push(new MicroParticle());
        }
    }

    initParticles();

    // --- Draw Connection Lines ---
    function drawConnections(ctx) {
        for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
                const a = particles[i];
                const b = particles[j];
                const dx = a.x - b.x;
                const dy = a.y - b.y;
                const dist = Math.sqrt(dx * dx + dy * dy);

                const maxDist = (a.isHub || b.isHub) ? CONFIG.connectionDistance * 1.5 : CONFIG.connectionDistance;

                if (dist < maxDist) {
                    const alpha = (1 - dist / maxDist) * CONFIG.glowIntensity * Math.min(a.opacity, b.opacity);

                    // Gradient line between the two particle colors
                    const gradient = ctx.createLinearGradient(a.x, a.y, b.x, b.y);
                    gradient.addColorStop(0, `rgba(${a.color.r}, ${a.color.g}, ${a.color.b}, ${alpha * 0.7})`);
                    gradient.addColorStop(1, `rgba(${b.color.r}, ${b.color.g}, ${b.color.b}, ${alpha * 0.7})`);

                    ctx.beginPath();
                    ctx.moveTo(a.x, a.y);
                    ctx.lineTo(b.x, b.y);
                    ctx.strokeStyle = gradient;
                    ctx.lineWidth = (a.isHub || b.isHub) ? 1.2 : 0.6;
                    ctx.stroke();
                }
            }
        }
    }

    // --- Mouse Energy Flare ---
    function drawMouseFlare(ctx) {
        if (!mouse.active) return;

        // Outer attraction ring
        const ringGradient = ctx.createRadialGradient(mouse.x, mouse.y, 0, mouse.x, mouse.y, CONFIG.mouseRadius);
        ringGradient.addColorStop(0, 'rgba(0, 240, 255, 0.12)');
        ringGradient.addColorStop(0.3, 'rgba(0, 119, 255, 0.06)');
        ringGradient.addColorStop(0.7, 'rgba(138, 43, 226, 0.03)');
        ringGradient.addColorStop(1, 'transparent');

        ctx.fillStyle = ringGradient;
        ctx.beginPath();
        ctx.arc(mouse.x, mouse.y, CONFIG.mouseRadius, 0, Math.PI * 2);
        ctx.fill();

        // Inner core glow
        const coreGlow = ctx.createRadialGradient(mouse.x, mouse.y, 0, mouse.x, mouse.y, 40);
        coreGlow.addColorStop(0, 'rgba(0, 240, 255, 0.25)');
        coreGlow.addColorStop(1, 'transparent');
        ctx.fillStyle = coreGlow;
        ctx.beginPath();
        ctx.arc(mouse.x, mouse.y, 40, 0, Math.PI * 2);
        ctx.fill();
    }

    // --- Central Ambient Energy Aura ---
    function drawCenterAura(ctx) {
        const cx = W / 2;
        const cy = H / 2;
        const aura = ctx.createRadialGradient(cx, cy, 10, cx, cy, Math.max(W, H) * 0.45);
        aura.addColorStop(0, 'rgba(0, 50, 120, 0.15)');
        aura.addColorStop(0.3, 'rgba(0, 30, 80, 0.08)');
        aura.addColorStop(0.7, 'rgba(5, 10, 30, 0.04)');
        aura.addColorStop(1, 'transparent');

        ctx.fillStyle = aura;
        ctx.beginPath();
        ctx.arc(cx, cy, Math.max(W, H) * 0.45, 0, Math.PI * 2);
        ctx.fill();
    }

    // --- Main Animation Loop ---
    function animate() {
        ctx.clearRect(0, 0, W, H);

        // Background ambient aura
        drawCenterAura(ctx);

        // Update & draw micro particles
        microParticles.forEach(mp => {
            mp.update();
            mp.draw(ctx);
        });

        // Update particles
        particles.forEach(p => p.update());

        // Draw connection lines
        drawConnections(ctx);

        // Draw particles on top
        particles.forEach(p => p.draw(ctx));

        // Mouse energy flare
        drawMouseFlare(ctx);

        animationId = requestAnimationFrame(animate);
    }

    animate();

    // --- Visibility API: pause when tab is hidden ---
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            cancelAnimationFrame(animationId);
        } else {
            animate();
        }
    });
}

/* ============================================
   2. Password Eye Toggle
   ============================================ */
function initPasswordToggle() {
    const toggles = document.querySelectorAll('.toggle-password');
    toggles.forEach(toggle => {
        toggle.addEventListener('click', () => {
            const input = toggle.parentElement.querySelector('input');
            if (input) {
                const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
                input.setAttribute('type', type);
                toggle.classList.toggle('fa-eye');
                toggle.classList.toggle('fa-eye-slash');
            }
        });
    });
}

/* ============================================
   3. Option Tabs Switcher
   ============================================ */
function initOptionTabs() {
    const tabBtns = document.querySelectorAll('.option-tab-btn');
    tabBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const group = btn.closest('.option-tabs-group');
            if (group) {
                group.querySelectorAll('.option-tab-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
            }
        });
    });
}

/* ============================================
   4. Flash Message Auto-Dismiss
   ============================================ */
function initFlashDismiss() {
    const flashes = document.querySelectorAll('.flash-cyber-card');
    flashes.forEach(flash => {
        setTimeout(() => {
            flash.style.opacity = '0';
            flash.style.transform = 'translateX(50px)';
            flash.style.transition = 'all 0.4s ease';
            setTimeout(() => flash.remove(), 400);
        }, 5000);
    });
}

/* ============================================
   5. Mobile Navbar Toggle
   ============================================ */
function initNavbarMobile() {
    const toggler = document.querySelector('.cyber-nav-toggle');
    const menu = document.querySelector('.cyber-nav-menu');
    if (toggler && menu) {
        toggler.addEventListener('click', () => {
            menu.classList.toggle('mobile-open');
            toggler.classList.toggle('active');
        });
    }
}

/* ============================================
   6. Loading Overlay Controller
   ============================================ */
function showLoadingOverlay(message) {
    let overlay = document.getElementById('loading-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'loading-overlay';
        overlay.innerHTML = `
            <div class="loading-content">
                <div class="dna-spinner">
                    <div class="dna-helix"></div>
                    <div class="dna-helix delay"></div>
                </div>
                <p class="loading-text">${message || 'Analyzing Career Genome...'}</p>
                <div class="loading-progress">
                    <div class="loading-bar"></div>
                </div>
            </div>
        `;
        document.body.appendChild(overlay);
    }
    overlay.classList.add('visible');
}

function hideLoadingOverlay() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.classList.remove('visible');
    }
}

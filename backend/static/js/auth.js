/**
 * SkillDNA-AI — Authentication JavaScript
 * Handles login & registration forms, option tabs, and password strength
 */

document.addEventListener('DOMContentLoaded', () => {
    initAuthOptionTabs();
    initPasswordStrength();
});

/**
 * Handle Option Tabs in Login & Register forms
 * Toggles active class and sets hidden field value if present
 */
function initAuthOptionTabs() {
    const optionBtns = document.querySelectorAll('.option-tab-btn');
    optionBtns.forEach(btn => {
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

/**
 * Password strength indicator for registration form
 */
function initPasswordStrength() {
    const passwordInput = document.getElementById('password');
    const strengthBar = document.getElementById('strength-bar');

    if (!passwordInput || !strengthBar) return;

    passwordInput.addEventListener('input', () => {
        const val = passwordInput.value;
        let score = 0;

        if (val.length >= 8) score++;
        if (/[A-Z]/.test(val)) score++;
        if (/[a-z]/.test(val)) score++;
        if (/[0-9]/.test(val)) score++;
        if (/[^a-zA-Z0-9]/.test(val)) score++;

        const widthPercentage = Math.min((score / 5) * 100, 100);
        strengthBar.style.width = widthPercentage + '%';

        if (score <= 2) {
            strengthBar.style.backgroundColor = 'var(--rose-glow)';
        } else if (score <= 3) {
            strengthBar.style.backgroundColor = 'var(--amber-glow)';
        } else {
            strengthBar.style.backgroundColor = 'var(--emerald-glow)';
        }
    });
}

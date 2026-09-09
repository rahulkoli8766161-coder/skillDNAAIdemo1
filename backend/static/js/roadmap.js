/**
 * SkillDNA-AI — Roadmap Page JavaScript
 * Handles roadmap timeline expansion/collapse, priority filtering, and animations
 */

document.addEventListener('DOMContentLoaded', () => {
    initRoadmapTimeline();
    initRoadmapAnimations();
});

/**
 * Initialize roadmap stage expansion/collapse
 */
function initRoadmapTimeline() {
    const stages = document.querySelectorAll('.stage-content');

    stages.forEach(stage => {
        stage.addEventListener('click', () => {
            // Toggle expanded class
            const wasExpanded = stage.classList.contains('expanded');

            // Optionally collapse all other stages
            // stages.forEach(s => s.classList.remove('expanded'));

            if (wasExpanded) {
                stage.classList.remove('expanded');
            } else {
                stage.classList.add('expanded');
            }
        });
    });

    // Expand the first stage by default
    if (stages.length > 0) {
        stages[0].classList.add('expanded');
    }
}

/**
 * Animate roadmap elements on scroll
 */
function initRoadmapAnimations() {
    const stages = document.querySelectorAll('.roadmap-stage');
    const priorityGroups = document.querySelectorAll('.priority-group');
    const projectCards = document.querySelectorAll('.project-card');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    // Animate stages
    stages.forEach((stage, i) => {
        stage.style.opacity = '0';
        stage.style.transform = 'translateY(30px)';
        stage.style.transition = `all 0.6s ease ${i * 0.15}s`;
        observer.observe(stage);
    });

    // Animate priority groups
    priorityGroups.forEach((group, i) => {
        group.style.opacity = '0';
        group.style.transform = 'translateY(20px)';
        group.style.transition = `all 0.5s ease ${i * 0.1}s`;
        observer.observe(group);
    });

    // Animate project cards
    projectCards.forEach((card, i) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = `all 0.5s ease ${i * 0.1}s`;
        observer.observe(card);
    });
}

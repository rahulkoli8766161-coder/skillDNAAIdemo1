/**
 * SkillDNA-AI — Profile Page JavaScript
 * Handles dynamic skill tags, resume drag-and-drop upload, and form submission
 */

document.addEventListener('DOMContentLoaded', () => {
    initSkillTagInput();
    initResumeUpload();
    initProfileForm();
});

/**
 * Dynamic skill tag input
 * Handles adding skills via Enter key, comma, or clicking the "Add" button
 */
function initSkillTagInput() {
    const container = document.getElementById('skills-container');
    const hiddenInput = document.getElementById('hidden-skills-input');
    const skillInput = document.getElementById('skill-input');
    const addBtn = document.getElementById('add-skill-btn');

    if (!container || !hiddenInput || !skillInput) return;

    let skills = [];
    try {
        if (hiddenInput.value) {
            skills = JSON.parse(hiddenInput.value);
            if (!Array.isArray(skills)) skills = [];
        }
    } catch (e) {
        if (hiddenInput.value) {
            skills = hiddenInput.value.split(',').map(s => s.trim()).filter(s => s);
        }
    }

    // Function to add a new skill
    function addSkill(skillText) {
        const cleaned = skillText.trim().replace(/^,+|,+$/g, '');
        if (!cleaned) return;
        
        if (!skills.includes(cleaned)) {
            skills.push(cleaned);
            renderSkillTags();
            updateHiddenInput();
        }
        skillInput.value = '';
    }

    // Function to render all skill tags inside container
    function renderSkillTags() {
        container.innerHTML = '';
        skills.forEach((skill, index) => {
            const tag = document.createElement('span');
            tag.className = 'skill-pill-tag';
            tag.style.cssText = 'font-family: var(--font-cyber); font-size: 0.85rem; padding: 0.35rem 0.8rem; background: rgba(0, 240, 255, 0.12); border: 1px solid rgba(0, 240, 255, 0.3); border-radius: 9999px; color: var(--cyan-glow); display: inline-flex; align-items: center; gap: 0.4rem; transition: all 0.2s ease;';
            tag.innerHTML = `
                <span>${escapeHtml(skill)}</span>
                <i class="fa-solid fa-xmark remove-skill-tag" style="cursor: pointer; opacity: 0.7; transition: opacity 0.2s ease;" title="Remove"></i>
            `;

            // Remove tag click event
            tag.querySelector('.remove-skill-tag').addEventListener('click', (e) => {
                e.stopPropagation();
                skills.splice(index, 1);
                renderSkillTags();
                updateHiddenInput();
            });

            container.appendChild(tag);
        });
    }

    function updateHiddenInput() {
        hiddenInput.value = JSON.stringify(skills);
    }

    // Keydown event on skill input
    skillInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ',') {
            e.preventDefault();
            addSkill(skillInput.value);
        }
    });

    // Click event on Add button
    if (addBtn) {
        addBtn.addEventListener('click', (e) => {
            e.preventDefault();
            addSkill(skillInput.value);
        });
    }

    // Render initial tags if any
    renderSkillTags();
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

/**
 * Resume file upload with drag-and-drop & Browse button
 */
function initResumeUpload() {
    const dropzone = document.getElementById('resume-dropzone');
    const fileInput = document.getElementById('resume');
    const fileNameDisplay = document.getElementById('file-name-display');

    if (!dropzone || !fileInput) return;

    // Trigger file input click when dropzone is clicked
    dropzone.addEventListener('click', (e) => {
        if (e.target.tagName !== 'LABEL' && e.target.tagName !== 'INPUT') {
            fileInput.click();
        }
    });

    fileInput.addEventListener('change', () => {
        handleFileSelect(fileInput, fileNameDisplay);
    });

    // Drag and drop events
    dropzone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropzone.style.borderColor = 'var(--cyan-glow)';
        dropzone.style.background = 'rgba(0, 240, 255, 0.08)';
    });

    dropzone.addEventListener('dragleave', () => {
        dropzone.style.borderColor = 'var(--border-cyber)';
        dropzone.style.background = 'rgba(0, 240, 255, 0.03)';
    });

    dropzone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropzone.style.borderColor = 'var(--border-cyber)';
        dropzone.style.background = 'rgba(0, 240, 255, 0.03)';

        if (e.dataTransfer.files.length > 0) {
            fileInput.files = e.dataTransfer.files;
            handleFileSelect(fileInput, fileNameDisplay);
        }
    });
}

/**
 * Validate & display selected resume filename
 */
function handleFileSelect(fileInput, fileNameDisplay) {
    const file = fileInput.files[0];
    if (!file) return;

    const allowedExtensions = ['pdf', 'docx', 'txt'];
    const ext = file.name.split('.').pop().toLowerCase();
    const maxSize = 5 * 1024 * 1024; // 5MB

    if (!allowedExtensions.includes(ext)) {
        alert('Invalid file format. Please upload PDF, DOCX, or TXT file.');
        fileInput.value = '';
        if (fileNameDisplay) fileNameDisplay.style.display = 'none';
        return;
    }

    if (file.size > maxSize) {
        alert('File size exceeds 5MB limit.');
        fileInput.value = '';
        if (fileNameDisplay) fileNameDisplay.style.display = 'none';
        return;
    }

    if (fileNameDisplay) {
        fileNameDisplay.innerHTML = `<i class="fa-solid fa-file-contract"></i> Selected: <strong>${escapeHtml(file.name)}</strong> (${(file.size / 1024).toFixed(1)} KB)`;
        fileNameDisplay.style.display = 'block';
    }
}

/**
 * Profile form submit handling
 */
function initProfileForm() {
    const form = document.getElementById('profile-form');
    if (!form) return;

    form.addEventListener('submit', (e) => {
        const careerGoal = document.getElementById('career_goal');
        if (careerGoal && !careerGoal.value.trim()) {
            e.preventDefault();
            alert('Please specify your Target Career Goal.');
            careerGoal.focus();
        }
    });
}

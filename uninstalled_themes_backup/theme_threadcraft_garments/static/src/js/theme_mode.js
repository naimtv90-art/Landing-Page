/** @odoo-module **/

/**
 * THREADCRAFT Dark/Light Mode Controller
 * Persists theme mode to localStorage and dynamically toggles classes & icons.
 */

function applyTheme(mode) {
    const isDark = mode === 'dark';
    if (isDark) {
        document.documentElement.classList.add('tc-dark-mode');
        document.body.classList.add('tc-dark-mode');
    } else {
        document.documentElement.classList.remove('tc-dark-mode');
        document.body.classList.remove('tc-dark-mode');
    }

    const btn = document.getElementById('tc-theme-toggle');
    if (btn) {
        const icon = btn.querySelector('.tc-theme-icon');
        const label = btn.querySelector('.tc-theme-label');
        if (icon) {
            icon.className = isDark ? 'fa fa-sun-o tc-theme-icon text-warning' : 'fa fa-moon-o tc-theme-icon text-warning';
        }
        if (label) {
            label.textContent = isDark ? 'LIGHT' : 'DARK';
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const savedMode = localStorage.getItem('tc_theme_mode') || 'light';
    applyTheme(savedMode);

    const btn = document.getElementById('tc-theme-toggle');
    if (btn) {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const currentIsDark = document.documentElement.classList.contains('tc-dark-mode');
            const nextMode = currentIsDark ? 'light' : 'dark';
            localStorage.setItem('tc_theme_mode', nextMode);
            applyTheme(nextMode);
        });
    }
});

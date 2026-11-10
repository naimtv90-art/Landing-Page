/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.TcGeneralAnimations = publicWidget.Widget.extend({
    selector: '#wrapwrap',
    disabledInEditableMode: false,

    start() {
        this._super(...arguments);
        this.initScrollReveal();
    },

    initScrollReveal() {
        const revealElements = this.el.querySelectorAll('.tc-reveal-on-scroll');
        if (!revealElements.length) return;

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('tc-revealed');
                }
            });
        }, { threshold: 0.15 });

        revealElements.forEach(el => observer.observe(el));
    }
});

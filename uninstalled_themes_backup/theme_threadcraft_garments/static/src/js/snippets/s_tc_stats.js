/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.TcStatsCounters = publicWidget.Widget.extend({
    selector: '.s_tc_stats',
    disabledInEditableMode: false,

    start() {
        this._super(...arguments);
        this.counterEls = this.el.querySelectorAll('.tc-counter-val');
        if (!this.counterEls.length) return;

        this.hasAnimated = false;
        this.observer = new IntersectionObserver((entries) => {
            if (entries[0].isIntersecting && !this.hasAnimated) {
                this.hasAnimated = true;
                this.animateCounters();
            }
        }, { threshold: 0.25 });

        this.observer.observe(this.el);
    },

    animateCounters() {
        this.counterEls.forEach((counter) => {
            const target = parseInt(counter.getAttribute('data-target') || counter.textContent.replace(/[^0-9]/g, '') || '0', 10);
            if (!target) return;

            const duration = 1600;
            const steps = 30;
            const stepTime = duration / steps;
            const increment = target / steps;
            let current = 0;

            const timer = setInterval(() => {
                current += increment;
                if (current >= target) {
                    current = target;
                    clearInterval(timer);
                }
                counter.textContent = Math.round(current);
            }, stepTime);
        });
    },

    destroy() {
        if (this.observer) {
            this.observer.disconnect();
            this.observer = null;
        }
        this._super(...arguments);
    }
});

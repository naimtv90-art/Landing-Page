/** @odoo-module **/

import options from "@web_editor/js/editor/snippets.options";

options.registry.TcThemeOption = options.Class.extend({
    /**
     * Custom Website Builder Option for Threadcraft Sections
     */
    setSectionBg(previewMode, widgetValue, params) {
        this.$target.removeClass('tc-bg-light tc-bg-charcoal tc-bg-grid-dark tc-bg-grid-light');
        if (widgetValue) {
            this.$target.addClass(widgetValue);
        }
    },

    set3DSilhouette(previewMode, widgetValue, params) {
        if (widgetValue) {
            this.$target.attr('data-default-sil', widgetValue);
            const silBtn = this.$target[0].querySelector(`.btn-sil-toggle[data-sil="${widgetValue}"]`);
            if (silBtn) silBtn.click();
        }
    },
});

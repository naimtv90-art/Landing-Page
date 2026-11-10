/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.TcProductsArchive = publicWidget.Widget.extend({
    selector: '.s_tc_products',
    disabledInEditableMode: false,

    start() {
        this._super(...arguments);
        this.filterBtns = this.el.querySelectorAll('.tc-filter-btn');
        this.cards = this.el.querySelectorAll('.tc-product-col');

        this.filterBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const cat = e.currentTarget.getAttribute('data-category');
                this.filterCategory(cat);
            });
        });
    },

    filterCategory(cat) {
        this.filterBtns.forEach(b => {
            b.classList.toggle('active', b.getAttribute('data-category') === cat);
        });

        this.cards.forEach(card => {
            const cardCat = card.getAttribute('data-category');
            if (cat === 'all' || cardCat === cat) {
                card.style.display = '';
            } else {
                card.style.display = 'none';
            }
        });
    }
});

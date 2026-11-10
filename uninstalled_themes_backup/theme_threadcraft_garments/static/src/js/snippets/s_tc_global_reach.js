/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

export const DESTINATIONS_DATA = {
    'new-york': {
        city: 'New York, United States',
        region: 'AMERICAS',
        transit: '14 - 18 Days (Sea) / 3 Days (Air)',
        volume: '180,000 units/mo',
        port: 'Port of NY & NJ / JFK Intl Cargo',
        categories: 'Heavyweight Hoodies, Organic Tees, Selvedge'
    },
    'london': {
        city: 'London, United Kingdom',
        region: 'EUROPE',
        transit: '18 - 22 Days (Sea) / 2 Days (Air)',
        volume: '95,000 units/mo',
        port: 'Port of Southampton / London Gateway',
        categories: 'Tailored Knits, Luxury Outerwear, GOTS Basics'
    },
    'paris': {
        city: 'Paris, France',
        region: 'EUROPE',
        transit: '20 - 24 Days (Sea) / 2 Days (Air)',
        volume: '75,000 units/mo',
        port: 'Le Havre / Paris CDG',
        categories: 'Supima Polos, Artisanal Selvedge, Fleece'
    },
    'berlin': {
        city: 'Berlin, Germany',
        region: 'EUROPE',
        transit: '19 - 23 Days (Sea) / 2 Days (Air)',
        volume: '85,000 units/mo',
        port: 'Hamburg Port / Frankfurt Air Hub',
        categories: 'Technical Bombers, Recycled Activewear'
    },
    'tokyo': {
        city: 'Tokyo, Japan',
        region: 'ASIA-PACIFIC',
        transit: '10 - 14 Days (Sea) / 2 Days (Air)',
        volume: '65,000 units/mo',
        port: 'Port of Yokohama / Tokyo Haneda',
        categories: 'Shuttle Loom Selvedge, 300+ GSM Tees'
    },
    'sydney': {
        city: 'Sydney, Australia',
        region: 'ASIA-PACIFIC',
        transit: '12 - 16 Days (Sea) / 3 Days (Air)',
        volume: '50,000 units/mo',
        port: 'Port Botany / Sydney Kingsford',
        categories: 'Breathable Activewear, Organic Cotton Knits'
    },
    'dubai': {
        city: 'Dubai, United Arab Emirates',
        region: 'MIDDLE EAST',
        transit: '6 - 9 Days (Sea) / 1 Day (Air)',
        volume: '40,000 units/mo',
        port: 'Jebel Ali Port / Dubai Cargo Village',
        categories: 'Luxury Pique Polos, Corporate Casuals'
    }
};

publicWidget.registry.TcGlobalReach = publicWidget.Widget.extend({
    selector: '.s_tc_global_reach',
    disabledInEditableMode: false,

    start() {
        this._super(...arguments);
        this.destBtns = this.el.querySelectorAll('.tc-dest-btn');
        this.cityEl = this.el.querySelector('.tc-dest-city');
        this.regionEl = this.el.querySelector('.tc-dest-region');
        this.transitEl = this.el.querySelector('.tc-dest-transit');
        this.volumeEl = this.el.querySelector('.tc-dest-volume');
        this.portEl = this.el.querySelector('.tc-dest-port');
        this.catEl = this.el.querySelector('.tc-dest-categories');

        this.destBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const dest = e.currentTarget.getAttribute('data-dest');
                this.setDestination(dest);
            });
        });
    },

    setDestination(key) {
        const data = DESTINATIONS_DATA[key];
        if (!data) return;

        this.destBtns.forEach(b => {
            b.classList.toggle('active', b.getAttribute('data-dest') === key);
        });

        if (this.cityEl) this.cityEl.textContent = data.city;
        if (this.regionEl) this.regionEl.textContent = data.region;
        if (this.transitEl) this.transitEl.textContent = data.transit;
        if (this.volumeEl) this.volumeEl.textContent = data.volume;
        if (this.portEl) this.portEl.textContent = data.port;
        if (this.catEl) this.catEl.textContent = data.categories;
    }
});

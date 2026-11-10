/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

export const FACTORY_ZONES = {
    'SEC-01': {
        name: "AUTOMATED CNC CUTTING & SPREADING",
        desc: "Equipped with computerized high-ply fabric spreaders and Gerber Paragon CNC ultrasonic cutters operating in temperature and humidity stabilized cleanrooms.",
        machinery: "Gerber Paragon® Multi-Ply + Eastman Auto-Spreaders",
        capacity: "25,000 Panels / Day",
        level: "95% Automated"
    },
    'SEC-02': {
        name: "LEAN SYNCHRONOUS SEWING LINES",
        desc: "36 modular synchronous assembly lines utilizing programmable Juki direct-drive lockstitch, Pegasus 5-thread overlock, and Yamato flatlock machinery.",
        machinery: "Juki DDL-9000C + Pegasus EX Series + Yamato Flatlock",
        capacity: "18,500 Finished Units / Day",
        level: "78% Semi-Automated"
    },
    'SEC-03': {
        name: "ECO-DYEING & WASHING LABORATORY",
        desc: "State-of-the-art low liquor ratio (1:4) soft-flow dyeing vessels, Tonello ozone wash drums, and Jeanologia laser finishing booths for sustainable vintage washes.",
        machinery: "Thies iMaster® Soft Flow + Tonello Ozone + Jeanologia Laser",
        capacity: "12,000 kg Fabric / Day",
        level: "90% Automated"
    },
    'SEC-04': {
        name: "PHYSICAL TESTING & SPECTROMETRY LAB",
        desc: "ISO 17025 accredited laboratory conducting continuous physical, chemical, and dimensional compliance verifications.",
        machinery: "Datacolor 800 Spectrophotometer + Martindale Tester",
        capacity: "350 Test Batches / Day",
        level: "85% Automated"
    },
    'SEC-05': {
        name: "STEAM TUNNEL FINISHING & RFID PACKING",
        desc: "Veit steam tunnel finishers paired with automated folding, polybagging, and item-level EPC Gen 2 RFID encoding for instant retail distribution.",
        machinery: "Veit 8326 Continuous Steam Tunnel + Beck Automated Bagging",
        capacity: "22,000 Packed Cartons / Day",
        level: "92% Automated"
    }
};

publicWidget.registry.TcFactoryHotspots = publicWidget.Widget.extend({
    selector: '.s_tc_factory',
    disabledInEditableMode: false,

    start() {
        this._super(...arguments);
        this.zoneBtns = this.el.querySelectorAll('.tc-factory-btn');
        this.nameEl = this.el.querySelector('.tc-zone-name');
        this.descEl = this.el.querySelector('.tc-zone-desc');
        this.codeEl = this.el.querySelector('.tc-zone-code');
        this.machineryEl = this.el.querySelector('.tc-zone-machinery');
        this.capEl = this.el.querySelector('.tc-zone-capacity');
        this.levelEl = this.el.querySelector('.tc-zone-level');

        this.zoneBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const code = e.currentTarget.getAttribute('data-code');
                this.setZone(code);
            });
        });
    },

    setZone(code) {
        const data = FACTORY_ZONES[code];
        if (!data) return;

        this.zoneBtns.forEach(b => {
            b.classList.toggle('active', b.getAttribute('data-code') === code);
        });

        if (this.nameEl) this.nameEl.textContent = data.name;
        if (this.descEl) this.descEl.textContent = data.desc;
        if (this.codeEl) this.codeEl.textContent = code;
        if (this.machineryEl) this.machineryEl.textContent = data.machinery;
        if (this.capEl) this.capEl.textContent = data.capacity;
        if (this.levelEl) this.levelEl.textContent = data.level;
    }
});

/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

export const STAGES_DATA = [
    {
        step: "01",
        title: "RAW MATERIAL SOURCING",
        tagline: "GOTS & BCI VERIFIED SUSTAINABLE FIBERS",
        description: "Direct partnership with certified regenerative farms. Extra-long staple organic cotton, traceable merino wool, and recycled sea-waste polyester verified with DNA molecular markers.",
        metricLabel: "Traceability Index",
        metricVal: "100% DNA Verified",
        img: "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?auto=format&fit=crop&w=1200&q=80"
    },
    {
        step: "02",
        title: "FABRIC DEVELOPMENT & SPINNING",
        tagline: "HIGH-GAUGE KNITTING & SHUTTLE LOOM PRECISION",
        description: "Custom yarn spinning from 16s to 120/2s counts. In-house circular knitting machines and shuttle looms develop bespoke textures: French terry, double pique, and technical interlock.",
        metricLabel: "Fabric Library",
        metricVal: "450+ Custom Weaves",
        img: "https://images.unsplash.com/photo-1584917865442-de89df76afd3?auto=format&fit=crop&w=1200&q=80"
    },
    {
        step: "03",
        title: "DIGITAL PATTERN & 3D CLO LAB",
        tagline: "VIRTUAL PROTOTYPING & ZERO-WASTE MARKER MAKING",
        description: "Digital 3D fit visualization in CLO 3D eliminates physical sample waste. AI-driven nesting algorithms optimize marker utilization to exceed 92% fabric efficiency.",
        metricLabel: "Fabric Yield Efficiency",
        metricVal: "92.4% Average",
        img: "https://images.unsplash.com/photo-1558769132-cb1aea458c5e?auto=format&fit=crop&w=1200&q=80"
    },
    {
        step: "04",
        title: "PRECISION CUTTING & AUTOMATED SEWING",
        tagline: "ULTRASONIC CNC CUTTERS & ERGONOMIC LINES",
        description: "Automated multi-ply Gerber vacuum cutters achieve sub-millimeter precision. Dedicated lean production lines equipped with automated Juki and Brother lockstitch machinery.",
        metricLabel: "Sewing Accuracy",
        metricVal: "±0.5 mm Tolerance",
        img: "https://images.unsplash.com/photo-1528698827591-e19ccd7bc23d?auto=format&fit=crop&w=1200&q=80"
    },
    {
        step: "05",
        title: "MULTI-POINT QUALITY INSPECTION",
        tagline: "AQL 1.5 STRICT INSPECTION & SPECTROMETRY",
        description: "Comprehensive 4-point fabric inspection, spectrophotometer color matching, bursting strength tests, and metal detection ensure zero-defect shipment integrity.",
        metricLabel: "Defect Rate",
        metricVal: "< 0.38% (AQL 1.5)",
        img: "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&w=1200&q=80"
    },
    {
        step: "06",
        title: "FINISHING, RFID & GLOBAL EXPORT",
        tagline: "ECO-PRESSING, AUTOMATED BOXING & BONDED FREIGHT",
        description: "Tunnel steaming, robotic RFID tagging for retail floor readiness, and climate-controlled container packing. Direct bonded air and sea freight logistics reaching 30+ international ports.",
        metricLabel: "On-Time Export Delivery",
        metricVal: "98.6% Historical",
        img: "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?auto=format&fit=crop&w=1200&q=80"
    }
];

publicWidget.registry.TcManufacturingStory = publicWidget.Widget.extend({
    selector: '.s_tc_manufacturing_story',
    disabledInEditableMode: false,

    start() {
        this._super(...arguments);
        this.currentStep = 0;

        this.stagePills = this.el.querySelectorAll('.tc-stage-pill');
        this.titleEl = this.el.querySelector('.tc-stage-title');
        this.taglineEl = this.el.querySelector('.tc-stage-tagline');
        this.descEl = this.el.querySelector('.tc-stage-desc');
        this.stepEl = this.el.querySelector('.tc-stage-step-num');
        this.imgEl = this.el.querySelector('.tc-stage-image');
        this.metricLabelEl = this.el.querySelector('.tc-metric-label');
        this.metricValEl = this.el.querySelector('.tc-metric-val');

        // Nav click
        this.stagePills.forEach((pill, idx) => {
            pill.addEventListener('click', () => {
                this.setStage(idx);
            });
        });

        const prevBtn = this.el.querySelector('.btn-prev-stage');
        if (prevBtn) {
            prevBtn.addEventListener('click', () => {
                const next = (this.currentStep > 0) ? this.currentStep - 1 : STAGES_DATA.length - 1;
                this.setStage(next);
            });
        }

        const nextBtn = this.el.querySelector('.btn-next-stage');
        if (nextBtn) {
            nextBtn.addEventListener('click', () => {
                const next = (this.currentStep < STAGES_DATA.length - 1) ? this.currentStep + 1 : 0;
                this.setStage(next);
            });
        }
    },

    setStage(idx) {
        this.currentStep = idx;
        const data = STAGES_DATA[idx];
        if (!data) return;

        this.stagePills.forEach((p, i) => {
            p.classList.toggle('active', i === idx);
        });

        if (this.titleEl) this.titleEl.textContent = data.title;
        if (this.taglineEl) this.taglineEl.textContent = data.tagline;
        if (this.descEl) this.descEl.textContent = data.description;
        if (this.stepEl) this.stepEl.textContent = data.step;
        if (this.imgEl) this.imgEl.src = data.img;
        if (this.metricLabelEl) this.metricLabelEl.textContent = data.metricLabel;
        if (this.metricValEl) this.metricValEl.textContent = data.metricVal;
    }
});

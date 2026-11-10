/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { Threadcraft3DGarment } from "../three_scene";

publicWidget.registry.TcHero3D = publicWidget.Widget.extend({
    selector: '.s_tc_hero',
    disabledInEditableMode: false,

    start() {
        this._super(...arguments);
        this.canvasContainer = this.el.querySelector('.tc-hero-canvas-container');
        if (!this.canvasContainer) return;

        // Clean out any dummy canvas element
        const dummyCanvas = this.canvasContainer.querySelector('canvas');
        if (dummyCanvas) dummyCanvas.remove();

        // Initialize 3D Engine
        this.engine = new Threadcraft3DGarment(this.canvasContainer, {
            silhouette: 'tshirt',
            color: '#171717',
            wireframe: false,
        });

        // Silhouette buttons
        this.el.querySelectorAll('[data-silhouette], .btn-sil-toggle').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const sil = e.currentTarget.getAttribute('data-silhouette') || e.currentTarget.getAttribute('data-sil');
                this.el.querySelectorAll('[data-silhouette], .btn-sil-toggle').forEach(b => {
                    b.classList.remove('active', 'btn-dark');
                    b.classList.add('btn-outline-dark');
                });
                e.currentTarget.classList.add('active', 'btn-dark');
                e.currentTarget.classList.remove('btn-outline-dark');
                if (this.engine && sil) this.engine.setSilhouette(sil);
            });
        });

        // Colorway swatches
        this.el.querySelectorAll('[data-color], .tc-swatch').forEach(swatch => {
            swatch.addEventListener('click', (e) => {
                e.preventDefault();
                const color = e.currentTarget.getAttribute('data-color');
                this.el.querySelectorAll('[data-color], .tc-swatch').forEach(s => {
                    s.classList.remove('border-2', 'border-dark', 'active');
                });
                e.currentTarget.classList.add('border-2', 'border-dark', 'active');
                if (this.engine && color) this.engine.setColor(color);
            });
        });

        // CAD Wireframe toggle
        const cadBtn = this.el.querySelector('[data-toggle-cad], .btn-cad-toggle');
        if (cadBtn) {
            this.isWireframe = false;
            cadBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.isWireframe = !this.isWireframe;
                cadBtn.classList.toggle('active', this.isWireframe);
                cadBtn.innerHTML = this.isWireframe 
                    ? '<i class="fa fa-codepen me-1 text-success"/> CAD: ACTIVE' 
                    : '<i class="fa fa-codepen me-1"/> CAD WIREFRAME';
                if (this.engine) this.engine.setWireframe(this.isWireframe);
            });
        }
    },

    destroy() {
        if (this.engine) {
            this.engine.destroy();
            this.engine = null;
        }
        this._super(...arguments);
    }
});

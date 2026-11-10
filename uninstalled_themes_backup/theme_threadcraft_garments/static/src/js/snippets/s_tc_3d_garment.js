/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { Threadcraft3DGarment } from "../three_scene";

publicWidget.registry.Tc3DGarmentShowcase = publicWidget.Widget.extend({
    selector: '.s_tc_3d_garment',
    disabledInEditableMode: false,

    start() {
        this._super(...arguments);
        this.canvasContainer = this.el.querySelector('.tc-3d-canvas-container, .tc-3d-canvas-box');
        if (!this.canvasContainer) return;

        // Clean out any dummy canvas
        const dummy = this.canvasContainer.querySelector('canvas');
        if (dummy) dummy.remove();

        const defaultSil = this.canvasContainer.getAttribute('data-silhouette') || 'hoodie';
        const defaultColor = this.canvasContainer.getAttribute('data-color') || '#C7F36B';

        this.engine = new Threadcraft3DGarment(this.canvasContainer, {
            silhouette: defaultSil,
            color: defaultColor,
            wireframe: false,
        });

        // Color clicks
        this.el.querySelectorAll('[data-color], .tc-swatch').forEach(swatch => {
            swatch.addEventListener('click', (e) => {
                e.preventDefault();
                const color = e.currentTarget.getAttribute('data-color');
                this.el.querySelectorAll('[data-color], .tc-swatch').forEach(s => {
                    s.classList.remove('border-white', 'border-2', 'active');
                    s.classList.add('border-secondary');
                });
                e.currentTarget.classList.add('border-white', 'border-2', 'active');
                e.currentTarget.classList.remove('border-secondary');
                if (this.engine && color) this.engine.setColor(color);
            });
        });

        // Silhouette clicks
        this.el.querySelectorAll('[data-silhouette], .btn-sil-toggle').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const sil = e.currentTarget.getAttribute('data-silhouette') || e.currentTarget.getAttribute('data-sil');
                this.el.querySelectorAll('[data-silhouette], .btn-sil-toggle').forEach(b => {
                    b.classList.remove('active');
                });
                e.currentTarget.classList.add('active');
                if (this.engine && sil) this.engine.setSilhouette(sil);
            });
        });

        // Wireframe toggle
        const cadBtn = this.el.querySelector('[data-toggle-cad], .btn-cad-toggle');
        if (cadBtn) {
            this.isWireframe = false;
            cadBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.isWireframe = !this.isWireframe;
                cadBtn.classList.toggle('active', this.isWireframe);
                cadBtn.innerHTML = this.isWireframe 
                    ? '<i class="fa fa-cubes me-1 text-success"/> WIREFRAME: ON' 
                    : '<i class="fa fa-cubes me-1"/> WIREFRAME TOGGLE';
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

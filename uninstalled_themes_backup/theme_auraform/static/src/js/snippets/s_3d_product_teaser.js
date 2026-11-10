/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

export const AuraForm3DProductTeaser = publicWidget.Widget.extend({
    selector: '.s_3d_product_teaser',

    /**
     * @override
     */
    start: function () {
        this._super.apply(this, arguments);
        this.canvases = this.el.querySelectorAll('.teaser-canvas-wrapper');
        this.scenes = [];

        if (window.THREE) {
            this._initTeasers();
        } else {
            setTimeout(() => {
                if (window.THREE) this._initTeasers();
            }, 300);
        }
    },

    _initTeasers: function () {
        const THREE = window.THREE;

        this.canvases.forEach((container, idx) => {
            const width = container.clientWidth || 300;
            const height = container.clientHeight || 280;

            const scene = new THREE.Scene();
            const camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 50);
            camera.position.set(2.0, 1.2, 2.0);
            camera.lookAt(0, 0.4, 0);

            const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
            renderer.setSize(width, height);
            renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
            container.appendChild(renderer.domElement);

            // Light
            const amb = new THREE.AmbientLight(0xffffff, 0.7);
            const dir = new THREE.DirectionalLight(0xffffff, 1.4);
            dir.position.set(3, 5, 3);
            scene.add(amb);
            scene.add(dir);

            // Mini Chair
            const meshGroup = new THREE.Group();
            const hexColors = [0x17181c, 0x1e2e4a, 0x8a4533];
            const color = hexColors[idx % hexColors.length];

            const mat = new THREE.MeshStandardMaterial({ color: color, roughness: 0.8 });
            const seat = new THREE.Mesh(new THREE.BoxGeometry(0.48, 0.08, 0.46), mat);
            seat.position.set(0, 0.6, 0);
            meshGroup.add(seat);

            const back = new THREE.Mesh(new THREE.BoxGeometry(0.44, 0.58, 0.03), mat);
            back.position.set(0, 1.0, -0.2);
            meshGroup.add(back);

            const baseMat = new THREE.MeshStandardMaterial({ color: 0x18191c, metalness: 0.8, roughness: 0.3 });
            const hub = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.1, 0.5, 16), baseMat);
            hub.position.set(0, 0.25, 0);
            meshGroup.add(hub);

            scene.add(meshGroup);

            this.scenes.push({ scene, camera, renderer, meshGroup });
        });

        this._animate();
    },

    _animate: function () {
        this.animId = requestAnimationFrame(this._animate.bind(this));
        this.scenes.forEach((item) => {
            item.meshGroup.rotation.y += 0.01;
            item.renderer.render(item.scene, item.camera);
        });
    },

    /**
     * @override
     */
    destroy: function () {
        if (this.animId) cancelAnimationFrame(this.animId);
        this.scenes.forEach((item) => {
            if (item.renderer) item.renderer.dispose();
        });
        this._super.apply(this, arguments);
    },
});

publicWidget.registry.AuraForm3DProductTeaser = AuraForm3DProductTeaser;

/** @odoo-module **/

/**
 * THREADCRAFT 3D WebGL Engine
 * Self-contained Three.js renderer for Garments, Factory Twin, and Global Logistics.
 * Directly derived from GarmentMesh.tsx with studio lighting, realistic geometry,
 * interactive orbit drag, and responsive resize.
 */

export class Threadcraft3DGarment {
    constructor(containerEl, options = {}) {
        this.container = containerEl;
        this.options = Object.assign({
            silhouette: 'tshirt',
            color: '#EDE9E1',
            wireframe: false,
            autoRotate: true,
        }, options);

        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.garmentGroup = null;
        this.animFrameId = null;
        this.isDestroyed = false;

        this.init();
    }

    init() {
        if (!window.THREE || !this.container) return;

        // Clean out any existing canvas or elements
        const existingCanvases = this.container.querySelectorAll('canvas');
        existingCanvases.forEach(c => c.remove());

        const width = this.container.clientWidth || 600;
        const height = this.container.clientHeight || 500;

        // Scene
        this.scene = new window.THREE.Scene();

        // Camera - matched with GarmentMesh perspective
        this.camera = new window.THREE.PerspectiveCamera(42, width / height, 0.1, 100);
        this.camera.position.set(0, 0.35, 4.2);

        // WebGL Renderer
        this.renderer = new window.THREE.WebGLRenderer({
            antialias: true,
            alpha: true,
            powerPreference: 'high-performance'
        });
        this.renderer.setSize(width, height);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = window.THREE.PCFSoftShadowMap;

        // Ensure canvas fills container
        this.renderer.domElement.style.cssText = 'position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: block; z-index: 1; pointer-events: auto;';
        this.container.appendChild(this.renderer.domElement);

        // Studio Fashion Lighting (matched with HeroGarmentScene.tsx)
        const ambientLight = new window.THREE.AmbientLight(0xffffff, 0.75);
        this.scene.add(ambientLight);

        // Key light
        const keyLight = new window.THREE.DirectionalLight(0xffffff, 1.2);
        keyLight.position.set(4, 5, 5);
        keyLight.castShadow = true;
        this.scene.add(keyLight);

        // Fill light
        const fillLight = new window.THREE.DirectionalLight(0xe2e8f0, 0.5);
        fillLight.position.set(-4, 2, 3);
        this.scene.add(fillLight);

        // Electric Lime high-fashion rim light
        const rimLight = new window.THREE.SpotLight(0xC7F36B, 2.2);
        rimLight.position.set(0, 6, -4);
        rimLight.angle = 0.6;
        rimLight.penumbra = 0.9;
        this.scene.add(rimLight);

        // Soft bounce light
        const bounceLight = new window.THREE.PointLight(0xffffff, 0.35);
        bounceLight.position.set(0, -2, 2);
        this.scene.add(bounceLight);

        // Garment Group
        this.garmentGroup = new window.THREE.Group();
        this.scene.add(this.garmentGroup);

        this.buildGarment();

        // Window resize
        this.onResize = () => {
            if (!this.container || !this.renderer || !this.camera) return;
            const w = this.container.clientWidth;
            const h = this.container.clientHeight;
            if (w === 0 || h === 0) return;
            this.camera.aspect = w / h;
            this.camera.updateProjectionMatrix();
            this.renderer.setSize(w, h);
        };
        window.addEventListener('resize', this.onResize);

        // Mouse & Touch interaction
        this.setupInteraction();

        // Start render loop
        this.render();
    }

    buildGarment() {
        if (!this.garmentGroup) return;

        // Clear previous meshes
        while (this.garmentGroup.children.length > 0) {
            const obj = this.garmentGroup.children[0];
            if (obj.geometry) obj.geometry.dispose();
            if (obj.material) {
                if (Array.isArray(obj.material)) obj.material.forEach(m => m.dispose());
                else obj.material.dispose();
            }
            this.garmentGroup.remove(obj);
        }

        const color = new window.THREE.Color(this.options.color);
        const material = new window.THREE.MeshStandardMaterial({
            color: color,
            roughness: 0.85,
            metalness: 0.05,
            wireframe: this.options.wireframe,
            side: window.THREE.DoubleSide,
        });

        const darkMat = new window.THREE.MeshStandardMaterial({
            color: 0x1f1f1f,
            roughness: 0.6,
            wireframe: this.options.wireframe,
        });

        const limeMat = new window.THREE.MeshStandardMaterial({
            color: 0xC7F36B,
            emissive: 0xC7F36B,
            emissiveIntensity: 0.4,
            roughness: 0.3,
            wireframe: this.options.wireframe,
        });

        const sil = this.options.silhouette;

        if (sil === 'hoodie') {
            // ==================== HOODIE ====================
            const group = new window.THREE.Group();
            group.scale.set(1.15, 1.15, 1.15);
            group.position.set(0, -0.15, 0);

            // Main Torso
            const torso = new window.THREE.Mesh(new window.THREE.CylinderGeometry(1.02, 1.12, 2.2, 32, 16, true), material);
            group.add(torso);

            // Upper Chest
            const chest = new window.THREE.Mesh(new window.THREE.CylinderGeometry(0.62, 1.02, 0.45, 32, 8, true), material);
            chest.position.set(0, 1.25, 0);
            group.add(chest);

            // Hood Dome
            const hood = new window.THREE.Mesh(new window.THREE.SphereGeometry(0.72, 32, 24, 0, Math.PI * 2, 0, Math.PI * 0.75), material);
            hood.position.set(0, 1.45, -0.12);
            group.add(hood);

            // Hood Opening Trim
            const trim = new window.THREE.Mesh(new window.THREE.TorusGeometry(0.55, 0.06, 16, 32), darkMat);
            trim.position.set(0, 1.42, 0.25);
            group.add(trim);

            // Kangaroo Front Pocket
            const pocket = new window.THREE.Mesh(new window.THREE.BoxGeometry(1.1, 0.7, 0.2), material);
            pocket.position.set(0, -0.3, 1.05);
            group.add(pocket);

            // Left Long Sleeve
            const leftArm = new window.THREE.Mesh(new window.THREE.CylinderGeometry(0.34, 0.42, 1.85, 24, 8, true), material);
            leftArm.position.set(-1.25, 0.25, 0);
            leftArm.rotation.z = 0.52;
            group.add(leftArm);

            // Right Long Sleeve
            const rightArm = new window.THREE.Mesh(new window.THREE.CylinderGeometry(0.34, 0.42, 1.85, 24, 8, true), material);
            rightArm.position.set(1.25, 0.25, 0);
            rightArm.rotation.z = -0.52;
            group.add(rightArm);

            // Waist Ribbed Hem
            const hem = new window.THREE.Mesh(new window.THREE.CylinderGeometry(1.08, 1.08, 0.22, 32), darkMat);
            hem.position.set(0, -1.2, 0);
            group.add(hem);

            this.garmentGroup.add(group);

        } else if (sil === 'polo' || sil === 'jacket') {
            // ==================== POLO SHIRT ====================
            const group = new window.THREE.Group();
            group.scale.set(1.25, 1.25, 1.25);
            group.position.set(0, -0.2, 0);

            // Main Torso
            const torso = new window.THREE.Mesh(new window.THREE.CylinderGeometry(0.9, 0.96, 2.05, 32, 16, true), material);
            group.add(torso);

            // Upper Chest
            const chest = new window.THREE.Mesh(new window.THREE.CylinderGeometry(0.55, 0.9, 0.35, 32, 8, true), material);
            chest.position.set(0, 1.1, 0);
            group.add(chest);

            // Flat-Knit Pique Collar
            const collar = new window.THREE.Mesh(new window.THREE.CylinderGeometry(0.52, 0.62, 0.2, 28, 4, true), darkMat);
            collar.position.set(0, 1.28, 0);
            group.add(collar);

            // Front Button Placket
            const placket = new window.THREE.Mesh(new window.THREE.BoxGeometry(0.2, 0.65, 0.04), darkMat);
            placket.position.set(0, 0.88, 0.94);
            group.add(placket);

            // Buttons
            for (let i = 0; i < 3; i++) {
                const btn = new window.THREE.Mesh(new window.THREE.CylinderGeometry(0.035, 0.035, 0.02, 16), limeMat);
                btn.rotation.x = Math.PI / 2;
                btn.position.set(0, 1.08 - (i * 0.18), 0.97);
                group.add(btn);
            }

            // Short Sleeves
            const leftArm = new window.THREE.Mesh(new window.THREE.CylinderGeometry(0.35, 0.38, 0.8, 24, 6, true), material);
            leftArm.position.set(-1.05, 0.7, 0);
            leftArm.rotation.z = 0.58;
            group.add(leftArm);

            const rightArm = new window.THREE.Mesh(new window.THREE.CylinderGeometry(0.35, 0.38, 0.8, 24, 6, true), material);
            rightArm.position.set(1.05, 0.7, 0);
            rightArm.rotation.z = -0.58;
            group.add(rightArm);

            this.garmentGroup.add(group);

        } else {
            // ==================== FLAGSHIP T-SHIRT ====================
            const group = new window.THREE.Group();
            group.scale.set(1.3, 1.3, 1.3);
            group.position.set(0, -0.2, 0);

            // Main Torso Cylinder
            const torso = new window.THREE.Mesh(new window.THREE.CylinderGeometry(0.9, 0.98, 2.0, 32, 16, true), material);
            torso.castShadow = true;
            torso.receiveShadow = true;
            group.add(torso);

            // Upper Chest & Shoulder Slope
            const chest = new window.THREE.Mesh(new window.THREE.CylinderGeometry(0.55, 0.9, 0.35, 32, 8, true), material);
            chest.position.set(0, 1.05, 0);
            group.add(chest);

            // Chunky Ribbed Neckline Collar
            const collar = new window.THREE.Mesh(new window.THREE.TorusGeometry(0.52, 0.07, 16, 40), material);
            collar.position.set(0, 1.22, 0);
            group.add(collar);

            // Left Drop Shoulder Sleeve
            const leftArm = new window.THREE.Mesh(new window.THREE.CylinderGeometry(0.34, 0.38, 0.85, 24, 8, true), material);
            leftArm.position.set(-1.08, 0.65, 0);
            leftArm.rotation.z = 0.62;
            group.add(leftArm);

            // Right Drop Shoulder Sleeve
            const rightArm = new window.THREE.Mesh(new window.THREE.CylinderGeometry(0.34, 0.38, 0.85, 24, 8, true), material);
            rightArm.position.set(1.08, 0.65, 0);
            rightArm.rotation.z = -0.62;
            group.add(rightArm);

            // Sleeve Cuffs
            const leftCuff = new window.THREE.Mesh(new window.THREE.TorusGeometry(0.34, 0.04, 12, 24), darkMat);
            leftCuff.position.set(-1.42, 0.32, 0);
            leftCuff.rotation.z = 0.62;
            group.add(leftCuff);

            const rightCuff = new window.THREE.Mesh(new window.THREE.TorusGeometry(0.34, 0.04, 12, 24), darkMat);
            rightCuff.position.set(1.42, 0.32, 0);
            rightCuff.rotation.z = -0.62;
            group.add(rightCuff);

            // Bottom Hem
            const hem = new window.THREE.Mesh(new window.THREE.TorusGeometry(0.98, 0.04, 12, 32), darkMat);
            hem.position.set(0, -1.0, 0);
            group.add(hem);

            // Brand Accent Label Stitch on Hem
            const tag = new window.THREE.Mesh(new window.THREE.BoxGeometry(0.12, 0.22, 0.02), limeMat);
            tag.position.set(0.6, -0.92, 0.98);
            group.add(tag);

            this.garmentGroup.add(group);
        }
    }

    setupInteraction() {
        let isDragging = false;
        let previousMouseX = 0;

        const onMouseDown = (e) => {
            isDragging = true;
            previousMouseX = e.clientX;
        };

        const onMouseMove = (e) => {
            if (!isDragging || !this.garmentGroup) return;
            const deltaX = e.clientX - previousMouseX;
            this.garmentGroup.rotation.y += deltaX * 0.008;
            previousMouseX = e.clientX;
        };

        const onMouseUp = () => {
            isDragging = false;
        };

        this.container.addEventListener('mousedown', onMouseDown);
        window.addEventListener('mousemove', onMouseMove);
        window.addEventListener('mouseup', onMouseUp);

        // Touch support for mobile
        let previousTouchX = 0;
        this.container.addEventListener('touchstart', (e) => {
            if (e.touches.length === 1) {
                isDragging = true;
                previousTouchX = e.touches[0].clientX;
            }
        });
        window.addEventListener('touchmove', (e) => {
            if (!isDragging || !this.garmentGroup || e.touches.length !== 1) return;
            const deltaX = e.touches[0].clientX - previousTouchX;
            this.garmentGroup.rotation.y += deltaX * 0.01;
            previousTouchX = e.touches[0].clientX;
        });
        window.addEventListener('touchend', () => { isDragging = false; });
    }

    setColor(hex) {
        this.options.color = hex;
        this.buildGarment();
    }

    setSilhouette(sil) {
        this.options.silhouette = sil;
        this.buildGarment();
    }

    setWireframe(enabled) {
        this.options.wireframe = enabled;
        this.buildGarment();
    }

    render() {
        if (this.isDestroyed) return;

        if (this.garmentGroup && this.options.autoRotate) {
            this.garmentGroup.rotation.y += 0.004;
            this.garmentGroup.position.y = Math.sin(Date.now() * 0.002) * 0.06;
        }

        if (this.renderer && this.scene && this.camera) {
            this.renderer.render(this.scene, this.camera);
        }

        this.animFrameId = requestAnimationFrame(() => this.render());
    }

    destroy() {
        this.isDestroyed = true;
        if (this.animFrameId) cancelAnimationFrame(this.animFrameId);
        if (this.onResize) window.removeEventListener('resize', this.onResize);
        if (this.renderer && this.renderer.domElement && this.renderer.domElement.parentNode) {
            this.renderer.domElement.parentNode.removeChild(this.renderer.domElement);
        }
        if (this.renderer) this.renderer.dispose();
    }
}

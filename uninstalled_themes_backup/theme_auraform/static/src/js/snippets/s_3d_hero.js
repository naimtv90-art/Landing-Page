/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

export const AuraForm3DHero = publicWidget.Widget.extend({
    selector: '.s_3d_hero',
    events: {
        'click .js_quick_color': '_onQuickColorClick',
        'click .js_turntable_toggle': '_onTurntableToggle',
    },

    /**
     * @override
     */
    start: function () {
        this._super.apply(this, arguments);
        if (!this.el) return;
        this.container = this.el.querySelector('.hero-3d-stage');
        if (!this.container) return;

        this.autoRotate = true;
        this.currentHex = '#17181c';
        this.targetColor = null;

        if (window.THREE) {
            this._initThreeScene();
        } else {
            console.warn('[AuraForm 3D] Three.js not found on window. Retrying...');
            setTimeout(() => {
                if (window.THREE) this._initThreeScene();
            }, 300);
        }
    },

    /**
     * Initialize Three.js WebGL Scene
     */
    _initThreeScene: function () {
        const THREE = window.THREE;
        const width = this.container.clientWidth || 500;
        const height = this.container.clientHeight || 500;

        // 1. Scene & Camera
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 100);
        this.camera.position.set(2.4, 1.4, 2.4);

        // 2. WebGL Renderer
        this.renderer = new THREE.WebGLRenderer({
            antialias: true,
            alpha: true,
            powerPreference: 'high-performance',
        });
        this.renderer.setSize(width, height);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        this.container.appendChild(this.renderer.domElement);

        // Remove loading spinner
        const loader = this.container.querySelector('.af-3d-loader');
        if (loader) loader.remove();

        // 3. OrbitControls
        if (THREE.OrbitControls) {
            this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
            this.controls.enableDamping = true;
            this.controls.dampingFactor = 0.05;
            this.controls.maxPolarAngle = Math.PI / 2.05; // Prevent under-floor clipping
            this.controls.minDistance = 1.4;
            this.controls.maxDistance = 5.0;
            this.controls.target.set(0, 0.45, 0);
        }

        // 4. Lights
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.65);
        this.scene.add(ambientLight);

        const keyLight = new THREE.DirectionalLight(0xffffff, 1.5);
        keyLight.position.set(5, 8, 4);
        keyLight.castShadow = true;
        keyLight.shadow.mapSize.width = 1024;
        keyLight.shadow.mapSize.height = 1024;
        this.scene.add(keyLight);

        const fillLight = new THREE.DirectionalLight(0x93c5fd, 0.8);
        fillLight.position.set(-5, 4, -3);
        this.scene.add(fillLight);

        // 5. Contact Shadow Plane
        const shadowGeo = new THREE.PlaneGeometry(6, 6);
        const shadowMat = new THREE.ShadowMaterial({ opacity: 0.35 });
        const shadowPlane = new THREE.Mesh(shadowGeo, shadowMat);
        shadowPlane.rotation.x = -Math.PI / 2;
        shadowPlane.position.y = -0.4;
        shadowPlane.receiveShadow = true;
        this.scene.add(shadowPlane);

        // 6. Build Chair Model
        this._buildProceduralChair();

        // 7. Mouse Parallax listener
        this._onMouseMove = this._handleMouseMove.bind(this);
        window.addEventListener('mousemove', this._onMouseMove);

        // 8. Resize listener
        this._onResize = this._handleResize.bind(this);
        window.addEventListener('resize', this._onResize);

        // 9. Render Loop
        this.targetColor = new THREE.Color(this.currentHex);
        this._animate();
    },

    /**
     * Procedural High-Fidelity Ergonomic Chair Assembly
     */
    _buildProceduralChair: function () {
        const THREE = window.THREE;
        this.chairGroup = new THREE.Group();
        this.chairGroup.position.set(0, -0.4, 0);

        // PBR Materials
        this.fabricMaterial = new THREE.MeshStandardMaterial({
            color: this.currentHex,
            roughness: 0.85,
            metalness: 0.1,
        });

        this.frameMaterial = new THREE.MeshStandardMaterial({
            color: 0x18191c,
            metalness: 0.35,
            roughness: 0.7,
        });

        this.chromeMaterial = new THREE.MeshStandardMaterial({
            color: 0xe2e8f0,
            metalness: 0.95,
            roughness: 0.2,
        });

        // 1. Base hub & 5 legs
        const hubGeo = new THREE.CylinderGeometry(0.12, 0.15, 0.12, 24);
        const hubMesh = new THREE.Mesh(hubGeo, this.frameMaterial);
        hubMesh.position.y = 0.1;
        hubMesh.castShadow = true;
        this.chairGroup.add(hubMesh);

        for (let i = 0; i < 5; i++) {
            const angle = (i * 2 * Math.PI) / 5;
            const legLength = 0.65;
            const legGeo = new THREE.BoxGeometry(0.06, 0.04, legLength);
            const legMesh = new THREE.Mesh(legGeo, this.frameMaterial);
            legMesh.position.set((Math.cos(angle) * legLength) / 2, 0.08, (Math.sin(angle) * legLength) / 2);
            legMesh.rotation.y = -angle + Math.PI / 2;
            legMesh.castShadow = true;
            this.chairGroup.add(legMesh);

            // Wheel
            const wheelGeo = new THREE.CylinderGeometry(0.035, 0.035, 0.03, 16);
            const wheelMat = new THREE.MeshStandardMaterial({ color: 0x0f1115, roughness: 0.6 });
            const wheelMesh = new THREE.Mesh(wheelGeo, wheelMat);
            wheelMesh.position.set(Math.cos(angle) * legLength, 0.04, Math.sin(angle) * legLength);
            wheelMesh.rotation.z = Math.PI / 2;
            this.chairGroup.add(wheelMesh);
        }

        // Piston Lift
        const pistonGeo = new THREE.CylinderGeometry(0.038, 0.038, 0.38, 24);
        const pistonMesh = new THREE.Mesh(pistonGeo, this.chromeMaterial);
        pistonMesh.position.y = 0.35;
        pistonMesh.castShadow = true;
        this.chairGroup.add(pistonMesh);

        // Seat Cushion
        const seatGeo = new THREE.BoxGeometry(0.54, 0.08, 0.52);
        this.seatMesh = new THREE.Mesh(seatGeo, this.fabricMaterial);
        this.seatMesh.position.set(0, 0.72, 0.02);
        this.seatMesh.castShadow = true;
        this.seatMesh.receiveShadow = true;
        this.chairGroup.add(this.seatMesh);

        // Waterfall Edge
        const frontEdgeGeo = new THREE.CylinderGeometry(0.035, 0.035, 0.54, 24);
        const frontEdgeMesh = new THREE.Mesh(frontEdgeGeo, this.fabricMaterial);
        frontEdgeMesh.position.set(0, 0.7, 0.28);
        frontEdgeMesh.rotation.z = Math.PI / 2;
        this.chairGroup.add(frontEdgeMesh);

        // Y-Spine Frame
        const spineGeo = new THREE.BoxGeometry(0.08, 0.5, 0.05);
        const spineMesh = new THREE.Mesh(spineGeo, this.frameMaterial);
        spineMesh.position.set(0, 0.95, -0.25);
        spineMesh.rotation.x = -0.15;
        spineMesh.castShadow = true;
        this.chairGroup.add(spineMesh);

        // Backrest Frame & Mesh
        const backGeo = new THREE.BoxGeometry(0.48, 0.65, 0.03);
        this.backMesh = new THREE.Mesh(backGeo, this.fabricMaterial);
        this.backMesh.position.set(0, 1.25, -0.2);
        this.backMesh.castShadow = true;
        this.chairGroup.add(this.backMesh);

        // Lumbar Cushion
        const lumbarGeo = new THREE.BoxGeometry(0.32, 0.14, 0.04);
        this.lumbarMesh = new THREE.Mesh(lumbarGeo, this.fabricMaterial);
        this.lumbarMesh.position.set(0, 0.98, -0.18);
        this.chairGroup.add(this.lumbarMesh);

        // Armrests
        [-0.31, 0.31].forEach((xPos) => {
            const armPillar = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.02, 0.25, 16), this.frameMaterial);
            armPillar.position.set(xPos, 0.78, 0);
            this.chairGroup.add(armPillar);

            const armPad = new THREE.Mesh(new THREE.BoxGeometry(0.09, 0.035, 0.26), this.frameMaterial);
            armPad.position.set(xPos, 0.92, 0.02);
            armPad.castShadow = true;
            this.chairGroup.add(armPad);
        });

        this.scene.add(this.chairGroup);
    },

    /**
     * Mouse Move Parallax
     */
    _handleMouseMove: function (e) {
        if (!this.chairGroup) return;
        const mouseX = (e.clientX / window.innerWidth) * 2 - 1;
        const mouseY = -(e.clientY / window.innerHeight) * 2 + 1;
        this.targetRotationY = mouseX * 0.25;
        this.targetRotationX = mouseY * 0.1;
    },

    /**
     * Window Resize Handler
     */
    _handleResize: function () {
        if (!this.container || !this.renderer || !this.camera) return;
        const width = this.container.clientWidth;
        const height = this.container.clientHeight;
        this.camera.aspect = width / height;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(width, height);
    },

    /**
     * Event: Quick Color Click
     */
    _onQuickColorClick: function (ev) {
        ev.preventDefault();
        const btn = ev.currentTarget;
        const hex = btn.dataset.hex || '#17181c';
        const label = btn.dataset.name || 'Obsidian Black';

        this.targetColor = new window.THREE.Color(hex);

        // Update active class
        this.el.querySelectorAll('.js_quick_color').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        // Update label
        const nameEl = this.el.querySelector('.js_active_color_name');
        if (nameEl) nameEl.textContent = label;
    },

    /**
     * Event: Toggle Turntable
     */
    _onTurntableToggle: function (ev) {
        ev.preventDefault();
        this.autoRotate = !this.autoRotate;
        const btn = ev.currentTarget;
        if (this.autoRotate) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    },

    /**
     * Continuous Animation Loop
     */
    _animate: function () {
        this.animationFrameId = requestAnimationFrame(this._animate.bind(this));

        // Smooth color transition
        if (this.fabricMaterial && this.targetColor) {
            this.fabricMaterial.color.lerp(this.targetColor, 0.1);
        }

        // Turntable rotation
        if (this.autoRotate && this.chairGroup) {
            this.chairGroup.rotation.y += 0.007;
        }

        if (this.controls) {
            this.controls.update();
        }

        if (this.renderer && this.scene && this.camera) {
            this.renderer.render(this.scene, this.camera);
        }
    },

    /**
     * @override
     */
    destroy: function () {
        if (this.animationFrameId) {
            cancelAnimationFrame(this.animationFrameId);
        }
        window.removeEventListener('mousemove', this._onMouseMove);
        window.removeEventListener('resize', this._onResize);

        if (this.renderer) {
            this.renderer.dispose();
            if (this.renderer.domElement && this.renderer.domElement.parentNode) {
                this.renderer.domElement.parentNode.removeChild(this.renderer.domElement);
            }
        }
        this._super.apply(this, arguments);
    },
});

publicWidget.registry.AuraForm3DHero = AuraForm3DHero;

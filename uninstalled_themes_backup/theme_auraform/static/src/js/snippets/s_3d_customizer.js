/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

export const AuraForm3DCustomizer = publicWidget.Widget.extend({
    selector: '.s_3d_customizer',
    events: {
        'click .js_viewpoint_btn': '_onViewpointClick',
        'click .js_fabric_swatch': '_onFabricSwatchClick',
        'click .js_finish_card': '_onFinishCardClick',
        'click .js_addon_toggle': '_onAddonToggle',
        'click .js_turntable_toggle': '_onTurntableToggle',
        'click .js_reset_defaults': '_onResetDefaults',
        'click .js_panel_tab': '_onPanelTabClick',
        'click .js_add_to_cart_3d': '_onAddToCart',
    },

    /**
     * @override
     */
    start: function () {
        this._super.apply(this, arguments);
        if (!this.el) return;
        this.viewport = this.el.querySelector('.customizer-viewport');
        if (!this.viewport) return;

        // Customizer State
        this.basePrice = parseFloat(this.el.dataset.basePrice || '599');
        this.finishPrice = 0;
        this.lumbarPrice = 45;
        this.armrestPrice = 60;

        this.hasLumbar = true;
        this.armrestType = '4d';
        this.legFinish = 'matte-black';
        this.autoRotate = false;
        this.currentViewpoint = 'default';

        this.currentFabric = {
            name: 'Obsidian Black',
            hex: '#17181c',
            roughness: 0.85,
        };

        // Camera viewpoint positions
        this.viewpoints = {
            default: { pos: [2.3, 1.4, 2.3], target: [0, 0.45, 0] },
            front: { pos: [0.01, 0.8, 2.7], target: [0, 0.5, 0] },
            side: { pos: [2.8, 0.8, 0.01], target: [0, 0.5, 0] },
            detail: { pos: [1.1, 0.95, 1.0], target: [0, 0.65, 0] },
        };

        if (window.THREE) {
            this._initCustomizerEngine();
        } else {
            setTimeout(() => {
                if (window.THREE) this._initCustomizerEngine();
            }, 300);
        }

        this._updatePriceDisplay();
    },

    /**
     * Initialize 3D Engine & Scene
     */
    _initCustomizerEngine: function () {
        const THREE = window.THREE;
        const width = this.viewport.clientWidth || 800;
        const height = this.viewport.clientHeight || 600;

        // 1. Scene
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x0b0d12);

        // 2. Camera
        this.camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 100);
        this.camera.position.set(...this.viewpoints.default.pos);

        // 3. Renderer
        this.renderer = new THREE.WebGLRenderer({
            antialias: true,
            powerPreference: 'high-performance',
            toneMappingExposure: 1.15,
        });
        this.renderer.setSize(width, height);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        this.viewport.appendChild(this.renderer.domElement);

        // Remove loading spinner
        const loader = this.viewport.querySelector('.af-3d-loader');
        if (loader) loader.remove();

        // 4. OrbitControls
        if (THREE.OrbitControls) {
            this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
            this.controls.enableDamping = true;
            this.controls.dampingFactor = 0.06;
            this.controls.maxPolarAngle = Math.PI / 2.05; // Prevent dipping beneath floor
            this.controls.minDistance = 1.3;
            this.controls.maxDistance = 4.8;
            this.controls.target.set(...this.viewpoints.default.target);
        }

        // 5. Studio Lighting
        const ambient = new THREE.AmbientLight(0xffffff, 0.6);
        this.scene.add(ambient);

        this.keyLight = new THREE.DirectionalLight(0xffffff, 1.8);
        this.keyLight.position.set(5, 8, 4);
        this.keyLight.castShadow = true;
        this.keyLight.shadow.mapSize.width = 1024;
        this.keyLight.shadow.mapSize.height = 1024;
        this.scene.add(this.keyLight);

        const fillLight = new THREE.DirectionalLight(0xdbeafe, 0.7);
        fillLight.position.set(-6, 4, -3);
        this.scene.add(fillLight);

        const rimLight = new THREE.DirectionalLight(0xf8fafc, 1.1);
        rimLight.position.set(0, 5, -5);
        this.scene.add(rimLight);

        // 6. Ground Shadow Plane
        const groundGeo = new THREE.PlaneGeometry(8, 8);
        const groundMat = new THREE.ShadowMaterial({ opacity: 0.45 });
        const ground = new THREE.Mesh(groundGeo, groundMat);
        ground.rotation.x = -Math.PI / 2;
        ground.position.y = -0.4;
        ground.receiveShadow = true;
        this.scene.add(ground);

        // 7. Load GLTF or Procedural Chair Model
        const modelUrl = this.el.dataset.modelUrl;
        if (modelUrl && THREE.GLTFLoader) {
            this._loadGLTFModel(modelUrl);
        } else {
            this._buildProceduralErgonomicChair();
        }

        // 8. Resize listener
        this._onResize = this._handleResize.bind(this);
        window.addEventListener('resize', this._onResize);

        // 9. Camera Target Tracking
        this.targetCamPos = new THREE.Vector3(...this.viewpoints.default.pos);
        this.targetLookAt = new THREE.Vector3(...this.viewpoints.default.target);
        this.isTransitioningCamera = false;

        // 10. Start Animation Loop
        this.targetFabricColor = new THREE.Color(this.currentFabric.hex);
        this.targetLegColor = new THREE.Color(0x18191c);
        this._animate();
    },

    /**
     * GLTF Model Loader with Part Targeting
     */
    _loadGLTFModel: function (url) {
        const THREE = window.THREE;
        const loader = new THREE.GLTFLoader();
        loader.load(
            url,
            (gltf) => {
                this.chairModel = gltf.scene;
                this.chairModel.position.set(0, -0.4, 0);

                // Map target mesh names
                this.chairModel.traverse((child) => {
                    if (child.isMesh) {
                        child.castShadow = true;
                        child.receiveShadow = true;
                        if (child.name.includes('Seat') || child.name.includes('Backrest')) {
                            child.material = child.material.clone();
                            this.fabricMaterial = child.material;
                        } else if (child.name.includes('Legs') || child.name.includes('Base')) {
                            child.material = child.material.clone();
                            this.legMaterial = child.material;
                        }
                    }
                });
                this.scene.add(this.chairModel);
            },
            undefined,
            (err) => {
                console.warn('[AuraForm 3D] GLTF load failed, using procedural chair.', err);
                this._buildProceduralErgonomicChair();
            }
        );
    },

    /**
     * Procedural High-Fidelity Customizer Model
     */
    _buildProceduralErgonomicChair: function () {
        const THREE = window.THREE;
        this.chairModel = new THREE.Group();
        this.chairModel.position.set(0, -0.4, 0);

        // PBR Material References
        this.fabricMaterial = new THREE.MeshStandardMaterial({
            color: this.currentFabric.hex,
            roughness: this.currentFabric.roughness,
            metalness: 0.1,
        });

        this.legMaterial = new THREE.MeshStandardMaterial({
            color: 0x18191c,
            metalness: 0.25,
            roughness: 0.85,
        });

        this.frameMaterial = new THREE.MeshStandardMaterial({
            color: 0x222630,
            metalness: 0.75,
            roughness: 0.35,
        });

        // 1. Five-Star Wheeled Base
        const hub = new THREE.Mesh(new THREE.CylinderGeometry(0.13, 0.16, 0.14, 32), this.legMaterial);
        hub.position.y = 0.12;
        hub.castShadow = true;
        this.chairModel.add(hub);

        for (let i = 0; i < 5; i++) {
            const angle = (i * 2 * Math.PI) / 5;
            const legLen = 0.65;
            const prong = new THREE.Mesh(new THREE.BoxGeometry(0.07, 0.04, legLen), this.legMaterial);
            prong.position.set((Math.cos(angle) * legLen) / 2, 0.08, (Math.sin(angle) * legLen) / 2);
            prong.rotation.y = -angle + Math.PI / 2;
            prong.castShadow = true;
            this.chairModel.add(prong);

            // Caster Wheels
            const casterGroup = new THREE.Group();
            casterGroup.position.set(Math.cos(angle) * legLen, 0.045, Math.sin(angle) * legLen);
            const w1 = new THREE.Mesh(new THREE.CylinderGeometry(0.038, 0.038, 0.018, 20), this.frameMaterial);
            w1.rotation.z = Math.PI / 2;
            w1.position.x = -0.02;
            const w2 = w1.clone();
            w2.position.x = 0.02;
            casterGroup.add(w1);
            casterGroup.add(w2);
            this.chairModel.add(casterGroup);
        }

        // Piston Lift
        const piston = new THREE.Mesh(new THREE.CylinderGeometry(0.032, 0.032, 0.32, 32), new THREE.MeshStandardMaterial({ color: 0xe5e7eb, metalness: 0.95, roughness: 0.1 }));
        piston.position.y = 0.45;
        piston.castShadow = true;
        this.chairModel.add(piston);

        // 2. Ergonomic Seat with Waterfall
        const seat = new THREE.Mesh(new THREE.BoxGeometry(0.54, 0.085, 0.52), this.fabricMaterial);
        seat.position.set(0, 0.72, 0.02);
        seat.castShadow = true;
        seat.receiveShadow = true;
        this.chairModel.add(seat);

        const waterfall = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 0.54, 32), this.fabricMaterial);
        waterfall.position.set(0, 0.7, 0.28);
        waterfall.rotation.z = Math.PI / 2;
        waterfall.castShadow = true;
        this.chairModel.add(waterfall);

        // 3. Aerospace Y-Spine Frame
        const spine = new THREE.Mesh(new THREE.BoxGeometry(0.085, 0.45, 0.055), this.frameMaterial);
        spine.position.set(0, 0.88, -0.26);
        spine.rotation.x = -0.15;
        spine.castShadow = true;
        this.chairModel.add(spine);

        // 4. Mesh Backrest
        const backrest = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.68, 0.03), this.fabricMaterial);
        backrest.position.set(0, 1.22, -0.2);
        backrest.castShadow = true;
        backrest.receiveShadow = true;
        this.chairModel.add(backrest);

        // 5. Lumbar Support Assembly
        this.lumbarGroup = new THREE.Group();
        this.lumbarGroup.position.set(0, 0.94, -0.18);
        const lumbarPad = new THREE.Mesh(new THREE.BoxGeometry(0.34, 0.14, 0.04), this.fabricMaterial);
        lumbarPad.castShadow = true;
        this.lumbarGroup.add(lumbarPad);
        this.chairModel.add(this.lumbarGroup);

        // 6. Armrests (Left & Right)
        this.armrestGroup = new THREE.Group();
        [-0.31, 0.31].forEach((x) => {
            const pillar = new THREE.Mesh(new THREE.CylinderGeometry(0.022, 0.024, 0.26, 24), this.frameMaterial);
            pillar.position.set(x, 0.8, 0);
            pillar.castShadow = true;
            this.armrestGroup.add(pillar);

            const pad = new THREE.Mesh(new THREE.BoxGeometry(0.095, 0.038, 0.28), this.frameMaterial);
            pad.position.set(x, 0.96, 0.02);
            pad.castShadow = true;
            this.armrestGroup.add(pad);
        });
        this.chairModel.add(this.armrestGroup);

        this.scene.add(this.chairModel);
    },

    /**
     * Window Resize Handler
     */
    _handleResize: function () {
        if (!this.viewport || !this.renderer || !this.camera) return;
        const width = this.viewport.clientWidth;
        const height = this.viewport.clientHeight;
        this.camera.aspect = width / height;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(width, height);
    },

    /**
     * Event: Switch Camera Viewpoint
     */
    _onViewpointClick: function (ev) {
        ev.preventDefault();
        const btn = ev.currentTarget;
        const viewId = btn.dataset.view || 'default';
        const config = this.viewpoints[viewId] || this.viewpoints.default;

        this.targetCamPos.set(...config.pos);
        this.targetLookAt.set(...config.target);
        this.isTransitioningCamera = true;

        this.el.querySelectorAll('.js_viewpoint_btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
    },

    /**
     * Event: Change Fabric Swatch
     */
    _onFabricSwatchClick: function (ev) {
        ev.preventDefault();
        const btn = ev.currentTarget;
        const hex = btn.dataset.hex || '#17181c';
        const name = btn.dataset.name || 'Obsidian Black';
        const roughness = parseFloat(btn.dataset.roughness || '0.85');

        this.currentFabric = { name, hex, roughness };
        this.targetFabricColor = new window.THREE.Color(hex);

        this.el.querySelectorAll('.js_fabric_swatch').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        const titleEl = this.el.querySelector('.js_active_fabric_title');
        if (titleEl) titleEl.textContent = name;
    },

    /**
     * Event: Change Leg Finish
     */
    _onFinishCardClick: function (ev) {
        ev.preventDefault();
        const btn = ev.currentTarget;
        const finishId = btn.dataset.finish || 'matte-black';
        const priceMod = parseFloat(btn.dataset.priceMod || '0');

        this.legFinish = finishId;
        this.finishPrice = priceMod;

        const finishesConfig = {
            'matte-black': { color: 0x18191c, metalness: 0.25, roughness: 0.85 },
            'brushed-chrome': { color: 0xe2e8f0, metalness: 0.95, roughness: 0.22 },
            'natural-oak': { color: 0xc29b6f, metalness: 0.05, roughness: 0.70 },
        };

        const config = finishesConfig[finishId] || finishesConfig['matte-black'];
        this.targetLegColor = new window.THREE.Color(config.color);
        if (this.legMaterial) {
            this.legMaterial.metalness = config.metalness;
            this.legMaterial.roughness = config.roughness;
        }

        this.el.querySelectorAll('.js_finish_card').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        this._updatePriceDisplay();
    },

    /**
     * Event: Toggle Add-On Upgrades
     */
    _onAddonToggle: function (ev) {
        ev.preventDefault();
        const card = ev.currentTarget;
        const addonType = card.dataset.addon;

        if (addonType === 'lumbar') {
            this.hasLumbar = !this.hasLumbar;
            if (this.lumbarGroup) {
                this.lumbarGroup.visible = this.hasLumbar;
            }
            if (this.hasLumbar) {
                card.classList.add('active');
            } else {
                card.classList.remove('active');
            }
        } else if (addonType === 'armrest') {
            this.armrestType = this.armrestType === '4d' ? 'fixed' : '4d';
            if (this.armrestType === '4d') {
                card.classList.add('active');
            } else {
                card.classList.remove('active');
            }
        }

        this._updatePriceDisplay();
    },

    /**
     * Event: Toggle Auto-Rotate Turntable
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
     * Event: Reset Defaults
     */
    _onResetDefaults: function (ev) {
        ev.preventDefault();
        this.targetCamPos.set(...this.viewpoints.default.pos);
        this.targetLookAt.set(...this.viewpoints.default.target);
        this.isTransitioningCamera = true;
        this.autoRotate = false;

        // Reset to obsidian black and matte black
        const defaultFabric = this.el.querySelector('.js_fabric_swatch[data-hex="#17181c"]');
        if (defaultFabric) defaultFabric.click();

        const defaultFinish = this.el.querySelector('.js_finish_card[data-finish="matte-black"]');
        if (defaultFinish) defaultFinish.click();
    },

    /**
     * Event: Panel Tab Navigation
     */
    _onPanelTabClick: function (ev) {
        ev.preventDefault();
        const tabBtn = ev.currentTarget;
        const targetTab = tabBtn.dataset.tab;

        this.el.querySelectorAll('.js_panel_tab').forEach(b => b.classList.remove('active'));
        tabBtn.classList.add('active');

        this.el.querySelectorAll('.js_tab_content').forEach((content) => {
            if (content.dataset.tabContent === targetTab) {
                content.classList.remove('d-none');
            } else {
                content.classList.add('d-none');
            }
        });
    },

    /**
     * Compute and Update Dynamic Price Counter
     */
    _updatePriceDisplay: function () {
        let total = this.basePrice + this.finishPrice;
        if (this.hasLumbar) total += this.lumbarPrice;
        if (this.armrestType === '4d') total += this.armrestPrice;

        this.currentTotal = total;

        const priceEl = this.el.querySelector('.js_price_counter');
        if (priceEl) {
            priceEl.textContent = `$${Math.round(total)}`;
        }
    },

    /**
     * Odoo eCommerce: Add Customized Configuration to Cart
     */
    _onAddToCart: function (ev) {
        ev.preventDefault();
        const btn = ev.currentTarget;
        const productId = this.el.dataset.productId || '1';

        btn.disabled = true;
        const originalText = btn.innerHTML;
        btn.innerHTML = '<span>Adding to Cart...</span>';

        const customConfigSummary = `${this.currentFabric.name} | ${this.legFinish.toUpperCase()} | ${this.hasLumbar ? '+Lumbar' : ''} | ${this.armrestType.toUpperCase()} Armrests`;

        // Direct Odoo /shop/cart/update RPC or Form Submission
        fetch('/shop/cart/update', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                jsonrpc: '2.0',
                method: 'call',
                params: {
                    product_id: parseInt(productId),
                    add_qty: 1,
                    custom_config: customConfigSummary,
                },
            }),
        })
        .then(() => {
            btn.innerHTML = '<span>Added to Cart ✓</span>';
            setTimeout(() => {
                window.location.href = '/shop/cart';
            }, 600);
        })
        .catch(() => {
            // Fallback standard GET redirect to shop cart
            window.location.href = `/shop/cart?product_id=${productId}&add_qty=1`;
        });
    },

    /**
     * Continuous 60fps Animation Loop
     */
    _animate: function () {
        this.animId = requestAnimationFrame(this._animate.bind(this));

        // Smooth camera transitions
        if (this.isTransitioningCamera && this.camera && this.controls) {
            this.camera.position.lerp(this.targetCamPos, 0.08);
            this.controls.target.lerp(this.targetLookAt, 0.08);
            if (this.camera.position.distanceTo(this.targetCamPos) < 0.01) {
                this.isTransitioningCamera = false;
            }
        }

        // PBR Material smooth transitions
        if (this.fabricMaterial && this.targetFabricColor) {
            this.fabricMaterial.color.lerp(this.targetFabricColor, 0.1);
        }
        if (this.legMaterial && this.targetLegColor) {
            this.legMaterial.color.lerp(this.targetLegColor, 0.1);
        }

        // Turntable
        if (this.autoRotate && this.chairModel) {
            this.chairModel.rotation.y += 0.007;
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
        if (this.animId) cancelAnimationFrame(this.animId);
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

publicWidget.registry.AuraForm3DCustomizer = AuraForm3DCustomizer;

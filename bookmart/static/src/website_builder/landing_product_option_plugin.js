import { Plugin } from "@html_editor/plugin";
import { registry } from "@web/core/registry";
import { LandingProductOption } from "./landing_product_option";
import { BuilderAction } from "@html_builder/core/builder_action";

export class SelectLandingProductAction extends BuilderAction {
    static id = "selectLandingProduct";
    static dependencies = ["builderActions"];

    async load({ editingElement, value }) {
        if (!value) return null;
        try {
            const parsed = JSON.parse(value);
            const id = parsed.id;
            if (!id) return null;
            const records = await this.services.orm.read(
                "product.template",
                [id],
                ["name", "list_price", "product_variant_ids", "description_sale"]
            );
            return records && records[0] ? records[0] : null;
        } catch (e) {
            console.error("Error loading product data:", e);
            return null;
        }
    }

    apply({ editingElement, value, loadResult }) {
        if (!value) return;
        let id = null;
        let parsed = null;
        try {
            parsed = JSON.parse(value);
            id = parsed.id;
        } catch (e) {
            return;
        }
        if (!id) return;

        const prod = loadResult || parsed;
        const variantId = (prod.product_variant_ids && prod.product_variant_ids.length > 0)
            ? prod.product_variant_ids[0]
            : id;

        editingElement.dataset.productTemplateId = id;
        editingElement.dataset.productId = variantId;

        // 1. Update Title
        const titleEl = editingElement.querySelector(".snippet-display-title, .landing-product-info h2, h2");
        if (titleEl && prod.name) {
            titleEl.textContent = prod.name;
        }

        // 2. Update Price
        const priceEl = editingElement.querySelector(".snippet-display-price");
        if (priceEl && prod.list_price !== undefined) {
            priceEl.textContent = Number(prod.list_price).toFixed(2);
        }

        // 3. Update Image
        const imgEl = editingElement.querySelector(".snippet-display-img, img.landing-main-img");
        if (imgEl) {
            imgEl.src = `/web/image/product.template/${id}/image_1920`;
            imgEl.alt = prod.name || "Product Image";
        }
        const thumbImgs = editingElement.querySelectorAll(".landing-thumbnails-row img");
        thumbImgs.forEach(t => {
            t.src = `/web/image/product.template/${id}/image_1920`;
            t.alt = prod.name || "Product Image";
        });

        // 4. Update Description if available
        if (prod.description_sale) {
            const descEl = editingElement.querySelector(".snippet-display-desc");
            if (descEl) {
                descEl.textContent = prod.description_sale;
            }
        }

        // 5. Update Checkout Modal / Button binding
        const buyBtn = editingElement.querySelector(".landing-buy-now-trigger");
        let modal = null;
        if (buyBtn && buyBtn.dataset.bsTarget) {
            modal = this.document.querySelector(buyBtn.dataset.bsTarget);
        }
        if (!modal) {
            modal = editingElement.querySelector(".landing-checkout-modal");
        }
        if (modal) {
            const prodInput = modal.querySelector('input[name="product_id"]');
            if (prodInput) {
                prodInput.value = variantId;
            }
            const modalTitle = modal.querySelector(".modal-title");
            if (modalTitle && prod.name) {
                modalTitle.textContent = `Instant Checkout: ${prod.name}`;
            }
            const summaryTitle = modal.querySelector(".fw-bold.text-dark.text-truncate");
            if (summaryTitle && prod.name) {
                summaryTitle.textContent = prod.name;
            }
            const summaryImg = modal.querySelector(".modal-body img");
            if (summaryImg) {
                summaryImg.src = `/web/image/product.template/${id}/image_1920`;
            }
            const summaryPrice = modal.querySelector('[id^="summary-unit-price-"]');
            if (summaryPrice && prod.list_price !== undefined) {
                summaryPrice.textContent = Number(prod.list_price).toFixed(2);
                summaryPrice.dataset.price = Number(prod.list_price).toFixed(2);
            }
            const subtotalEl = modal.querySelector('[id^="calc-subtotal-"]');
            if (subtotalEl && prod.list_price !== undefined) {
                subtotalEl.textContent = Number(prod.list_price).toFixed(2);
            }
            const grandTotalEl = modal.querySelector('[id^="calc-grand-total-"], [id^="calc-total-"]');
            if (grandTotalEl && prod.list_price !== undefined) {
                grandTotalEl.textContent = Number(prod.list_price).toFixed(2);
            }
        }

        // 5.1 Update Cart Button attributes
        const cartBtn = editingElement.querySelector(".landing-add-to-cart-btn");
        if (cartBtn) {
            cartBtn.setAttribute("data-product-template-id", id);
            cartBtn.setAttribute("data-product-id", variantId);
        }

        // 6. Sync Product Name, Price & Image to Hero Strip & Footer (Header nav remains unified 'Products')
        const secId = editingElement.id;
        if (secId && prod.name) {

            // Update Hero Quick Jump Strip
            const stripCard = this.document.querySelector(`.landing-product-strip-wrapper a[href="#${secId}"]`);
            if (stripCard) {
                const stripTitle = stripCard.querySelector(".fw-bold.text-dark.text-truncate");
                if (stripTitle) {
                    stripTitle.textContent = prod.name;
                }
                const stripPrice = stripCard.querySelector(".fw-bold.text-primary");
                if (stripPrice && prod.list_price !== undefined) {
                    stripPrice.textContent = "৳" + Number(prod.list_price).toFixed(2);
                }
                const stripImg = stripCard.querySelector("img");
                if (stripImg) {
                    stripImg.src = `/web/image/product.template/${id}/image_1920`;
                    stripImg.alt = prod.name;
                }
            }

            // Update Footer Book Links
            const footerLinks = this.document.querySelectorAll(`footer a[href="#${secId}"]`);
            footerLinks.forEach((link) => {
                link.textContent = prod.name;
            });
        }
    }

    clean({ editingElement }) {
        delete editingElement.dataset.productTemplateId;
        delete editingElement.dataset.productId;
    }

    getValue({ editingElement }) {
        const id = editingElement.dataset.productTemplateId || editingElement.dataset.productId;
        if (id) {
            return JSON.stringify({ id: parseInt(id) });
        }
    }
}

class LandingProductOptionPlugin extends Plugin {
    static id = "bookmartProductOption";
    static dependencies = ["builderActions"];
    resources = {
        builder_options: [LandingProductOption],
        builder_actions: {
            SelectLandingProductAction,
        },
    };
}

const websitePlugins = registry.category("website-plugins");
if (!websitePlugins.contains(LandingProductOptionPlugin.id)) {
    websitePlugins.add(LandingProductOptionPlugin.id, LandingProductOptionPlugin);
} else {
    websitePlugins.add(LandingProductOptionPlugin.id, LandingProductOptionPlugin, { force: true });
}


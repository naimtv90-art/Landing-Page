import { BaseOptionComponent, useGetItemValue } from "@html_builder/core/utils";

export class LandingProductOption extends BaseOptionComponent {
    static template = "theme_multiproduct_landing.LandingProductOption";
    static selector = ".landing-product-section, [data-snippet='s_single_product_showcase']";
    static props = [];

    setup() {
        super.setup();
        this.getItemValue = useGetItemValue();
    }

    getItemValueJSON(id) {
        const value = this.getItemValue(id);
        return value && JSON.parse(value);
    }
}


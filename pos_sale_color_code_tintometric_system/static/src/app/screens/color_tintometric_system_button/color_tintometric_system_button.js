/** @odoo-module **/
// © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
// License LGPL-3.0 (https://www.gnu.org/licenses/lgpl-3.0.html)

import { _t } from "@web/core/l10n/translation";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { useService } from "@web/core/utils/hooks";
import { TextAreaPopup } from "@pos_sale_color_code_tintometric_system/app/utils/input_popups/textarea_popup";
import { Component } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";

export class ColorTintometricSystemButton extends Component {
    static template = "pos_sale_color_code_tintometric_system.ColorTintometricSystemButton";

    setup(_defaultObj, options) {
        super.setup(...arguments);
        this.pos = usePos();
        this.popup = useService("popup");
    };
    async addLot() {
        const selectedOrderline = this.pos.get_order().get_selected_orderline();
        if (!selectedOrderline) {
            return;
        }
        const { confirmed, payload: inputNote } = await this.popup.add(TextAreaPopup, {
            startingValue: selectedOrderline.get_tintometric_code(),
            title: _t("Add Lot/S.Tin"),
        });

        if (confirmed) {
            selectedOrderline.set_tintometric_code(inputNote);
        }
    }
}

ProductScreen.addControlButton({
    component: ColorTintometricSystemButton,
});

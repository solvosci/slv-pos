// Copyright 2026 Solvos
// License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { patch } from "@web/core/utils/patch";

patch(ControlButtons.prototype, {
    get secondaryUomLine() {
        const line = this.currentOrder?.getSelectedOrderline();
        return line && (line.secondary_uom_id || line.productSecondaryUnit) ? line : false;
    },
    async onClickSecondaryUomQty() {
        await this.pos.editSelectedLineSecondaryUomQty();
    },
});

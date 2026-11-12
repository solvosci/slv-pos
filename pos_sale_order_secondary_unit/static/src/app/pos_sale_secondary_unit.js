// Copyright 2026 Solvos
// License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { patch } from "@web/core/utils/patch";

patch(PosOrderline.prototype, {
    /** Take unit and pieces from the sale order line (pending part only). */
    async setQuantityFromSOL(convertedLine) {
        const res = await super.setQuantityFromSOL(...arguments);
        // ``convertedLine`` is a plain dict (read_converted): use the record.
        const sol = this.sale_order_line_id;
        const unit = sol?.secondary_uom_id;
        if (unit && sol.secondary_uom_qty) {
            let pieces = sol.secondary_uom_qty;
            const solQty = sol.product_uom_qty;
            if (solQty && Math.abs(this.qty) !== Math.abs(solQty)) {
                // Partially delivered/invoiced: proportional pending pieces.
                pieces = unit.uom_id.round((pieces * this.qty) / solQty);
            }
            this.update({ secondary_uom_id: unit, secondary_uom_qty: pieces });
        }
        return res;
    },
});

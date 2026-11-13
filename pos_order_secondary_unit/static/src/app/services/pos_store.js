// Copyright 2026 Solvos
// License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import { PosStore } from "@point_of_sale/app/services/pos_store";
import { makeAwaitable } from "@point_of_sale/app/utils/make_awaitable_dialog";
import { patch } from "@web/core/utils/patch";
import { SecondaryUnitPopup } from "../components/secondary_unit_popup/secondary_unit_popup";

patch(PosStore.prototype, {
    async addLineToOrder(vals, order, opts = {}, configure = true) {
        const line = await super.addLineToOrder(...arguments);
        if (
            !line ||
            line.secondary_uom_id ||
            line.refunded_orderline_id ||
            line.combo_parent_id
        ) {
            return line;
        }
        const unit = line.productSecondaryUnit;
        if (!unit) {
            return line;
        }
        if (configure) {
            // Interactive add (tap on product): ask unit + how many.
            const choice = await this.askSecondaryUnit(line, unit, 1);
            line.setSecondaryUomQty(choice?.pieces || 1, choice?.unit || unit, {
                forceEstimate: true,
            });
        } else {
            // Barcode, sale order import, etc.: estimate pieces from the qty.
            line.update({
                secondary_uom_id: unit,
                secondary_uom_qty: line.getSecondaryQtyFromQty(unit),
            });
        }
        return line;
    },

    /**
     * Ask which secondary unit and how many of it.
     * @returns {Promise<{unit: Object, pieces: number}|undefined>} undefined when cancelled
     */
    async askSecondaryUnit(line, unit = line.secondary_uom_id, startingValue = 1) {
        const units = line.productSecondaryUnits;
        if (!units.length) {
            return undefined;
        }
        const payload = await makeAwaitable(this.dialog, SecondaryUnitPopup, {
            productName: line.getFullProductName(),
            uomName: line.product_id.uom_id?.name || "",
            units,
            unit: units.find((u) => u.id === unit?.id) || units[0],
            startingValue: `${startingValue}`,
        });
        if (!payload) {
            return undefined;
        }
        const pieces = payload.unit.uom_id?.round(payload.pieces) || payload.pieces;
        return { unit: payload.unit, pieces };
    },

    async editSelectedLineSecondaryUomQty() {
        const line = this.getOrder()?.getSelectedOrderline();
        const unit = line?.secondary_uom_id || line?.productSecondaryUnit;
        if (!line || !unit) {
            return;
        }
        line.order_id.assertEditable();
        const choice = await this.askSecondaryUnit(
            line,
            unit,
            Math.abs(line.secondary_uom_qty) || 1
        );
        if (choice) {
            line.setSecondaryUomQty(choice.pieces, choice.unit);
        }
    },
});

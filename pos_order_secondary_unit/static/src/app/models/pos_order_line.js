// Copyright 2026 Solvos
// License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { formatFloat } from "@web/core/utils/numbers";
import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";

patch(PosOrderline.prototype, {
    setup() {
        super.setup(...arguments);
        // Refund lines created from the ticket screen: inherit the unit and an
        // estimate of the pieces from the refunded line.
        const refunded = this.refunded_orderline_id;
        if (refunded?.secondary_uom_id && !this.secondary_uom_id) {
            let pieces = refunded.secondary_uom_qty;
            if (refunded.qty && Math.abs(this.qty) !== Math.abs(refunded.qty)) {
                pieces = refunded.secondary_uom_id.uom_id.round(
                    (refunded.secondary_uom_qty * Math.abs(this.qty)) / Math.abs(refunded.qty)
                );
            }
            this.update({
                secondary_uom_id: refunded.secondary_uom_id,
                secondary_uom_qty: -Math.abs(pieces),
            });
        }
    },

    /**
     * All active secondary units of the product (OCA product_secondary_unit):
     * template units plus the ones restricted to this variant.
     */
    get productSecondaryUnits() {
        const product = this.product_id;
        if (!product) {
            return [];
        }
        return this.models["product.secondary.unit"]
            .getAll()
            .filter(
                (unit) =>
                    unit.product_tmpl_id?.id === product.product_tmpl_id?.id &&
                    (!unit.product_id || unit.product_id.id === product.id)
            )
            .sort((a, b) => a.factor - b.factor || a.id - b.id);
    },

    /** Default unit: "Default secondary unit for sales" or the first one. */
    get productSecondaryUnit() {
        const units = this.productSecondaryUnits;
        const saleDefault = this.product_id?.sale_secondary_uom_id;
        return units.find((u) => u.id === saleDefault?.id) || units[0] || false;
    },

    /** The weight comes from the scale and must never be overwritten. */
    get isWeighedWithScale() {
        return Boolean(
            this.product_id?.product_tmpl_id?.to_weight && this.config?.iface_electronic_scale
        );
    },

    /** Estimated primary qty (kg) for a number of pieces. */
    getSecondaryEstimatedQty(pieces, unit = this.secondary_uom_id) {
        return this.product_id.uom_id.round(pieces * (unit?.factor || 1));
    },

    /** Pieces estimated from the current primary qty. */
    getSecondaryQtyFromQty(unit = this.secondary_uom_id) {
        if (!unit?.factor) {
            return 0;
        }
        const pieces = unit.uom_id.round(this.qty / unit.factor);
        // Never show 0 pieces for a non-zero weight.
        if (!pieces && this.qty) {
            return Math.sign(this.qty) * (unit.uom_id.rounding || 1);
        }
        return pieces;
    },

    /**
     * Whether the current qty is still the automatic estimate (pieces x factor),
     * i.e. nobody has weighed it or typed a real weight yet.
     */
    get isQtySecondaryEstimate() {
        const unit = this.secondary_uom_id;
        if (!unit || unit.dependency_type !== "dependent" || this.isWeighedWithScale) {
            return false;
        }
        const estimate = this.getSecondaryEstimatedQty(this.secondary_uom_qty);
        return this.product_id.uom_id.isZero(Math.abs(this.qty) - Math.abs(estimate));
    },

    /**
     * Set unit + number of pieces. Only "dependent" units estimate the weight
     * as pieces x factor (on a new line, or while it is still that estimate):
     * a weighed or manually typed weight is always kept.
     * With "independent" units the weight is never touched: it is typed or
     * weighed afterwards.
     */
    setSecondaryUomQty(pieces, unit = this.secondary_uom_id || this.productSecondaryUnit, { forceEstimate = false } = {}) {
        if (!unit) {
            return;
        }
        const recomputeQty =
            unit.dependency_type === "dependent" &&
            !this.isWeighedWithScale &&
            (forceEstimate || !this.secondary_uom_id || this.isQtySecondaryEstimate);
        const signedPieces = this.qty < 0 ? -Math.abs(pieces) : Math.abs(pieces);
        this.update({ secondary_uom_id: unit, secondary_uom_qty: signedPieces });
        if (recomputeQty) {
            this.setQuantity(this.getSecondaryEstimatedQty(signedPieces, unit));
        }
    },

    /** e.g. "2" */
    get secondaryUomQtyStr() {
        return formatFloat(Math.abs(this.secondary_uom_qty || 0), {
            digits: [69, this.secondary_uom_id?.uom_id?.rounding < 1 ? 2 : 0],
            trailingZeros: false,
        });
    },

    /** e.g. "2 Ud" (short form, used on the pieces button) */
    get secondaryUomLabel() {
        if (!this.secondary_uom_id || !this.secondary_uom_qty) {
            return "";
        }
        return `${this.secondaryUomQtyStr} ${this.secondary_uom_id.name}`;
    },

    /** e.g. "2 Ud de 1,5 kg" (pieces + nominal weight of each piece) */
    get secondaryUomDescription() {
        const unit = this.secondary_uom_id;
        if (!unit || !this.secondary_uom_qty) {
            return "";
        }
        return _t("%(qty)s %(unit)s of %(factor)s %(uom)s", {
            qty: this.secondaryUomQtyStr,
            unit: unit.name,
            factor: formatFloat(unit.factor, { digits: [69, 3], trailingZeros: false }),
            uom: this.product_id.uom_id?.name || "",
        });
    },

    canBeMergedWith(orderline) {
        // Each line keeps its own piece count: "2 x 1.5 kg" and "1 x 3 kg"
        // must never be merged into a single "4.5 kg" line.
        if (
            this.secondary_uom_id ||
            orderline.secondary_uom_id ||
            this.productSecondaryUnit ||
            orderline.productSecondaryUnit
        ) {
            return false;
        }
        return super.canBeMergedWith(...arguments);
    },
});

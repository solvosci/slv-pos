// Copyright 2026 Solvos
// License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { useHotkey } from "@web/core/hotkeys/hotkey_hook";
import { _t } from "@web/core/l10n/translation";
import { formatFloat } from "@web/core/utils/numbers";
import { useService } from "@web/core/utils/hooks";
import { parseFloat } from "@web/views/fields/parsers";
import { Numpad } from "@point_of_sale/app/components/numpad/numpad";

/**
 * Choose one of the product's secondary units (e.g. "Ud1.5", "Ud2", "Ud1")
 * and how many of them.  Resolves with { unit, pieces }.
 */
export class SecondaryUnitPopup extends Component {
    static template = "pos_order_secondary_unit.SecondaryUnitPopup";
    static components = { Dialog, Numpad };
    static props = {
        productName: String,
        uomName: { type: String, optional: true },
        units: Array,
        unit: Object,
        startingValue: { type: [Number, String], optional: true },
        getPayload: Function,
        close: Function,
    };
    static defaultProps = { startingValue: "1", uomName: "" };

    setup() {
        this.numberBuffer = useService("number_buffer");
        this.numberBuffer.use({
            triggerAtInput: ({ buffer }) => (this.state.buffer = buffer),
        });
        useHotkey("enter", () => this.confirm());
        useHotkey("escape", () => this.cancel());
        this.state = useState({
            buffer: `${this.props.startingValue}`,
            unitId: this.props.unit.id,
        });
    }

    get title() {
        return _t("%s: unit and quantity", this.props.productName);
    }

    get selectedUnit() {
        return this.props.units.find((u) => u.id === this.state.unitId) || this.props.unit;
    }

    get pieces() {
        try {
            return parseFloat(`${this.state.buffer || ""}`);
        } catch {
            return NaN;
        }
    }

    get isValid() {
        return this.pieces > 0;
    }

    formatNumber(value) {
        return formatFloat(value, { digits: [69, 3], trailingZeros: false });
    }

    unitFactorLabel(unit) {
        return `${this.formatNumber(unit.factor)} ${this.props.uomName}`;
    }

    /** e.g. "≈ 3 kg" */
    get estimateLabel() {
        if (!this.isValid) {
            return "";
        }
        return `≈ ${this.formatNumber(this.pieces * this.selectedUnit.factor)} ${this.props.uomName}`;
    }

    selectUnit(unit) {
        this.state.unitId = unit.id;
    }

    confirm() {
        if (!this.isValid) {
            return;
        }
        this.props.getPayload({ unit: this.selectedUnit, pieces: this.pieces });
        this.props.close();
    }

    cancel() {
        this.props.close();
    }
}

/** @odoo-module */
// © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
// License LGPL-3.0 (https://www.gnu.org/licenses/lgpl-3.0.html)

import { Orderline } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";


patch(Orderline.prototype, {
    setup(_defaultObj, options) {
        super.setup(...arguments);
        this.color_code_tintometric = this.color_code_tintometric || null;
    },

    get_tintometric_code() {
        return this.color_code_tintometric;
    },

    set_tintometric_code(code_tintometric) {
        this.color_code_tintometric = code_tintometric || "";
    },

    getDisplayData() {
        let data = super.getDisplayData();
        data.color_code_tintometric = this.color_code_tintometric;
        return data;
    },

    export_as_JSON() {
        let data = super.export_as_JSON();
        data.color_code_tintometric = this.get_tintometric_code();
        return data;
    },

    init_from_JSON(json) {
        super.init_from_JSON(json);
        this.set_tintometric_code(json.color_code_tintometric);
    }
});

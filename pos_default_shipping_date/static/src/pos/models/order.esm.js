/** @odoo-module **/
// © 2024 Solvos Consultoría Informática (<http://www.solvos.es>)
// License LGPL-3.0 (https://www.gnu.org/licenses/lgpl-3.0.html)
import {Order} from "@point_of_sale/app/store/models";
import {patch} from "@web/core/utils/patch";

patch(Order.prototype, {
    setup(_defaultObj, options) {
        super.setup(...arguments);
        this.shippingDate = new Date().toISOString().split("T")[0]
    },
});

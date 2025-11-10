/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { SaleOrderManagementScreen } from "@pos_sale/app/order_management_screen/sale_order_management_screen/sale_order_management_screen";

const _original_onClickSaleOrder = SaleOrderManagementScreen.prototype.onClickSaleOrder;

patch(SaleOrderManagementScreen.prototype,  {
    async onClickSaleOrder(clickedOrder) {
        if (_original_onClickSaleOrder) {
            await _original_onClickSaleOrder.call(this, clickedOrder);
        }

        const order = this.pos.get_order();

        order.get_orderlines().forEach(line => {
            if (line.sale_order_line_id && line.sale_order_line_id.color_code_tintometric) {
                line.color_code_tintometric = line.sale_order_line_id.color_code_tintometric;
            }
        });
    },
});

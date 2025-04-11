/** @odoo-module **/
// © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
// License LGPL-3.0 (https://www.gnu.org/licenses/lgpl-3.0.html)

import { ReceiptScreen } from "@point_of_sale/app/screens/receipt_screen/receipt_screen";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";
import { usePos } from "@point_of_sale/app/store/pos_hook";

patch(ReceiptScreen.prototype, {
    setup(_defaultObj, options) {
        super.setup(...arguments);
        this.pos = usePos();
        this.orm = useService("orm");
        this.report = useService("report");
        this.popup = useService("popup");
    },

    async printInvoiceReport() {
        const order = this.currentOrder;
        const orderId = order?.server_id;

        if (!orderId) {
            console.error(_t("POS Order not found."));
            alert(_t("POS Order not found."));
            return;
        }

        try {
            const [orderWithInvoice] = await this.orm.read(
                "pos.order",
                [orderId],
                ["account_move", "partner_id"],
                { load: false }
            );
            if (orderWithInvoice?.account_move) {
                await this.report.doAction("account.account_invoices", [
                    orderWithInvoice.account_move,
                ]);
                return;
            } else{
                console.error(_t("Invoice not found"));
                alert(_t("Invoice not found"));
                return;
            }
        } catch (error) {
            console.error("Error to process the invoice:", error);
        }
    },

});

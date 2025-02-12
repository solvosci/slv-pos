/** @odoo-module **/
// © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
// License LGPL-3.0 (https://www.gnu.org/licenses/lgpl-3.0.html)

import { TicketScreen } from "@point_of_sale/app/screens/ticket_screen/ticket_screen";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";
import { usePos } from "@point_of_sale/app/store/pos_hook";

patch(TicketScreen.prototype, {
    setup(_defaultObj, options) {
        super.setup(...arguments);
        this.pos = usePos();
        this.orm = useService("orm");
        this.report = useService("report");
    },
    async printStockPicking() {
        const order = this.getSelectedOrder().backendId;

        if (!order) {
            console.error(_t("Pos Order not found."));
            return;
        }

        try {
            const picking_ids = await this.orm.call("pos.session", "get_picking_id", [
                this.pos.pos_session.id,
                order,
            ]);

            if (!picking_ids) {
                console.error(_t("Picking not found"));
                alert(_t("Picking not found"));
                return;
            }

            return this.report.doAction("stock.action_report_delivery",
                picking_ids
            );
        } catch (error) {
            console.error("Error en la llamada RPC:", error);
        }
    },
});

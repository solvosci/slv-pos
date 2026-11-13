import {TicketScreen} from "@point_of_sale/app/screens/ticket_screen/ticket_screen";
import {_t} from "@web/core/l10n/translation";
import {patch} from "@web/core/utils/patch";

patch(TicketScreen.prototype, {
    _getSearchFields() {
        return {
            ...super._getSearchFields(...arguments),
            PHONE: {
                repr: (order) => order.getPartner()?.phone || "",
                displayName: _t("Phone"),
                modelFields: ["partner_id.phone"],
            },
        };
    },
});

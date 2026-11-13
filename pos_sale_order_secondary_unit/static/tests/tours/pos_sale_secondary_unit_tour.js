// Copyright 2026 Solvos
// License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import * as Chrome from "@point_of_sale/../tests/pos/tours/utils/chrome_util";
import * as Dialog from "@point_of_sale/../tests/generic_helpers/dialog_util";
import * as PaymentScreen from "@point_of_sale/../tests/pos/tours/utils/payment_screen_util";
import * as PosSale from "@pos_sale/../tests/tours/utils/pos_sale_utils";
import * as ProductScreen from "@point_of_sale/../tests/pos/tours/utils/product_screen_util";
import * as ReceiptScreen from "@point_of_sale/../tests/pos/tours/utils/receipt_screen_util";
import { registry } from "@web/core/registry";

registry.category("web_tour.tours").add("PosSaleSecondaryUnitTour", {
    steps: () =>
        [
            Chrome.startPoS(),
            Dialog.confirm("Open Register"),
            PosSale.settleNthOrder(1),
            {
                content: "a single cake line (not split into 1 + 1 + 1 + 0.2)",
                trigger: ".order-container:not(:has(.orderline:nth-child(2) .product-name:contains('SO Cake')))",
            },
            ProductScreen.selectedOrderlineHas("SO Cake", "3.2"),
            {
                content: "pieces come from the sale order line",
                trigger: ".order-container .orderline .o_secondary_uom_info:contains('2 Ud1.5 of 1.5 kg')",
            },
            ProductScreen.clickPayButton(),
            PaymentScreen.clickPaymentMethod("Bank", true, { remaining: "0.0" }),
            PaymentScreen.clickValidate(),
            ReceiptScreen.isShown(),
        ].flat(),
});

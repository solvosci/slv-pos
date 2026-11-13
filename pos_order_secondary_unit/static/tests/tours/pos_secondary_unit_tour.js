// Copyright 2026 Solvos
// License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import * as Chrome from "@point_of_sale/../tests/pos/tours/utils/chrome_util";
import * as Dialog from "@point_of_sale/../tests/generic_helpers/dialog_util";
import * as NumberPopup from "@point_of_sale/../tests/generic_helpers/number_popup_util";
import * as Order from "@point_of_sale/../tests/generic_helpers/order_widget_util";
import * as PaymentScreen from "@point_of_sale/../tests/pos/tours/utils/payment_screen_util";
import * as ProductScreen from "@point_of_sale/../tests/pos/tours/utils/product_screen_util";
import * as ReceiptScreen from "@point_of_sale/../tests/pos/tours/utils/receipt_screen_util";
import { inLeftSide } from "@point_of_sale/../tests/pos/tours/utils/common";
import { registry } from "@web/core/registry";

const piecesOnSelectedLine = (label) => ({
    content: `selected line shows '${label}'`,
    trigger: `.order-container .orderline.selected .o_secondary_uom_info:contains("${label}")`,
});
const unitPopupIsShown = () => ({
    content: "unit popup is shown",
    trigger: ".modal .o_secondary_unit_popup",
});
const chooseUnit = (name) => ({
    content: `choose unit ${name}`,
    trigger: `.modal .o_secondary_unit_choice[data-unit-name="${name}"]`,
    run: "click",
});
const unitIsChosen = (name) => ({
    content: `unit ${name} is selected`,
    trigger: `.modal .o_secondary_unit_choice.active[data-unit-name="${name}"]`,
});

registry.category("web_tour.tours").add("PosOrderSecondaryUnitTour", {
    steps: () =>
        [
            Chrome.startPoS(),
            Dialog.confirm("Open Register"),

            // 1. Tap the cake: choose unit "Ud2" (independent) and 2 of them:
            //    the weight is not estimated (stays at the default 1 kg).
            ProductScreen.clickDisplayedProduct("Secondary Cake"),
            unitPopupIsShown(),
            unitIsChosen("Ud"), // default secondary unit for sales
            chooseUnit("Ud2"),
            unitIsChosen("Ud2"),
            NumberPopup.enterValue("2"),
            NumberPopup.isShown("2"),
            Dialog.confirm(),
            Order.hasLine({ withClass: ".selected", productName: "Secondary Cake", quantity: "1" }),
            piecesOnSelectedLine("2 Ud2 of 2 kg"),

            // 2. The real weight is 4.1 kg: pieces must stay at 2.
            ProductScreen.clickNumpad("4", ".", "1"),
            Order.hasLine({ withClass: ".selected", productName: "Secondary Cake", quantity: "4.1" }),
            piecesOnSelectedLine("2 Ud2 of 2 kg"),

            // 3. Change to 3 x "Ud" (1.5 kg) with the pieces button: weight was
            //    typed, so it is kept (4.1).
            inLeftSide([
                {
                    content: "click pieces button",
                    trigger: ".o_secondary_uom_button",
                    run: "click",
                },
            ]),
            unitIsChosen("Ud2"),
            chooseUnit("Ud"),
            NumberPopup.enterValue("3"),
            Dialog.confirm(),
            piecesOnSelectedLine("3 Ud of 1.5 kg"),
            Order.hasLine({ withClass: ".selected", productName: "Secondary Cake", quantity: "4.1" }),

            // 4. Tapping the same product again must NOT merge lines.
            ProductScreen.clickDisplayedProduct("Secondary Cake"),
            unitPopupIsShown(),
            Dialog.confirm(),
            piecesOnSelectedLine("1 Ud of 1.5 kg"),
            Order.hasLine({ withClass: ".selected", productName: "Secondary Cake", quantity: "1.5" }),
            Order.hasLine({ productName: "Secondary Cake", quantity: "4.1" }),

            // 5. Pay and check the receipt shows the pieces.
            ProductScreen.clickPayButton(),
            PaymentScreen.clickPaymentMethod("Bank"),
            PaymentScreen.clickValidate(),
            ReceiptScreen.receiptIsThere(),
            {
                content: "receipt shows pieces",
                trigger: ".pos-receipt .o_secondary_uom_info:contains('3 Ud of 1.5 kg')",
            },
        ].flat(),
});

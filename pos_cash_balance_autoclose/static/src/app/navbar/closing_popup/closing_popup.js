/** @odoo-module */
// © 2026 Solvos Consultoría Informática (<http://www.solvos.es>)
// License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

import { patch } from "@web/core/utils/patch";
import { ClosePosPopup } from "@point_of_sale/app/navbar/closing_popup/closing_popup";
import { MoneyDetailsPopup } from "@point_of_sale/app/utils/money_details_popup/money_details_popup";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { _t } from "@web/core/l10n/translation";
import { parseFloat } from "@web/views/fields/parsers";

function parseAmount(value, env) {
    if (value === undefined || value === null || value === "") {
        return 0;
    }
    if (!env.utils.isValidFloat(value)) {
        return 0;
    }
    return parseFloat(value);
}

patch(ClosePosPopup.prototype, {
    getInitialState() {
        const state = super.getInitialState();
        const cashDetails = this.props.default_cash_details;

        if (
            this.pos.pos_session.pos_cash_balance_manual_allowed &&
            cashDetails &&
            typeof cashDetails.amount === "number" &&
            typeof cashDetails.opening === "number"
        ) {
            const suggestedCashOut = Math.max(
                cashDetails.amount - cashDetails.opening,
                0
            );

            state.manual_cash_out = this.env.utils.formatCurrency(
                suggestedCashOut,
                false
            );
        } else {
            state.manual_cash_out = "";
        }

        return state;
    },

    _onManualCashKeydown(event) {
        event.stopPropagation();
    },

    setManualWithdrawInput(value) {
        if (this.env.utils.isValidFloat(value) && this.manualMoneyDetails) {
            this.manualMoneyDetails = null;
        }
    },

    openManualWithdrawDetailsPopup() {
        return this.openDetailsPopup("manual_cash_out");
    },

    async openDetailsPopup(target = "counted") {
        const action = _t("Cash control - closing");
        this.hardwareProxy.openCashbox(action);

        const isManual = target === "manual_cash_out";

        const { confirmed, payload } = await this.popup.add(MoneyDetailsPopup, {
            moneyDetails: isManual ? this.manualMoneyDetails : this.moneyDetails,
            action: action,
        });

        if (!confirmed) {
            return;
        }

        const { total, moneyDetailsNotes, moneyDetails } = payload;
        const formattedTotal = this.env.utils.formatCurrency(total, false);

        if (isManual) {
            this.state.manual_cash_out = formattedTotal;
            this.manualMoneyDetails = moneyDetails;
        } else {
            this.state.payments[this.props.default_cash_details.id].counted =
                formattedTotal;
            this.moneyDetails = moneyDetails;
        }

        if (moneyDetailsNotes) {
            if (isManual) {
                this.manualMoneyDetailsNotes = moneyDetailsNotes;
            } else {
                this.state.notes = moneyDetailsNotes;
            }
        }
    },

    async _cashOut({ amount }) {
        if (amount <= 0) {
            return;
        }

        const pos = this.pos;

        await this.orm.call(
            "pos.session",
            "try_cash_in_out",
            [
                [pos.pos_session.id],
                "out",
                amount,
                _t("Cash closure"),
                {
                    formattedAmount: this.env.utils.formatCurrency(amount),
                    translatedType: _t("out"),
                },
            ],
            {
                context: {
                    pos_close_cash_sudo: true,
                },
            }
        );
    },

    get cashRemainingAfterClosing() {
        const cashDetails = this.props.default_cash_details;
        if (!cashDetails) {
            return 0;
        }

        const expectedCash = Number(cashDetails.amount) || 0;
        const manualWithdraw = Math.max(
            parseAmount(this.state.manual_cash_out, this.env),
            0
        );

        return Math.max(expectedCash - manualWithdraw, 0);
    },

    get isCashRemainingDifferentFromOpening() {
        const cashDetails = this.props.default_cash_details;
        if (!cashDetails) {
            return false;
        }

        const openingCash = Number(cashDetails.opening) || 0;
        const remainingCash = this.cashRemainingAfterClosing;

        return Math.abs(remainingCash - openingCash) > 0.00001;
    },

    async closeSession() {
        const pos = this.pos;

        if (!pos.config.cash_control) {
            return super.closeSession();
        }

        const cashDetails = this.props.default_cash_details;
        if (!cashDetails) {
            return super.closeSession();
        }

        const cashPaymentMethodId = cashDetails.id;
        const paymentState = this.state.payments[cashPaymentMethodId];
        if (!paymentState) {
            return super.closeSession();
        }

        const expectedCash = Number(cashDetails.amount) || 0;
        const openingCash = Number(cashDetails.opening) || 0;
        const originalCounted = parseAmount(paymentState.counted, this.env);

        let cashOut = 0;

        if (pos.pos_session.pos_cash_balance_manual_allowed) {
            cashOut = Math.max(
                parseAmount(this.state.manual_cash_out, this.env),
                0
            );
        } else {
            cashOut = Math.max(expectedCash - openingCash, 0);
        }

        if (cashOut > expectedCash) {
            await this.popup.add(ErrorPopup, {
                title: _t("Invalid cash out"),
                body: _t(
                    "You are trying to cash out more than the expected cash in the drawer."
                ),
            });
            return;
        }

        if (cashOut > 0) {
            await this._cashOut({ amount: cashOut });
        }

        const finalCash = Math.max(originalCounted - cashOut, 0);
        paymentState.counted = this.env.utils.formatCurrency(
            finalCash,
            false
        );

        return super.closeSession();
    },
});

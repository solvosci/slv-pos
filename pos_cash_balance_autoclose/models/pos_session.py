# © 2026 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import models, fields


class PosSession(models.Model):
    _inherit = "pos.session"

    pos_cash_balance_manual_allowed = fields.Boolean(
        related="config_id.pos_cash_balance_manual_allowed",
        readonly=True,
    )

    def _loader_params_pos_session(self):
        res = super()._loader_params_pos_session()
        res["search_params"]["fields"].append(
            "pos_cash_balance_manual_allowed"
        )
        return res

    def _get_pos_ui_pos_config(self, params):
        res = super()._get_pos_ui_pos_config(params)
        res["has_cash_move_permission"] = self.user_has_groups(
            "point_of_sale.group_pos_user"
        )
        return res

    def _validate_session(
        self,
        balancing_account=False,
        amount_to_balance=0,
        bank_payment_method_diffs=None,
    ):
        self.ensure_one()

        cash_difference = self.cash_register_difference

        res = super()._validate_session(
            balancing_account=balancing_account,
            amount_to_balance=amount_to_balance,
            bank_payment_method_diffs=bank_payment_method_diffs,
        )

        if cash_difference:
            self.cash_register_balance_end_real -= cash_difference

        return res

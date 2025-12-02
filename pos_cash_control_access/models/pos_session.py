# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import models


class PosSession(models.Model):
    _inherit = "pos.session"

    def _get_pos_ui_pos_config(self, params):
        res = super(PosSession, self)._get_pos_ui_pos_config(params)
        res['has_cash_move_permission'] = self.user_has_groups('point_of_sale.group_pos_user')
        return res

    def try_cash_in_out(self, _type, amount, reason, extras):
        self = self.with_context(pos_cash_inout_sudo=True)
        return super().try_cash_in_out(_type, amount, reason, extras)

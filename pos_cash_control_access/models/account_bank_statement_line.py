# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import models, api


class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'

    @api.model
    def create(self, vals_list):
        if self._context.get('pos_cash_inout_sudo'):
            return super(
                AccountBankStatementLine,
                self.sudo()
            ).create(vals_list)

        return super().create(vals_list)

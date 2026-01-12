# © 2026 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import models, fields


class PosConfig(models.Model):
    _inherit = "pos.config"

    pos_cash_balance_manual_allowed = fields.Boolean(
        string="Allow manual cash balance on close", 
        default=False, 
        help="Allows manual entry of the cash amount you want to cash out from the till during the logout menu.",
    )

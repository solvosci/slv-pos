# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    pos_order_line_id = fields.Many2many("pos.order.line")
    color_code_tintometric_pos = fields.Char(compute="_compute_color_code_tintometric_pos", string="Lot/S.Tin pos")

    @api.depends('pos_order_line_id.color_code_tintometric')
    def _compute_color_code_tintometric_pos(self):
        for record in self:
            record.color_code_tintometric_pos = record.pos_order_line_id.color_code_tintometric

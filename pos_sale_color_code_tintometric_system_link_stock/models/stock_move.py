# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = "stock.move"

    move_color_code_tintometric = fields.Char(compute="_compute_move_color_code_tintometric", string="Lot/S.Tin", store=True)

    @api.depends("move_color_code_tintometric_pos","color_code_tintometric")
    def _compute_move_color_code_tintometric(self):
        for move in self:
            move.move_color_code_tintometric = (
                move.move_color_code_tintometric_pos
                or move.color_code_tintometric
            )

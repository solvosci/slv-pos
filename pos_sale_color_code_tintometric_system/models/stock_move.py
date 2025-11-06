# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = "stock.move"

    move_pos_order_line_ids = fields.Many2many("pos.order.line")
    move_color_code_tintometric_pos = fields.Char(related="move_pos_order_line_ids.color_code_tintometric", string="Lot/S.Tin pos")

class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def _get_aggregated_product_quantities(self, **kwargs):
        aggregated_move_lines = super()._get_aggregated_product_quantities(**kwargs)
        for key, vals in aggregated_move_lines.items():

            vals['move_color_code_tintometric_pos'] = (
                vals.get('move').move_color_code_tintometric_pos
            )

        return aggregated_move_lines

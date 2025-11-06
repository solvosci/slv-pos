# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import models


class StockMove(models.Model):
    _inherit = "stock.picking"

    def _create_picking_from_pos_order_lines(self, location_dest_id, lines, picking_type, partner=False):
        pickings = super()._create_picking_from_pos_order_lines(location_dest_id, lines, picking_type, partner=False)

        for picking in pickings:
            for move in picking.move_ids_without_package:
                pos_lines = lines.filtered(
                    lambda l: l.product_id == move.product_id
                )

                move.move_pos_order_line_ids = [(6, 0, pos_lines.ids)]

        return pickings

# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html
from odoo import models


class PosSession(models.Model):
    _inherit = "pos.session"

    def get_picking_id(self, order_id):
        pos_order_id = self.env['pos.order'].sudo().browse(order_id)
        if pos_order_id.exists() and pos_order_id.picking_ids:
            return pos_order_id.picking_ids.ids

        return False

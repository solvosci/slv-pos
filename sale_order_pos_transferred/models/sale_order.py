# © 2024 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html
from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    has_pos_orders = fields.Boolean(
        compute="_compute_has_pos_orders",
        store=True,
    )

    @api.depends("pos_order_line_ids")
    def _compute_has_pos_orders(self):
        for order in self:
            order.has_pos_orders = bool(order.pos_order_line_ids)

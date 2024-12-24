# © 2024 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html
from odoo import models


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    def _prepare_procurement_group_vals(self):
        values = super()._prepare_procurement_group_vals()
        if self.sale_order_origin_id:
            values["partner_id"] = self.sale_order_origin_id.partner_shipping_id.id
        return values
    
    def _prepare_procurement_values(self, group_id=False):
        values = super()._prepare_procurement_values(group_id=group_id)
        if self.sale_order_origin_id:
            values["partner_id"] = self.sale_order_origin_id.partner_shipping_id.id
        return values

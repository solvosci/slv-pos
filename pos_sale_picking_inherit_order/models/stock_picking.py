# © 2024 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html
from odoo import api, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.model
    def _create_picking_from_pos_order_lines(
        self,
        location_dest_id,
        lines,
        picking_type,
        partner=False
    ):
        sale_order_origin_ids = lines.sudo().sale_order_origin_id
        if sale_order_origin_ids:
            partner = sale_order_origin_ids[0].partner_shipping_id
        # TODO cover negative/return pickings ?? Not sure if this is needed
        # See https://github.com/odoo/odoo/blob/8f6aad85107bfe857759d27c9a2a5080160894a6/addons/point_of_sale/models/stock_picking.py#L30
        return super()._create_picking_from_pos_order_lines(
            location_dest_id,
            lines,
            picking_type,
            partner=partner
        )

    def _get_client_order_ref(self):
        order_ref = self.sudo().sale_id.client_order_ref
        origin_sale_ids = self.sudo().pos_order_id.lines.sale_order_origin_id
        if origin_sale_ids:
            origin_order_refs = origin_sale_ids.mapped("client_order_ref")
            order_ref = "%s%s%s" % (
                order_ref or "",
                " // " if order_ref and origin_order_refs else "",
                origin_order_refs and ", ".join(origin_order_refs),
            )
        return order_ref

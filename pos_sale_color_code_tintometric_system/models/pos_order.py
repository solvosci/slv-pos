# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import models


class PosOrder(models.Model):
    _inherit = "pos.order"

    def _prepare_invoice_lines(self):
        invoice_lines = super()._prepare_invoice_lines()

        for pos_line in self.lines:
            for inv_tuple in invoice_lines:
                vals = inv_tuple[2]

                if vals.get("product_id") == pos_line.product_id.id:
                    vals["pos_order_line_id"] = [(6, 0, [pos_line.id])]
                    break

        return invoice_lines

# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def read_converted(self):
        results = super().read_converted()

        for res in results:
            origin_line = self.filtered(lambda l: l.id == res.get('id'))
            if origin_line:
                res['color_code_tintometric'] = origin_line.color_code_tintometric
        return results

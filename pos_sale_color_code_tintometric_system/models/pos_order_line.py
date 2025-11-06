# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import models


class PosOrderLine(models.Model):
    _name = "pos.order.line"
    _inherit = ["pos.order.line", "color.tintometric.system.mixin"]

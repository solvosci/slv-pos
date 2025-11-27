# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import models, fields


class PosOrder(models.Model):
    _inherit = "pos.order"

    is_margins_costs_accessible_to_every_user = fields.Boolean(related="config_id.is_margins_costs_accessible_to_every_user")

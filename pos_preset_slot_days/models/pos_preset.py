# Copyright 2026 Solvos Consultoría Informática, S.L. (<https://www.solvos.es>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PosPreset(models.Model):
    _inherit = "pos.preset"

    slot_days = fields.Integer(
        string="Bookable days",
        default=7,
        help="Number of days, starting today, for which the PoS offers time slots.",
    )

    _slot_days_positive = models.Constraint(
        "CHECK(slot_days >= 1)",
        "The bookable days must be at least 1.",
    )

    @api.model
    def _load_pos_data_fields(self, config):
        return super()._load_pos_data_fields(config) + ["slot_days"]

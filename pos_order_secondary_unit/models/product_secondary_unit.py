# Copyright 2026 Solvos
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models


class ProductSecondaryUnit(models.Model):
    _name = "product.secondary.unit"
    _inherit = ["product.secondary.unit", "pos.load.mixin"]

    @api.model
    def _load_pos_data_domain(self, data, config):
        # Load the units of every product available in this PoS, not only the
        # products of the initial batch: the PoS loads products lazily
        # (load_product_from_pos) and their units must already be there.
        return [
            ("product_tmpl_id.company_id", "in", [config.company_id.id, False]),
            ("product_tmpl_id.available_in_pos", "=", True),
            ("product_tmpl_id.sale_ok", "=", True),
        ]

    @api.model
    def _load_pos_data_fields(self, config):
        return [
            "id",
            "name",
            "code",
            "product_tmpl_id",
            "product_id",
            "uom_id",
            "dependency_type",
            "factor",
            "write_date",
        ]

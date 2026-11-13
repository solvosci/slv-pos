# Copyright 2026 Solvos
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
from odoo.tools import float_compare, float_round


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    # Deliberately NOT based on ``product.secondary.unit.mixin``: in the PoS the
    # weight (qty) is the real, weighed or corrected figure and the number of
    # pieces is entered by the cashier. The mixin would recompute the pieces
    # from the weight on every write (3.1 kg / 1.5 = 2.07 pieces).
    secondary_uom_id = fields.Many2one(
        comodel_name="product.secondary.unit",
        string="Second unit",
        ondelete="restrict",
    )
    secondary_uom_qty = fields.Float(
        string="Secondary Qty",
        digits="Product Unit",
    )

    @api.model
    def _load_pos_data_fields(self, config):
        return super()._load_pos_data_fields(config) + [
            "secondary_uom_id",
            "secondary_uom_qty",
        ]

    def _format_secondary_number(self, value):
        """1.5 -> '1,5' (decimal separator of the user's language, no zeros)."""
        lang = self.env["res.lang"]._get_data(code=self.env.lang or "en_US")
        return f"{value:g}".replace(".", lang.decimal_point or ".")

    def _get_secondary_uom_label(self):
        """Human readable pieces, e.g. '2 Ud de 1,5 kg' (empty if not applicable)."""
        self.ensure_one()
        unit = self.secondary_uom_id
        if not unit or not self.secondary_uom_qty:
            return ""
        qty = float_round(
            abs(self.secondary_uom_qty),
            precision_rounding=unit.uom_id.rounding or 0.01,
        )
        return self.env._(
            "%(qty)s %(unit)s of %(factor)s %(uom)s",
            qty=self._format_secondary_number(qty),
            unit=unit.name,
            factor=self._format_secondary_number(unit.factor),
            uom=self.product_uom_id.name or self.product_id.uom_id.name or "",
        )

    def _prepare_refund_data(self, refund_order, PosPackOperationLot):
        vals = super()._prepare_refund_data(refund_order, PosPackOperationLot)
        if self.secondary_uom_id:
            vals["secondary_uom_id"] = self.secondary_uom_id.id
            refunded_qty = -vals.get("qty", 0.0)
            # Only a full refund gives an exact number of pieces; for partial
            # refunds we estimate proportionally (the cashier can fix it).
            full_refund = (
                not self.qty
                or float_compare(refunded_qty, self.qty, precision_digits=6) == 0
            )
            if full_refund:
                vals["secondary_uom_qty"] = -self.secondary_uom_qty
            else:
                vals["secondary_uom_qty"] = -float_round(
                    self.secondary_uom_qty * refunded_qty / self.qty,
                    precision_rounding=self.secondary_uom_id.uom_id.rounding or 0.01,
                )
        return vals


class PosOrder(models.Model):
    _inherit = "pos.order"

    def _get_invoice_lines_values(self, line_values, pos_line, move_type):
        vals = super()._get_invoice_lines_values(line_values, pos_line, move_type)
        label = pos_line._get_secondary_uom_label()
        if label and vals.get("display_type") != "line_section":
            vals["name"] = f"{vals.get('name') or ''}\n({label})".strip()
        return vals

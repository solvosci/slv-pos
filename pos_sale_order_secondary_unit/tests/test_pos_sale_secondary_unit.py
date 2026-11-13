# Copyright 2026 Solvos
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests import tagged

from odoo.addons.pos_sale.tests.test_pos_sale_flow import TestPoSSale


@tagged("post_install", "-at_install")
class TestPosSaleSecondaryUnit(TestPoSSale):
    def test_settle_sale_order_keeps_secondary_unit(self):
        kg = self.env.ref("uom.product_uom_kgm")
        # Required configuration: kg grouped in the PoS, so pos_sale does not
        # split the line into lines of 1 kg.
        kg.is_pos_groupable = True
        tmpl = self.env["product.template"].create(
            {
                "name": "SO Cake",
                "available_in_pos": True,
                "list_price": 20.0,
                "taxes_id": [(5, 0, 0)],
                "uom_id": kg.id,
            }
        )
        unit_15 = self.env["product.secondary.unit"].create(
            {
                "name": "Ud1.5",
                "uom_id": self.env.ref("uom.product_uom_unit").id,
                "factor": 1.5,
                "product_tmpl_id": tmpl.id,
                "dependency_type": "independent",
            }
        )
        self.env["product.secondary.unit"].create(
            {
                "name": "Ud2",
                "uom_id": self.env.ref("uom.product_uom_unit").id,
                "factor": 2.0,
                "product_tmpl_id": tmpl.id,
                "dependency_type": "independent",
            }
        )
        product = tmpl.product_variant_id
        sale_order = (
            self.env["sale.order"]
            .sudo()
            .create(
                {
                    "partner_id": self.env["res.partner"].create({"name": "Cliente"}).id,
                    "order_line": [
                        (
                            0,
                            0,
                            {
                                "product_id": product.id,
                                "secondary_uom_id": unit_15.id,
                                "secondary_uom_qty": 2,
                                "product_uom_qty": 3.2,
                                "price_unit": 20.0,
                            },
                        )
                    ],
                }
            )
        )
        sol = sale_order.order_line
        # independent unit: OCA keeps both quantities as entered
        self.assertAlmostEqual(sol.product_uom_qty, 3.2)
        self.assertAlmostEqual(sol.secondary_uom_qty, 2.0)

        self.main_pos_config.open_ui()
        self.start_pos_tour("PosSaleSecondaryUnitTour", login="accountman")

        pos_line = self.env["pos.order.line"].search(
            [("sale_order_line_id", "=", sol.id)]
        )
        self.assertEqual(len(pos_line), 1, "The line must not be split")
        self.assertAlmostEqual(pos_line.qty, 3.2)
        self.assertEqual(pos_line.secondary_uom_id, unit_15)
        self.assertAlmostEqual(pos_line.secondary_uom_qty, 2.0)

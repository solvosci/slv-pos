# Copyright 2026 Solvos
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests import tagged

from odoo.addons.point_of_sale.tests.test_frontend import TestPointOfSaleHttpCommon


@tagged("post_install", "-at_install")
class TestPosOrderSecondaryUnitUi(TestPointOfSaleHttpCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cake_tmpl = cls.env["product.template"].create(
            {
                "name": "Secondary Cake",
                "available_in_pos": True,
                "list_price": 20.0,
                "taxes_id": [(5, 0, 0)],
                "uom_id": cls.env.ref("uom.product_uom_kgm").id,
            }
        )
        cls.cake_piece = cls.env["product.secondary.unit"].create(
            {
                "name": "Ud",
                "uom_id": cls.env.ref("uom.product_uom_unit").id,
                "factor": 1.5,
                "product_tmpl_id": cake_tmpl.id,
                "dependency_type": "dependent",
            }
        )
        cls.cake_piece_2kg = cls.env["product.secondary.unit"].create(
            {
                "name": "Ud2",
                "uom_id": cls.env.ref("uom.product_uom_unit").id,
                "factor": 2.0,
                "product_tmpl_id": cake_tmpl.id,
                "dependency_type": "independent",
            }
        )
        cake_tmpl.sale_secondary_uom_id = cls.cake_piece
        cls.cake = cake_tmpl.product_variant_id

    def test_pos_secondary_unit_tour(self):
        self.main_pos_config.with_user(self.pos_user).open_ui()
        self.start_pos_tour("PosOrderSecondaryUnitTour", login="pos_user")
        order = self.env["pos.order"].search(
            [("lines.product_id", "=", self.cake.id)], order="id desc", limit=1
        )
        lines = order.lines.sorted("id")
        self.assertEqual(len(lines), 2, "Lines with pieces must not be merged")
        self.assertAlmostEqual(lines[0].qty, 4.1)
        self.assertAlmostEqual(lines[0].secondary_uom_qty, 3.0)
        self.assertEqual(lines[0].secondary_uom_id, self.cake_piece)
        self.assertEqual(lines[1].secondary_uom_id, self.cake_piece)
        self.assertAlmostEqual(lines[1].qty, 1.5)
        self.assertAlmostEqual(lines[1].secondary_uom_qty, 1.0)

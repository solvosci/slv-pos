# Copyright 2026 Solvos
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests import tagged

from odoo.addons.point_of_sale.tests.common import TestPoSCommon


@tagged("post_install", "-at_install")
class TestPosOrderSecondaryUnit(TestPoSCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.uom_kg = cls.env.ref("uom.product_uom_kgm")
        cls.uom_unit = cls.env.ref("uom.product_uom_unit")
        cls.cake = cls.create_product("Tarta de queso", cls.categ_basic, 20.0, 8.0)
        cls.cake.uom_id = cls.uom_kg
        cls.cake_piece = cls.env["product.secondary.unit"].create(
            {
                "name": "Ud",
                "uom_id": cls.uom_unit.id,
                "factor": 1.5,
                "product_tmpl_id": cls.cake.product_tmpl_id.id,
                "dependency_type": "dependent",
            }
        )
        cls.cake_piece_2kg = cls.env["product.secondary.unit"].create(
            {
                "name": "Ud2",
                "uom_id": cls.uom_unit.id,
                "factor": 2.0,
                "product_tmpl_id": cls.cake.product_tmpl_id.id,
                "dependency_type": "independent",
            }
        )
        cls.cake.sale_secondary_uom_id = cls.cake_piece

    def setUp(self):
        super().setUp()
        self.config = self.basic_config

    def _sync_cake_order(self, qty, pieces, **order_kwargs):
        order_data = self.create_ui_order_data(
            [
                {
                    "product": self.cake,
                    "quantity": qty,
                    "secondary_uom_id": self.cake_piece.id,
                    "secondary_uom_qty": pieces,
                }
            ],
            **order_kwargs,
        )
        res = self.env["pos.order"].sync_from_ui([order_data])
        return self.env["pos.order"].browse(res["pos.order"][0]["id"])

    def test_load_pos_data(self):
        self.open_new_session()
        params = self.pos_session.load_data_params()
        self.assertIn("product.secondary.unit", params)
        self.assertIn("sale_secondary_uom_id", params["product.product"]["fields"])
        self.assertIn("secondary_uom_qty", params["pos.order.line"]["fields"])
        data = self.pos_session.load_data(["product.secondary.unit"])
        unit_ids = [u["id"] for u in data["product.secondary.unit"]]
        self.assertIn(self.cake_piece.id, unit_ids)
        self.assertIn(self.cake_piece_2kg.id, unit_ids, "All units must be loaded")

    def test_unit_not_loaded_when_product_not_in_pos(self):
        self.cake.available_in_pos = False
        self.open_new_session()
        data = self.pos_session.load_data(["product.secondary.unit"])
        unit_ids = [u["id"] for u in data["product.secondary.unit"]]
        self.assertNotIn(self.cake_piece.id, unit_ids)

    def test_sync_keeps_pieces_and_real_weight(self):
        """2 cakes weighing 3.1 kg in total: pieces must NOT become 2.07."""
        self.open_new_session()
        order = self._sync_cake_order(3.1, 2)
        line = order.lines
        self.assertAlmostEqual(line.qty, 3.1)
        self.assertEqual(line.secondary_uom_id, self.cake_piece)
        self.assertAlmostEqual(line.secondary_uom_qty, 2.0)

    def test_invoice_line_shows_pieces(self):
        self.open_new_session()
        order = self._sync_cake_order(
            3.0, 2, customer=self.customer, is_invoiced=True
        )
        self.assertTrue(order.account_move)
        inv_line = order.account_move.invoice_line_ids.filtered(
            lambda aml: aml.product_id == self.cake
        )
        self.assertIn("(2 Ud of 1.5 kg)", inv_line.name)
        self.assertAlmostEqual(inv_line.quantity, 3.0)

    def test_full_refund_copies_pieces(self):
        self.open_new_session()
        order = self._sync_cake_order(3.0, 2)
        refund = self.env["pos.order"].browse(order.refund()["res_id"])
        self.assertEqual(refund.lines.secondary_uom_id, self.cake_piece)
        self.assertAlmostEqual(refund.lines.secondary_uom_qty, -2.0)
        self.assertAlmostEqual(refund.lines.qty, -3.0)

    def test_label(self):
        self.open_new_session()
        order = self._sync_cake_order(3.0, 2)
        self.assertEqual(order.lines._get_secondary_uom_label(), "2 Ud of 1.5 kg")

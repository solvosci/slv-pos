# Copyright 2026 Solvos Consultoría Informática, S.L. (<https://www.solvos.es>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from psycopg2 import IntegrityError

from odoo.tests import TransactionCase, tagged
from odoo.tools import mute_logger


@tagged("post_install", "-at_install")
class TestPosPresetSlotDays(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.preset = cls.env["pos.preset"].create({"name": "Encargo"})

    @mute_logger("odoo.sql_db")
    def test_slot_days_at_least_one(self):
        with self.assertRaises(IntegrityError):
            self.preset.slot_days = 0
            self.env.flush_all()

# Copyright 2026 Solvos Consultoría Informática, S.L. (<https://www.solvos.es>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "POS Preset Slot Days",
    "summary": "Configure how many days can be selected when scheduling PoS orders",
    "version": "19.0.1.0.0",
    "category": "Sales/Point of Sale",
    "website": "https://github.com/OCA/pos",
    "author": "Solvos, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["point_of_sale"],
    "data": ["views/pos_preset_views.xml"],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_preset_slot_days/static/src/app/models/pos_preset_slot_days.esm.js",
        ],
    },
}

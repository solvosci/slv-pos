# Copyright 2026 Solvos
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "POS Order Secondary Unit",
    "summary": "Sell in the Point of Sale with a secondary unit (pieces) "
    "while charging in the primary unit (kg)",
    "version": "19.0.1.0.0",
    "development_status": "Beta",
    "category": "Sales/Point of Sale",
    "website": "https://www.solvos.es",
    "author": "Solvos",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["point_of_sale", "sale_order_secondary_unit"],
    "data": ["views/pos_order_views.xml"],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_order_secondary_unit/static/src/**/*",
        ],
        "web.assets_tests": [
            "pos_order_secondary_unit/static/tests/tours/**/*",
        ],
    },
}

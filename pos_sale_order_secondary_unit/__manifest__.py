# Copyright 2026 Solvos
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "POS Sale Order Secondary Unit",
    "summary": "Keep the secondary unit and quantity when a sale order "
    "is settled in the Point of Sale",
    "version": "19.0.1.0.0",
    "development_status": "Beta",
    "category": "Sales/Point of Sale",
    "website": "https://www.solvos.es",
    "author": "Solvos",
    "license": "AGPL-3",
    "installable": True,
    "auto_install": True,
    "depends": ["pos_order_secondary_unit", "pos_sale"],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_sale_order_secondary_unit/static/src/**/*",
        ],
        "web.assets_tests": [
            "pos_sale_order_secondary_unit/static/tests/tours/**/*",
        ],
    },
}

# Copyright 2026 Solvos Consultoría Informática, S.L. (<https://www.solvos.es>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    "name": "POS Product Card Name Lines",
    "summary": "Show up to 4 lines of the product name on PoS product cards",
    "version": "19.0.1.0.0",
    "category": "Sales/Point of Sale",
    "website": "https://github.com/solvosci/slv-pos",
    "author": "Solvos",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": ["point_of_sale"],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_product_card_name_lines/static/src/app/components/product_card/pos_product_card_name_lines.scss",
        ],
    },
}

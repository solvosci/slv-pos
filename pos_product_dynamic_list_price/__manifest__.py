# © 2026 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html
{
    "name": "POS - Product Dynamic List Price",
    "summary": """
        Applies reference price list for a product to POS sessions
    """,
    "author": "Solvos",
    "license": "LGPL-3",
    "version": "17.0.1.0.0",
    "category": "Point Of Sale",
    "website": "https://github.com/solvosci/slv-pos",
    "depends": ["product_dynamic_list_price", "point_of_sale"],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_product_dynamic_list_price/static/src/js/product_price_patch.js",
        ],
    },
    "installable": True,
}

# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html
{
    "name": "POS Stock Picking Print Button",
    "summary": """
        Adds new button to print Picking Delivery from POS
    """,
    "author": "Solvos",
    "license": "LGPL-3",
    "version": "17.0.1.0.0",
    "category": "Sales/Sales",
    "website": "https://github.com/solvosci/slv-pos",
    "depends": ["point_of_sale"],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_stock_picking_print_button/static/src/app/screens/**/*',
        ],
    },
}

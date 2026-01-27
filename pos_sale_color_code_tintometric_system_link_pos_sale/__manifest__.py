# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html
{
    "name": "POS Sale Color Code Tintometric System Link POS Sale",
    "summary": """
        Link between ‘pos_sale_colour_code_tintometric_system’ and ‘pos_sale’
        to ensure that when a sales order is transferred to the POS,
        the 'Lot/S.Tin' field from pos.order.line is received.
    """,
    "author": "Solvos",
    "license": "LGPL-3",
    "version": "17.0.1.0.0",
    "category": "Sales/Sales",
    "website": "https://github.com/solvosci/slv-pos",
    "depends": ["pos_sale","pos_sale_color_code_tintometric_system", ],
    "data": [
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_sale_color_code_tintometric_system_link_pos_sale/static/src/app/sale_order_management_screen.js',
        ],
    },
}

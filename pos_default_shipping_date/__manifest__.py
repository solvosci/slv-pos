# © 2024 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3.0 (https://www.gnu.org/licenses/lgpl-3.0.html)
{
    "name": "Point Of Sale Default Shipping Date",
    "summary": """
        Adds default shipping date to today in the point of sale
    """,
    "author": "Solvos",
    "license": "LGPL-3",
    "version": "17.0.1.0.0",
    "category": "Extra Tools",
    "website": "https://github.com/solvosci/slv-pos",
    'depends': ['point_of_sale'],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_default_shipping_date/static/src/pos/**/*.js',
        ],
    },
    'installable': True,
}

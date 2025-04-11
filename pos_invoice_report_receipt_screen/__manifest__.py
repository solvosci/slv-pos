# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html
{
    "name": "POS Invoice Report Receipt Screen",
    "summary": """
        Adds new button to print order invoice from POS
    """,
    "author": "Solvos",
    "license": "LGPL-3",
    "version": "17.0.1.0.0",
    "category": "Sales/Sales",
    "website": "https://github.com/solvosci/slv-pos",
    "depends": [
        "point_of_sale",
        ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_invoice_report_receipt_screen/static/src/app/screens/receipt_screen/**',
        ],
    },
}

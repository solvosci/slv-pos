# © 2024 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3.0 (https://www.gnu.org/licenses/lgpl-3.0.html)
{
    "name": "Point Of Sale Font Size Ticket",
    "summary": """
        Customizes the font size of POS tickets
    """,
    "author": "Solvos",
    "license": "LGPL-3",
    "version": "17.0.1.0.0",
    "category": "Extra Tools",
    "website": "https://github.com/solvosci/slv-pos",
    'depends': ['point_of_sale'],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_font_size_ticket/static/src/css/pos_receipts.css',
            # 'pos_font_size_ticket/static/src/xml/template.xml',
        ],
    },
    'installable': True,
}

# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html
{
    "name": "POS Sale Color Code Tintometric System",
    "summary": """
        Add "Lot/S.Tin" field on POS order screen, POS receipt, order POS on backend, order invoice and order picking
    """,
    "author": "Solvos",
    "license": "LGPL-3",
    "version": "17.0.1.0.0",
    "category": "Sales/Sales",
    "website": "https://github.com/solvosci/slv-pos",
    "depends": ["sale_order_color_code_tintometric_system", "point_of_sale"],
    "data": [
        "views/pos_order_line_views.xml",
        "views/account_move_views.xml",
        "views/stock_move_views.xml",
        "report/account_move_report_templates.xml",
        "report/stock_picking_report_templates.xml"
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_sale_color_code_tintometric_system/static/src/app/screens/color_tintometric_system_button/**',
            'pos_sale_color_code_tintometric_system/static/src/app/screens/models.js',
            'pos_sale_color_code_tintometric_system/static/src/app/screens/orderline/**',
            'pos_sale_color_code_tintometric_system/static/src/app/screens/order_receipt/*',
            'pos_sale_color_code_tintometric_system/static/src/app/utils/input_popups/**',
        ],
    },
}

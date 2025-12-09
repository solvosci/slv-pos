# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html
{
    "name": "POS Sale Color Code Tintometric System Link Stock",
    "summary": """
        New 'Lot/S.Tin' field on Move Analysis filled from sale order line or pos order line
    """,
    "author": "Solvos",
    "license": "LGPL-3",
    "version": "17.0.1.0.0",
    "category": "Sales/Sales",
    "website": "https://github.com/solvosci/slv-pos",
    "depends": ["pos_sale_color_code_tintometric_system", "sale_order_color_code_tintometric_system_stock"],
    "data": [
        "views/stock_move_views.xml"
    ],
}

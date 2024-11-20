# © 2024 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html
{
    "name": "Sale Order - Point Of Sale transferred info",
    "summary": """
        Adds extra POS transferred info for a Sale Order
    """,
    "author": "Solvos",
    "license": "LGPL-3",
    "version": "17.0.1.0.0",
    "category": "Sales/Sales",
    "website": "https://github.com/solvosci/slv-pos",
    "depends": ["pos_sale"],
    "data": ["views/sale_order_views.xml"],
    "pre_init_hook": "pre_init_hook",
}

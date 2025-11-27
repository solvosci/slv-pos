# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html
{
    "name": "POS Margin Backend",
    "summary": """
        Hides margins and costs in the POS backend whenever the corresponding visibility option is disabled.
    """,
    "author": "Solvos",
    "license": "LGPL-3",
    "version": "17.0.1.0.0",
    "category": "Sales/Sales",
    "website": "https://github.com/solvosci/slv-pos",
    "depends": ["point_of_sale"],
    "data": [
        "views/pos_order_report_views.xml",
        "views/pos_order_views.xml",
    ],
    "installable": True,
}

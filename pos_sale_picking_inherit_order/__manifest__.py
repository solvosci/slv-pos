# © 2024 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html
{
    "name": "POS Order Generated Pickings - inherit sales order data",
    "summary": """
        Ensures that picking generated from a POS Order keeps some data that
        could have if it was directly generated from a Sales Order
    """,
    "author": "Solvos",
    "license": "LGPL-3",
    "version": "17.0.1.0.0",
    "category": "Sales/Sales",
    "website": "https://github.com/solvosci/slv-pos",
    "depends": ["pos_sale"],
    "data": ["report/stock_picking_report_templates.xml"],
}

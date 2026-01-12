# © 2026 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html
{
    "name": "POS Cash Balance Autoclose",
    "summary": """
        Extends the Point of Sale closing process by allowing cash
        outs from the cash register at session closing.
    """,
    "author": "Solvos",
    "license": "LGPL-3",
    "version": "17.0.1.0.0",
    "category": "Sales/Sales",
    "website": "https://github.com/solvosci/slv-pos",
    "depends": [
        "point_of_sale",
    ],
    "data": [
        "views/pos_config_view.xml",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_cash_balance_autoclose/static/src/app/navbar/closing_popup/closing_popup.xml",
            "pos_cash_balance_autoclose/static/src/app/navbar/closing_popup/closing_popup.js",
        ],
    },
    "installable": True,
}

# Copyright 2026 Solvos Consultoría Informática, S.L. (<https://www.solvos.es>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "POS Ticket Screen Phone Search",
    "summary": "Search PoS orders by customer phone",
    "version": "19.0.1.0.0",
    "category": "Sales/Point of Sale",
    "website": "https://github.com/OCA/pos",
    "author": "Solvos, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["point_of_sale"],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_ticket_screen_phone_search/static/src/app/screens/ticket_screen/pos_ticket_screen_phone_search.esm.js",
        ],
    },
}

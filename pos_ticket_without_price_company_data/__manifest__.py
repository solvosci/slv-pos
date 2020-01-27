# © 2019 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "POS Ticket Without Price Company Data",
    "summary": "Adds some company data to the receipt ticket without price",
    "version": "12.0.1.0.0",
    "author": "Solvos",
    "website": "http://www.github.com/solvosci/slv-pos",
    "license": "LGPL-3",
    "category": "Point Of Sale",
    "depends": [
        'pos_ticket_without_price'
    ],
    "qweb": [
        'static/src/xml/pos.xml',
    ],
    'installable': True,
}

# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html
{
    "name": "Point of Sale Security",
    "summary": """
        Restrict POS data that each user can access in:
            - pos.payment
            - pos.config
            - pos.order and pos.order.line
            - pos.session
            - report.pos.order
        To do this, a new security group, ‘Point of Sale: Super Admin’, is created
        and the permissions for the other groups are reduced.
    """,
    "author": "Solvos",
    "license": "LGPL-3",
    "version": "17.0.1.0.0",
    "category": "Sales/Sales",
    "website": "https://github.com/solvosci/slv-pos",
    "depends": ["pos_hr"],
    "data": [
        "security/pos_security.xml"
    ],
}

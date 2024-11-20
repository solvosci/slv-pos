# © 2024 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html
from odoo.tools import sql

import logging

_logger = logging.getLogger(__name__) 


def pre_init_hook(env):
    if not sql.column_exists(env.cr, "sale_order", "has_pos_orders"):
        sql.create_column(env.cr, "sale_order", "has_pos_orders", "boolean")

    _logger.info("Initializing has_pos_orders field")
    env.cr.execute(
        """
        UPDATE
            sale_order
        SET
            has_pos_orders = true
        FROM
            sale_order so
        INNER JOIN
            pos_order_line pol ON so.id = pol.sale_order_origin_id
        WHERE
            sale_order.id = so.id
        """
    )

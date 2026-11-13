Bridge between `pos_order_secondary_unit` and `pos_sale` (auto-installed).

When a quotation / sale order is settled in the Point of Sale:

- The secondary unit and the number of pieces of each `sale.order.line` are
  copied to the PoS line (proportionally if partially delivered/invoiced).

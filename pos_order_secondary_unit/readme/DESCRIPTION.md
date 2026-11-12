Brings the secondary unit of OCA `product_secondary_unit` /
`sale_order_secondary_unit` to the Point of Sale.

Typical case: cakes sold and charged **by kg**, where the shop staff must know
**how many pieces** make up that weight (2 cakes of ~1.5 kg = 3 kg is not the
same as 1 cake of 3 kg).

- Every PoS order line stores the number of pieces (`secondary_uom_qty`) and the
  unit (`secondary_uom_id`) next to the weight (`qty`).
- Pieces and weight are **independent once the weight is known**: weighing or
  typing the real weight (3.1 kg) never changes the piece count (2), unlike the
  sales mixin, which would turn it into 2.07.
- Pieces are shown on the order screen, on the customer receipt, on the backend
  PoS order and on the invoice line description.

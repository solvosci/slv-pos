No PoS-specific configuration. The module reuses the configuration of
`product_secondary_unit` / `sale_order_secondary_unit`:

1. On the product, unit of measure **kg**.
2. In *Secondary Unit of Measure* add one line per size, e.g.
   `Ud1.5` (factor 1.5), `Ud2` (factor 2), `Ud1` (factor 1).
   The factor is the estimated kg of one piece.
3. Optionally set one of them as *Default secondary unit for sales*: it is
   preselected in the PoS. Otherwise the smallest factor is preselected.
4. The product must be *Available in PoS*.
5. On the unit of measure **kg** check *Group Products in POS* (developer
   mode, *Sales → Configuration → Products → Units & Packagings*). Otherwise,
   when a sale order is settled in the PoS (`pos_sale`), its kg lines are
   split into lines of 1 kg and the pieces are lost.

Every active secondary unit of the product is offered in the PoS. The
*dependency type* is not used in the PoS (see USAGE).

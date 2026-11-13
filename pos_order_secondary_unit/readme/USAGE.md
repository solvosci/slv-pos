1. Tap the product: a popup shows **all its secondary units** as buttons
   (e.g. `Ud1.5 · 1,5 kg`, `Ud2 · 2 kg`, `Ud1 · 1 kg`) and a numpad.
   Choose the unit, type how many and confirm.
2. The weight is pre-filled as an estimate (2 × Ud1.5 = 3 kg). With an
   electronic scale, the weighed value is kept.
3. Type the real weight with the numpad if needed (e.g. 3,10): the pieces stay.
4. To change unit or pieces of the selected line use the **pieces button** in
   the control bar (desktop) or *Actions → Pieces* (small screens). The weight
   is only recalculated if it was still the automatic estimate.
5. Different sizes of the same product go in **separate lines**
   (2 × Ud1.5 and 1 × Ud2): lines with pieces are never merged.
6. Line, receipt and invoice show `3,10  Tarta de queso` + `2 Ud1.5 de 1,5 kg`.
7. Barcode scans do not ask: pieces are estimated as weight / factor of the
   default unit and can be fixed with the pieces button.
8. Refunds from the ticket screen inherit the unit and the pieces (proportional
   estimate for partial refunds).

Bridge modules (auto-installed):

- `pos_sale_order_secondary_unit`: settling a sale order keeps unit and pieces.
- `pos_restaurant_order_secondary_unit`: split bill by pieces.

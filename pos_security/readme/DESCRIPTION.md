Restrict POS data that each user can access in:
- pos.payment
- pos.config
- pos.order and pos.order.line
- pos.session
- report.pos.order
To do this, a new security group, ‘Point of Sale: Super Admin’, is created
and the permissions for the other groups are reduced.

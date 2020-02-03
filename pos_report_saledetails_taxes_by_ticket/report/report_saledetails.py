# © 2020 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import api, models, _


class ReportSaleDetails(models.AbstractModel):
    _inherit = 'report.point_of_sale.report_saledetails'

    @api.model
    def _prepare_orders(
            self, date_start=False, date_stop=False, configs=False):
        # TODO make PR to Odoo with this hook method
        return self.env['pos.order'].search([
            ('date_order', '>=', date_start),
            ('date_order', '<=', date_stop),
            ('state', 'in', ['paid', 'invoiced', 'done']),
            ('config_id', 'in', configs.ids)])

    @api.model
    def get_taxes_by_ticket(self, orders):
        # TODO move to pos.order, make @api.multi and make PR to Odoo with
        #      this hook method
        taxes_by_ticket = []
        for order in orders:
            currency = order.session_id.currency_id
            for line in order.lines:
                if line.tax_ids_after_fiscal_position:
                    line_taxes = \
                        line.tax_ids_after_fiscal_position.compute_all(
                            line.price_unit *
                            (1 - (line.discount or 0.0) / 100.0),
                            currency, line.qty, product=line.product_id,
                            partner=line.order_id.partner_id or False)
                    for tax in line_taxes['taxes']:
                        tax_detail = next(
                            (n for n in taxes_by_ticket
                             if n['id'] == tax['id']
                             and n['ticket'] == order.pos_reference), None)
                        if tax_detail:
                            tax_detail['tax_amount'] += tax['amount']
                            tax_detail['base_amount'] += tax['base']
                            tax_detail['total_amount'] += \
                                tax['base'] + tax['amount']
                        else:
                            taxes_by_ticket.append({
                                'id': tax['id'],
                                'ticket': order.pos_reference,
                                'name': tax['name'],
                                'tax_amount': tax['amount'],
                                'base_amount': tax['base'],
                                'total_amount': tax['amount'] + tax['base']})
                else:
                    no_tax_detail = next(
                        (n for n in taxes_by_ticket
                         if n['id'] == 0
                         and n['ticket'] == order.pos_reference), None)
                    if no_tax_detail:
                        no_tax_detail['base_amount'] += \
                            line.price_subtotal_incl
                        no_tax_detail['total_amount'] += \
                            line.price_subtotal_incl
                    else:
                        taxes_by_ticket.append({
                            'id': 0,
                            'ticket': order.pos_reference,
                            'name': _('No Taxes'),
                            'tax_amount': 0.0,
                            'base_amount': line.price_subtotal_incl,
                            'total_amount': line.price_subtotal_incl})

        taxes_by_ticket.sort(key=lambda x: x['ticket'])
        return taxes_by_ticket

    @api.model
    def get_sale_details(
            self, date_start=False, date_stop=False, configs=False):
        orders = self._prepare_orders(
            date_start=date_start, date_stop=date_stop, configs=configs)

        taxes_by_ticket = self.get_taxes_by_ticket(orders)
        sale_details = super().get_sale_details(
            date_start=date_start, date_stop=date_stop, configs=configs)
        sale_details['taxes_by_ticket'] = taxes_by_ticket

        return sale_details

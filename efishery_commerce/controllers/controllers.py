# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
import json, pytz


class EfisheryCommerce(http.Controller):
    @http.route('/api/order/create', type="json", auth="jwt",
        save_session=False, methods=['POST'])
    def generate(self, partner_id, order_line):
        if not partner_id or not order_line:
            return json.dumps({'status': "300"})

        order_id = request.env['sale.order'].create({
            'partner_id': partner_id
            })

        for line in order_line:
            order_id.order_line = [(0, 0, {
                'product_id': line.get('product_id'),
                'product_uom_qty': line.get('qty'),
                })]

        order_id.action_confirm()
        invoice_id = order_id._create_invoices()
        invoice_id.action_post()

        payment_id = request.env['account.payment.register'].with_context(
            active_model='account.move',
            active_ids=invoice_id.ids).new()
        payment_id._create_payments()
        result = {
            'order': {
                        'id': order_id.id,
                        'name': order_id.name},
            'invoice':{
                        'id': invoice_id.id,
                        'name': invoice_id.name}
        }
        return result

    @http.route('/api/order/get', type="json", auth="jwt",
        save_session=False, methods=['GET'])
    def get(self):
        tz = pytz.timezone(request.env.user.tz or 'Asia/Jakarta')
        order_ids = request.env['sale.order'].search([
            ('user_id','=',request.env.uid)
            ])
        result = []
        for order in order_ids:
            date_order = pytz.utc.localize(order.date_order).astimezone(tz)
            result.append({
                'id': order.id,
                'name': order.name,
                'customer': order.partner_id.display_name,
                'date': date_order
                })
        return result
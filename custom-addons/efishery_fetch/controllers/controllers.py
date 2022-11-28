# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from datetime import datetime
import requests, json


class EfisheryFetch(http.Controller):
    # @http.route('/api/fetch', methods=['GET'], auth="user", type="http")
    @http.route('/api/fetch', type="http", auth="jwt",
        save_session=False, methods=['GET'])
    def fetch(self, **kw):
        CurrencyRate = request.env['res.currency.rate']
        currency_id = request.env.ref('base.USD')

        now = datetime.now()
        last_fetch = request.session.get('last_fetch', False)
        if last_fetch:
            last_fetch = datetime.strptime(last_fetch, "%Y-%m-%d %H:%M:%S.%f")
            if (now - last_fetch).total_seconds() < 2.0 and \
                request.env.user._is_admin():
                return json.dumps({
                    'status': 300,
                    'message': 'Too many requests'})

        request.session['last_fetch'] = str(now)
        url = "https://stein.efishery.com/v1/storages/5e1edf521073e315924ceab4/list"
        response = requests.get(url)
        if not response.ok:
            return json.dumps({'status': 400})

        result = response.json()
        for line in result:
            price = line.get('price', None)
            line['price_usd'] = None
            if price:
                line['price_usd'] = str(round(int(price) * currency_id.rate, 6))
        return json.dumps(result)

    @http.route('/api/fetch_json', type="json", auth="jwt",
        save_session=False, methods=['GET'])
    def fetch_json(self, **kw):
        CurrencyRate = request.env['res.currency.rate']
        currency_id = request.env.ref('base.USD')
        url = "https://stein.efishery.com/v1/storages/5e1edf521073e315924ceab4/list"
        response = requests.get(url)
        if not response.ok:
            return response.raise_for_status()

        result = response.json()
        for line in result:
            price = line.get('price', None)
            line['price_usd'] = None
            if price:
                line['price_usd'] = str(round(int(price) * currency_id.rate, 6))
        return result
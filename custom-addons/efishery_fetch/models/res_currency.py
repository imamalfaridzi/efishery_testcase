# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
import requests


class Currency(models.Model):
    _inherit = 'res.currency'


    @api.model
    def _cron_update_rates(self):
        CurrencyRate = self.env['res.currency.rate']
        url = "https://api.freecurrencyapi.com/v1/latest"
        params = {
            'apikey': "BB1iBEIf1luz1k8afYOtUbQ62rfQmVG1nfhO4PfU",
            'base_currency': "IDR"
        }
        response_rate = requests.get(url, params)

        if not response_rate.ok:
            return self._cron_api_rates()

        data = response_rate.json().get('data', False)
        if not data:
            return self._cron_api_rates()

        for key, val in data.items():
            currency_id = self.search([
                ('name', '=', key), ('active','in', [True,False])])
            if not currency_id:
                continue

            rate_id = CurrencyRate.search([
                ('currency_id', '=', currency_id.id),
                ('name', '=', datetime.today())])
            if rate_id:
                if rate_id.rate != val:
                    rate_id.rate = val
            else:
                CurrencyRate.create({
                    'currency_id': currency_id.id,
                    'name': datetime.today(),
                    'rate': val
                    })
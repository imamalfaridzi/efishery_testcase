# -*- coding: utf-8 -*-

from . import controllers
from . import models
from odoo import api, modules, SUPERUSER_ID
import base64


def _post_init(cr, registry):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        company_id = env.ref('base.main_company')
        company_id.write({
            'country_id': env.ref('base.id').id,
            'currency_id': env.ref('base.IDR').id,
            })
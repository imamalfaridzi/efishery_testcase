# -*- coding: utf-8 -*-
{
    'name': "Efishery Fetch",

    'summary': """
        Data Processing from Efishery API
    """,

    'description': """
        Features :\n
        - Fetch data from efishery api\n
        - Add Scheduler to update currency rates\n
        - API data processing (add usd price)\n
        - User limitation (1 request / 2 seconds)
        """,

    'author': "Imam Maulana Alfaridzi",
    'website': "https://www.efishery.com",
    'category': 'Customizations',
    'version': '0.1',

    'depends': ['base', 'account', 'efishery_auth'],

    'data': [
        'data/res_currency_data.xml',
    ],
    'post_init_hook': '_post_init',
}

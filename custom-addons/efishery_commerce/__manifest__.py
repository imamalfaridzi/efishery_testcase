# -*- coding: utf-8 -*-
{
    'name': "Efishery Marketplace",

    'summary': """
        Customize sales, invoicing module for Efishery
    """,

    'description': """
        Features :\n
        - Endpoint to create Sales Order\n
        - Automatically create Invoice with paid status\n
        """,

    'author': "Imam Maulana Alfaridzi",
    'website': "https://www.efishery.com",

    'category': 'Customizations',
    'version': '0.1',

    'depends': [
        'base',
        'sale_management',
        'account',
        'efishery_auth'
    ],

}

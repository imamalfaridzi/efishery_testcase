# -*- coding: utf-8 -*-
{
    'name': "Efishery Website",

    'summary': """
        Customize website module for Efishery
    """,

    'description': """
        Features :\n
        - Import users from website\n
        - Background jobs processing\n
        - Website push notification
        """,

    'author': "Imam Maulana Alfaridzi",
    'website': "https://www.efishery.com",
    'category': 'Website',
    'version': '0.1',
    'depends': ['base', 'website'],

    'data': [
        'security/ir.model.access.csv',
        'data/website_import_data.xml',
        'views/templates.xml',
        'views/views.xml',
        'views/website_import_view.xml',
    ]
}

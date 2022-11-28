# -*- coding: utf-8 -*-
{
    'name': "Efishery Authentication",

    'summary': """
        Customize authentication module for Efishery
    """,

    'description': """
        Features :\n
        - Login endpoint with jwt authentication\n
        - Limit login user only 1 tab/browser(device)
        """,

    'author': "Imam Maulana Alfaridzi",
    'website': "https://www.efishery.com",

    'category': 'Customizations',
    'version': '0.1',

    'depends': ['base'],
    "external_dependencies": {'python': ['pyjwt']},
}
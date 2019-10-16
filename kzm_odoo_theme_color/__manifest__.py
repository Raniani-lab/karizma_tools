# -*- coding: utf-8 -*-


{
    'name': "Change menu color",
    'summary': """Change Odoo color""",
    'description': """
    Change color of Odoo 12.0 
    """,
    'author': "Karizma Conseil",
    'website': "www.karizma-conseil.com",

    'depends': ['base',
                'web',
    ],
    'data': [
         'views/change_theme_color.xml'
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
    'demo': [],
}

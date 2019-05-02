# -*- coding: utf-8 -*-
{
    'name': "kzm_backup",

    'summary': """Manage Odoo Instance backup""",

    'description': """
    """,

    'author': "KARIZMA CONSEIL",
    'website': "http://www.karizma.ma",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'mail',
                ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/instance_views.xml',
        'views/backup_views.xml',
        'data/mail.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        
    ],
}
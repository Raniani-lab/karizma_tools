# -*- coding: utf-8 -*-
{
    'name': "Mail mixin management",

    'summary': """
        Managing the groups who can and cannot use the mail mixin options""",

    'description': """
        
    """,

    'author': "Karizma-conseil",
    'website': "http://www.karizma.ma",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'mail', ],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

    ],
    # only loaded in demonstration mode
    'demo': [

    ],
}

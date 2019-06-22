# -*- coding: utf-8 -*-
{
    'name': "KZM Project Activity",

    'summary': """
        Add activity to an project""",

    'description': """
        Long description of module's purpose
    """,

    'author': "KARIZMA Conseil",
    'website': "http://karizma-conseil.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '11.0',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'project',
                ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/project_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
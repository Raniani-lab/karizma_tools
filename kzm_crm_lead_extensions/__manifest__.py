# -*- coding: utf-8 -*-
{
    'name': "CRM Extension",

    'summary': """
        Adding informations in the lead form""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Assabe POLO, KARIZMA Conseil",
    'website': "https://karizma-conseil.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'CRM',
    'version': '12.0',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'crm', ],

    # always loaded
    'qweb': ['static/src/xml/many2many_checkboxes.xml', ],
    'data': [
        # 'security/ir.model.access.csv',
        'views/crm_lead.xml',
    ],
}

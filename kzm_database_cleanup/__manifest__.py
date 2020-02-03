# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "kZM Database Cleanup",
    "version": "0.2.3",
    "author": "Karizma",
    "license": 'AGPL-3',
    "description": """
    """,
    "summary": "",
    "website": "http://www.karizma.ma",
    "category": 'Tools',
    "sequence": 20,
    "depends": [
        'account',
    ],
    "data": [
        "views/res_config_settings_views.xml",
    ],
    "qweb": [
    ],
    "auto_install": False,
    "installable": True,
    "application": False,
}

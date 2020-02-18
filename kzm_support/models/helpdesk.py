# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    contract_state = fields.Selection([
        ('out', 'Out of contract'),
        ('under', 'Under contract')
    ], string='Contract state')


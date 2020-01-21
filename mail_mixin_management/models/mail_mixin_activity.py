# -*- coding: utf-8 -*-


from odoo import api, exceptions, fields, models, _


class MailActivityMixin(models.AbstractModel):
    _inherit = 'mail.activity.mixin'

    activity_ids = fields.One2many(
        'mail.activity', 'res_id', 'Activities',
        auto_join=True,
        groups="mail_mixin_management.activity_managing_consultant", )

# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _


class ProjectProject(models.Model):

    _name = 'project.project'
    _inherit = ['project.project', 'mail.activity.mixin']

    # activity_ids = fields.Many2many('mail.activity.mixin', string="Project activities")


class MailActivity(models.Model):
    _inherit = 'mail.activity'

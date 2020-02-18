# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _


class ProjectProject(models.Model):

    _name = 'project.project'
    _inherit = ['project.project', 'mail.thread', 'mail.activity.mixin']

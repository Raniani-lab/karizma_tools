# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Backup(models.Model):
    _name = 'kzm.backup'
    _order = 'date desc'

    name = fields.Char(string="Name")
    path = fields.Char(string="Path")
    date = fields.Date(string="Date")
    statut = fields.Char(string="Statut")

    instance_id = fields.Many2one("kzm.instance")


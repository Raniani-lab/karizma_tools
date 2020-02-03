# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class Lead(models.Model):
    _inherit = 'crm.lead'
    _description = "Lead/Opportunity"

    denomination = fields.Char(string="Business Name")
    creation_year = fields.Date(string="Creation year", default=fields.date.today())
    legal_status = fields.Selection([
        ('sarl', 'SARL'),
        ('person', 'P. PHYSIQUE'),
        ('asso', 'ASSOC / INSTITUT'),
        ('sa', 'S.A'),
        ('auto', 'AUTO-ENTR'),
        ('adminp', 'ADMIN PUBLIC')])
    effectif = fields.Char(string="Effectif")
    activity_sector = fields.Selection([
        ('agro', 'Agroalimentaire'),
        ('bank', 'Banque / Assurance'),
        ('manuel', 'Bois / Papier / Carton / Imprimerie'),
        ('btp', 'BTP / Matériaux de construction'),
        ('cafe', 'Café / Restaurant'),
        ('chimie', 'Chimie / Parachimie'),
        ('commerce', 'Commerce / Négoce / Distribution'),
        ('edition', 'Édition / Communication / Multimédia'),
        ('etudes', 'Études et conseils'),
        ('indus', 'Industrie pharmaceutique'),
        ('info', 'Informatique / Télécoms'),
        ('machines', 'Machines et équipements / Automobile'),
        ('plas', 'Plastique / Caoutchouc'),
        ('esn', ' Services aux entreprises'),
        ('textile', 'Textile / Habillement / Chaussure')])
    activity = fields.Char(string="Activity")
    rc = fields.Char(string="RC")
    capital = fields.Float(string="Capital (in Dirahms)", digits=(6, 2))
    turnover = fields.Selection([
        ('inf', 'Inférieur à 1MDHS'),
        ('15', 'Entre 1 MDHS et 5 MDHS'),
        ('510', 'Entre 5 MDHS et 10 MDHS'),
        ('1050', 'Entre 10 MDHS et 50 MDHS'),
        ('50100', 'Entre 50 MDHS et 100 MDHS'),
        ('sup', 'Supérieur à 100 MDHS')])
    existing = fields.Char("Existing")
    perimeter = fields.Many2many('ir.module.module', string="Perimeter", domain=[('application', '=', True),
                                                                                 ('author', '=', 'Odoo S.A.')])
    specific_need = fields.Text(string="Specific Need")
    reprisal_data = fields.Selection([
        ('y', 'YES'),
        ('n', 'NO')
    ], default='n')
    method = fields.Char(string="Method")
    nature = fields.Char(string="Nature")
    size = fields.Char(string="Size")
    futur_users = fields.Char(string="Futur users")
    specifications = fields.Binary(string="Upload specifications load")
    specifications_filename = fields.Char(string="Filename")

    @api.onchange('reprisal_data')
    def _clean_reprisal_data(self):
        for r in self:
            r.method = False
            r.nature = False
            r.size = False

# -*- coding: utf-8 -*-
from odoo import http

# class KzmBackup(http.Controller):
#     @http.route('/kzm_backup/kzm_backup/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/kzm_backup/kzm_backup/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('kzm_backup.listing', {
#             'root': '/kzm_backup/kzm_backup',
#             'objects': http.request.env['kzm_backup.kzm_backup'].search([]),
#         })

#     @http.route('/kzm_backup/kzm_backup/objects/<model("kzm_backup.kzm_backup"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('kzm_backup.object', {
#             'object': obj
#         })
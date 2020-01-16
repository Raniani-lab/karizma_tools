# -*- coding: utf-8 -*-
# from odoo import http


# class MailMixinManagement(http.Controller):
#     @http.route('/mail_mixin_management/mail_mixin_management/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mail_mixin_management/mail_mixin_management/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mail_mixin_management.listing', {
#             'root': '/mail_mixin_management/mail_mixin_management',
#             'objects': http.request.env['mail_mixin_management.mail_mixin_management'].search([]),
#         })

#     @http.route('/mail_mixin_management/mail_mixin_management/objects/<model("mail_mixin_management.mail_mixin_management"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mail_mixin_management.object', {
#             'object': obj
#         })

from odoo import api, exceptions, fields, models, _


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    message_ids = fields.One2many(
        'mail.message', 'res_id', string='Messages',
        domain=lambda self: [('message_type', '!=', 'user_notification')], auto_join=True,
        groups="mail_mixin_management.message_managing_consultant,mail_mixin_management.note_managing_consultant")


class MailMessage(models.Model):
    _inherit = 'mail.message'

    type_selection = fields.Selection(
        selection=[
            ('note', 'Note'),
            ('comment', 'Comment'),
            ('other', 'Other'),
        ],
        string='Type_kzm',
        compute="_compute_type_subtype",
        store=True
    )

    @api.depends('subtype_id')
    def _compute_type_subtype(self):
        note_type = self.env.ref('mail.mt_note')
        message_type = self.env.ref('mail.mt_comment')
        for o in self:
            if o.subtype_id:
                if o.subtype_id.id == note_type.id:
                    o.type_selection = 'note'
                elif o.subtype_id.id == message_type.id:
                    o.type_selection = 'comment'
                else:
                    o.type_selection = 'other'

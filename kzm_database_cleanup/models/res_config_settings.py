# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    def cleanup_unreconcile(self):
        # unreconcile
        move_line_ids = self.env['account.move.line'].search([])
        move_line_ids.remove_move_reconcile()

    def cleanup_invoices(self):
        # unreconcile
        self.cleanup_unreconcile()
        self.env.cr.execute(""" DELETE FROM account_move_line;
                                DELETE FROM account_move;""")
        # # cancel incvoices
        # invoice_ids = self.env['account.move'].search([])
        # self.env.context = dict(self.env.context)
        # self.env.context.update({'force_delete': True})
        # invoice_ids.button_cancel()
        # # daft incvoices
        # invoice_ids.button_draft()
        # # invoice_ids.write({'move_name': False})
        # # delete incvoices
        # invoice_ids.unlink()
        journal_sale = self.env['account.journal'].search([('type', '=', 'sale')])
        journal_sale.write({'sequence_number_next': 1, 'refund_sequence_number_next': 1})

        journal_purchase = self.env['account.journal'].search([('type', '=', 'purchase')])
        journal_purchase.write({'sequence_number_next': 1, 'refund_sequence_number_next': 1})

        journal_cash = self.env['account.journal'].search([('type', '=', 'cash')])
        journal_cash.write({'sequence_number_next': 1})

        journal_bank = self.env['account.journal'].search([('type', '=', 'bank')])
        journal_bank.write({'sequence_number_next': 1})

        journal_general = self.env['account.journal'].search([('type', '=', 'general')])
        journal_general.write({'sequence_number_next': 1})

        # seq_ids = self.env['ir.sequence'].search([])
        # seq_ids.write({'number_next_actual': 1})

    def cleanup_payments(self):
        # unreconcile
        self.cleanup_unreconcile()
        # cancel payments
        # payment_ids = self.env['account.payment'].search([])
        # payment_ids.cancel()
        # # daft payments
        # payment_ids.action_draft()
        # payment_ids.write({'move_name': False})
        # # delete payments
        # payment_ids.unlink()
        self.env.cr.execute(""" DELETE FROM account_payment;""")

        seq_ids = self.env['ir.sequence'].search([])
        seq_ids.write({'number_next_actual': 1})

    def cleanup_stock(self):
        self.env.cr.execute("""
                            DELETE FROM stock_inventory;
                            DELETE FROM stock_scrap;
                            DELETE FROM stock_quant;
                            DELETE FROM stock_move_line;
                            DELETE FROM stock_move;
                            DELETE FROM stock_picking;""")
        seq_ids = self.env['ir.sequence'].search([])
        seq_ids.write({'number_next_actual': 1})

    def cleanup_so(self):
        # cleanup invoices
        self.cleanup_invoices()
        # cleanup stock
        self.cleanup_stock()
        sale_order_ids = self.env['sale.order'].search([])
        # cancel SO
        for so in sale_order_ids:
            so.action_cancel()
        # daft SO
        for so in sale_order_ids:
            so.action_draft()
        # delete SO
        for so in sale_order_ids:
            so.unlink()

        seq_ids = self.env['ir.sequence'].search([])

        seq_ids.write({'number_next_actual': 1})

    def cleanup_po(self):
        # cleanup invoices
        self.cleanup_invoices()
        # cleanup stock
        self.cleanup_stock()
        purchase_order_ids = self.env['purchase.order'].search([])
        # cancel PO
        purchase_order_ids.button_cancel()
        # delete PO
        purchase_order_ids.unlink()
        seq_ids = self.env['ir.sequence'].search([])
        seq_ids.write({'number_next_actual': 1})

    def cleanup_so_po(self):
        # cleanup invoices
        self.cleanup_invoices()
        # cleanup stock
        self.cleanup_stock()
        sale_order_ids = self.env['sale.order'].search([])
        # cancel SO
        for so in sale_order_ids:
            so.action_cancel()
        # daft SO
        for so in sale_order_ids:
            so.action_draft()
        # delete SO
        for so in sale_order_ids:
            so.unlink()
        purchase_order_ids = self.env['purchase.order'].search([])
        # cancel PO
        purchase_order_ids.button_cancel()
        # delete PO
        purchase_order_ids.unlink()
        seq_ids = self.env['ir.sequence'].search([])
        seq_ids.write({'number_next_actual': 1})

    def cleanup_all(self):
        # cleanup invoices
        self.cleanup_invoices()
        # cleanup stock
        self.cleanup_stock()
        # cleanup SO PO
        self.cleanup_so_po()
        seq_ids = self.env['ir.sequence'].search([])
        seq_ids.write({'number_next_actual': 1})

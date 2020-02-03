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
        # cancel incvoices
        invoice_ids = self.env['account.invoice'].search([])
        invoice_ids.action_invoice_cancel()
        # daft incvoices
        invoice_ids.action_invoice_draft()
        invoice_ids.write({'move_name': False})
        # delete incvoices
        invoice_ids.unlink()

    def cleanup_payments(self):
        # unreconcile
        self.cleanup_unreconcile()
        # cancel payments
        payment_ids = self.env['account.payment'].search([])
        payment_ids.cancel()
        # daft payments
        payment_ids.action_draft()
        payment_ids.write({'move_name': False})
        # delete payments
        payment_ids.unlink()

    def cleanup_stock(self):
        self.env.cr.execute("""
                            DELETE FROM stock_inventory;
                            DELETE FROM stock_scrap;
                            DELETE FROM stock_quant;
                            DELETE FROM stock_move_line;
                            DELETE FROM stock_move;
                            DELETE FROM stock_picking;""")

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

    def cleanup_all(self):
        # cleanup invoices
        self.cleanup_invoices()
        # cleanup stock
        self.cleanup_stock()
        # cleanup SO PO
        self.cleanup_so_po()
        seq_ids = self.env['ir.sequence'].search([])
        seq_ids.write({'number_next_actual': 1})

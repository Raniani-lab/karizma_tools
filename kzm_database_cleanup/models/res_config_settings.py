# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    @api.multi
    def cleanup_unreconcile(self):
        # unreconcile
        move_line_ids = self.env['account.move.line'].search([])
        move_line_ids.remove_move_reconcile()

    @api.multi
    def cleanup_ivoices(self):
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

    @api.multi
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

    @api.multi
    def cleanup_stock(self):
        self.env.cr.execute("""
                            DELETE FROM stock_inventory;
                            DELETE FROM stock_scrap;
                            DELETE FROM stock_quant;
                            DELETE FROM stock_move_line;
                            DELETE FROM stock_move;
                            DELETE FROM stock_picking;""")

    @api.multi
    def cleanup_so_po(self):
        # cleanup ivoices
        self.cleanup_ivoices()
        # cleanup stock
        self.cleanup_stock()
        sale_order_ids = self.env['sale.order'].search([])
        # cancel SO
        sale_order_ids.action_cancel()
        # daft SO
        sale_order_ids.action_draft()
        # delete SO
        sale_order_ids.unlink()
        purchase_order_ids = self.env['purchase.order'].search([])
        # cancel PO
        purchase_order_ids.button_cancel()
        # delete PO
        purchase_order_ids.unlink()

    @api.multi
    def cleanup_all(self):
        # cleanup ivoices
        self.cleanup_ivoices()
        # cleanup stock
        self.cleanup_stock()
        # cleanup SO PO
        self.cleanup_so_po()
        seq_ids = self.env['ir.sequence'].search([])
        seq_ids.write({'number_next_actual': 1})

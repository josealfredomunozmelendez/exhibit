# coding: utf-8
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def action_invoice_open(self):
        """Inherit method for add custom information in invoice's line"""
        self.filtered(
            lambda r:
            r.l10n_mx_edi_is_required()).generate_customs_information()
        return super(AccountInvoice, self).action_invoice_open()

    @api.multi
    def generate_customs_information(self):
        """Search custom information in move type out"""
        landed_obj = self.env['stock.landed.cost']
        for line in self.filtered(
                lambda r:
                r.l10n_mx_edi_get_pac_version() == '3.3').mapped(
                    'invoice_line_ids').filtered('sale_line_ids'):
            moves = line.mapped('sale_line_ids.move_ids').filtered(
                lambda r: r.state == 'done' and not r.scrapped)
            if not moves:
                continue
            landed = landed_obj.search(
                [('picking_ids', 'in',
                    moves.mapped('move_orig_fifo_ids.picking_id').ids),
                    ('l10n_mx_edi_customs_number', '!=', False)])
            line.l10n_mx_edi_customs_number = ','.join(
                list(set(landed.mapped('l10n_mx_edi_customs_number'))))

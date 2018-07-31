# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import _, api, models


class HrExpenseSheet(models.Model):
    _inherit = "hr.expense.sheet"

    @api.multi
    def approve_expense_sheets(self):
        """Extend the method, to validate if the expense has a XML attached.
        - If has a XML, try to generate a supplier invoice.
        - If the invoice could not be created, the expense is refused
        - Only apply when the payment mode in the expense is to company"""
        res = super(HrExpenseSheet, self).approve_expense_sheets()
        wizard = self.env['attach.xmls.wizard']
        invoice_obj = self.env['account.invoice']
        invoice = invoice_obj.search([
            ('expense_id', 'in', self.expense_line_ids.ids)])
        invoice.l10n_mx_edi_expense_autopaid()
        for expense in self.expense_line_ids:
            domain = expense.action_get_attachment_view().get('domain', [])
            domain.append(('name', '=ilike', '%.xml'))
            attachment = self.env['ir.attachment'].search(domain)
            for xml in attachment:
                datas = xml._file_read(xml.store_fname)
                validation = wizard.with_context({}).check_xml(
                    datas, xml.name, expense.account_id.id)
                if 'supplier' in validation.keys():
                    wizard.with_context({}).create_partner(datas, xml.name)
                    validation = wizard.with_context({}).check_xml(
                        datas, xml.name, expense.account_id.id)
                if 'invoice_id' in validation.keys():
                    invoice = invoice_obj.browse(validation['invoice_id'])
                    invoice.invoice_line_ids.filtered(
                        lambda l: not l.product_id).write({
                            'product_id': expense.product_id.id,
                        })
                    invoice.expense_id = expense
                    self.message_post(_('Invoice to the expense %s created '
                                        'correctly' % expense.name))
                    invoice.l10n_mx_edi_expense_autopaid()
                    continue
                self.refuse_by_error(expense, validation)
        return res

    def refuse_by_error(self, expense, validation):
        self.ensure_one()
        wizard_refuse = self.env['hr.expense.refuse.wizard']
        keys = validation.keys()
        errors = {
            'rfc': _(
                "The Receptor's RFC in the XML does not match with your "
                "Company's RFC"),
            'uuid_duplicate': _('The XML UUID belongs to other invoice.'),
            'reference': _('The invoice reference belongs to other invoice of '
                           'the same partner.'),
            'currency': _('The currency in the XML was not found or is '
                          'disabled'),
            'error': validation.get('error', '')
        }
        ctx = {
            'active_ids': expense.ids,
            'hr_expense_refuse_model': 'hr.expense'}
        for key in keys:
            if key in errors:
                message = errors[key]
                wizard_refuse.with_context(ctx).create({
                    'reason': _(
                        'Error when try to generate the invoice for the '
                        'expense "%s": %s') % (expense.name, message)
                }).expense_refuse_reason()
                return True
        wizard_refuse.with_context(ctx).create({
            'reason': _('The invoice could not be generated to the expense '
                        '"%s", please verify the XML structure') % (
                            expense.name)}).expense_refuse_reason()

    @api.multi
    def action_open_invoices(self):
        return {
            'name': _('Invoices'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.invoice',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('expense_id', 'in', self.expense_line_ids.ids)],
        }


class HrExpense(models.Model):
    _inherit = 'hr.expense'

    @api.multi
    def action_open_invoices(self):
        self.ensure_one()
        return {
            'name': _('Invoices'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.invoice',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('expense_id', 'in', self.ids)],
            'context': {
                'default_expense_id': self.id,
                'default_type': 'in_invoice',
            }
        }

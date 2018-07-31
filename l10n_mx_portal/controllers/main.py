# coding: utf-8
# Copyright 2016 Vauxoo (https://www.vauxoo.com) <info@vauxoo.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo.http import Controller, request, route


class SendInvoiceAndXML(Controller):

    @route(
        ['/send_invoice_mail/<int:invoice_id>', ],
        type='http', auth='user', website=True)
    def send_invoice_and_xml(self, invoice_id=None, **data):
        invoice_obj = request.env['account.invoice']
        invoice = invoice_obj.browse(invoice_id)
        invoice.sudo().send_invoice_mail()
        values = {
            'company': request.website.company_id,
            'user': request.env.user,
            'invoice': invoice,
        }
        return request.render('l10n_mx_portal.email_sent', values)

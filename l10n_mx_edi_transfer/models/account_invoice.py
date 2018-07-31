from odoo import api, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def _l10n_mx_edi_create_cfdi_values(self):
        values = super()._l10n_mx_edi_create_cfdi_values()
        if self.company_id.partner_id.commercial_partner_id != self.partner_id.commercial_partner_id:  # noqa
            return values
        values['document_type'] = 'T'
        values['payment_policy'] = None
        values['taxes']['transferred'] = None
        values['taxes']['withholding'] = None
        return values

# -*- coding: utf-8 -*-

from odoo import models, api, _
from odoo.tools.misc import format_date

class report_account_aged_payable(models.AbstractModel):
    _inherit = "account.aged.partner"

    def get_columns_name(self, options):
        columns = super(report_account_aged_payable, self).get_columns_name(options)
        columns += [{'name': _('Moneda'), 'class': 'number'}]
        return columns
        
    @api.model
    def get_lines(self, options, line_id = None):
        lines = super(report_account_aged_payable, self).get_lines(options, line_id)
        
        i = 0;
        for value in lines:
            currency = ''
            try:
                if lines[i]['level'] == 4:
                    aml = self.env['account.move.line'].search([('id', '=', lines[i]['id'])])
                    if aml.currency_id.id is False:
                        currency = self.env.ref('base.main_company').currency_id.display_name
                    else:
                        currency = aml.currency_id.display_name
            except:
                pass
            lines[i]['columns'] += [{'name': currency}]
            i += 1
        return lines

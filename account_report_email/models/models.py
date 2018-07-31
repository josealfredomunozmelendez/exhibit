# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.tools import append_content_to_html, DEFAULT_SERVER_DATE_FORMAT

class LlacoxAccountReportEmail(models.AbstractModel):
    _inherit = "account.followup.report"
    
    @api.model
    def send_email(self, options):
        
        partner = self.env['res.partner'].browse(options.get('partner_id'))
        email = self.env['res.partner'].browse(partner.address_get(['invoice'])['invoice']).email
        domain = [('partner_id', '=', options.get('partner_id'))]
        report_manager = self.env['account.report.manager'].search(domain, limit=1)

        if email and email.strip():
            subject =  report_manager.subject
            if not subject:
                subject = _('%s Payment Reminder') % (self.env.user.company_id.name) + ' - ' + partner.name,
            
            body_html = self.with_context(print_mode=True, mail=True, keep_summary=True).get_html(options)
            msg = self.get_post_message(options)
            msg += '<br>' + body_html.decode('utf-8')
            msg_id = partner.message_post(body=msg, subtype='account_reports.followup_logged_action')
            email = self.env['mail.mail'].with_context(default_mail_message_id=msg_id).create({
                'subject': subject,
                'body_html': append_content_to_html(body_html, self.env.user.signature or '', plaintext=False),
                'email_from': self.env.user.email or '',
                'email_to': email,
                'body': msg,
            })
            
            return True
        raise UserError(_('Could not send mail to partner because it does not have any email address defined'))
        
class LlacoxAccountReportEmailManager(models.AbstractModel):
    _inherit = "account.report.manager"
    
    subject = fields.Char(string="Subject")
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from datetime import timedelta

class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    assembly_date    = fields.Datetime(string = "Fecha de montaje", required = True)
    disassembly_date = fields.Datetime(string = "Fecha de desmontaje", required = True)
    
    @api.one
    def action_confirm(self):
        super(SaleOrder, self).action_confirm()
        self.env['calendar.event'].create({
            'name': 'Evento {}'.format(self.partner_id.name),
            'start': self.assembly_date,
            'stop': self.disassembly_date,
        })
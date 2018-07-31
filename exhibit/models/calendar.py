# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from datetime import timedelta

class Meeting(models.Model):
    _inherit = 'calendar.event'
    
    render_ids = fields.Many2many(comodel_name='ir.attachment', string = "Render")
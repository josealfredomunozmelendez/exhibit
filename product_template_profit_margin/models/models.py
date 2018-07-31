# -*- coding: utf-8 -*-

from odoo import models, fields, api


class LlacoxProductTemplate(models.Model):
    _name       = "product.template"
    _inherit    = "product.template"
    
    profit_percentage = fields.Float(digits=(6,2))
    
    @api.onchange('profit_percentage')
    def _value_pc(self):
        self.list_price = self.standard_price + (self.standard_price* (self.profit_percentage / 100))
    
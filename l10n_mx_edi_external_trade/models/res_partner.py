# coding: utf-8

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    l10n_mx_edi_external_trade = fields.Boolean(
        'Need external trade?', help='If this field is active, in the CFDIs '
        'that was generated to this partner will be added the complement '
        '"External Trade".')
    l10n_mx_edi_colony_code = fields.Char(
        string='Colony Code',
        help='Optional attribute used in the XML that serves to define the '
        'colony where the location is given and used external '
        'trade complement')
    l10n_mx_edi_locality_id = fields.Many2one(
        'l10n_mx_edi.res.locality', string='Locality',
        help='Optional attribute used in the XML that serves to define the '
        'locality where the location is given')
    l10n_mx_edi_curp = fields.Char(
        'CURP', size=18, help='Attribute to set in XML to express the CURP '
        'when the partner is from a natural person.')

    @api.onchange('l10n_mx_edi_locality_id')
    def _onchange_l10n_mx_edi_locality_id(self):
        self.l10n_mx_edi_locality = self.l10n_mx_edi_locality_id.name

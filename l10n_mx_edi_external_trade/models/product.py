# coding: utf-8

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    l10n_mx_edi_tariff_fraction = fields.Char(
        string='Tariff Fraction', help='It is used to express the key of '
        'the tariff fraction corresponding to the description of the '
        'product exported. Node "FraccionArancelaria" to concept.')
    l10n_mx_edi_umt_aduana = fields.Many2one(
        'product.uom', 'UMT Aduana', help='Used in complement '
        '"Comercio Exterior" to indicate in the products the '
        'TIGIE Units of Measurement, this based in the SAT catalog.')


class ProductUoM(models.Model):
    _inherit = 'product.uom'

    l10n_mx_edi_code_aduana = fields.Char(
        'Code Aduana', help='Used in the complement of "Comercio Exterior" to '
        'indicate in the products the UoM, this based in the SAT catalog.')

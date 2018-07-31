# -*- coding: utf-8 -*-

import odoo.addons.decimal_precision as dp
from odoo import _, api, fields, models
from odoo.addons.l10n_mx_edi.models.account_invoice import create_list_html


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    l10n_mx_edi_incoterm = fields.Selection(
        [('CIP', 'CARRIAGE AND INSURANCE PAID TO'),
         ('CPT', 'CARRIAGE PAID TO'),
         ('CFR', 'COST AND FREIGHT'),
         ('CIF', 'COST, INSURANCE AND FREIGHT'),
         ('DAF', 'DELIVERED AT FRONTIER'),
         ('DAP', 'DELIVERED AT PLACE'),
         ('DAT', 'DELIVERED AT TERMINAL'),
         ('DDP', 'DELIVERED DUTY PAID'),
         ('DDU', 'DELIVERED DUTY UNPAID'),
         ('DEQ', 'DELIVERED EX QUAY'),
         ('DES', 'DELIVERED EX SHIP'),
         ('EXW', 'EX WORKS'),
         ('FAS', 'FREE ALONGSIDE SHIP'),
         ('FCA', 'FREE CARRIER'),
         ('FOB', 'FREE ON BOARD')],
        string='Incoterm', help='Indicates the INCOTERM applicable to the '
        'external trade customer invoice.')
    l10n_mx_edi_cer_source = fields.Boolean(
        'Is Certificate Source?',
        help='Used in CFDI like attribute derived from the exception of '
        'certificates of Origin of the Free Trade Agreements that Mexico '
        'has celebrated with several countries. Inactive = No Funge as '
        'certificate of origin or active = Funge as certificate of origin.'
        ' CFDI node "CertificadoOrigen"')
    l10n_mx_edi_num_cer_source = fields.Char(
        'Number of Certificate Source',
        help='Used in CFDI to express the folio of the certificate of origin '
        'or the fiscal leaf of the CFDI with which the issuance of the '
        'certificate of origin was paid. CFDI node "NumCertificadoOrigen".')

    @api.multi
    def _l10n_mx_edi_create_cfdi(self):

        if (not self.partner_id.l10n_mx_edi_external_trade or
                self.l10n_mx_edi_get_pac_version() == '3.2'):
            return super(AccountInvoice, self)._l10n_mx_edi_create_cfdi()

        # Call the onchange to obtain the values of l10n_mx_edi_qty_umt
        # and l10n_mx_edi_price_unit_umt, this is necessary when the
        # invoice is created from the sales order or from the picking
        self.invoice_line_ids.onchange_quantity()
        self.invoice_line_ids._set_price_unit_umt()

        bad_line = self.invoice_line_ids.filtered(
            lambda l: not l.l10n_mx_edi_qty_umt or not l.product_id.
            l10n_mx_edi_umt_aduana or not l.l10n_mx_edi_tariff_fraction)
        if bad_line:
            line_name = bad_line.mapped('product_id.name')
            return {'error': _(
                'Please verify that Qty UMT has a value in the line, '
                'and that the product has set a value in Tariff Fraction and '
                'in UMT Aduana.<br/><br/>This for the products:'
            ) + create_list_html(line_name)}
        return super(AccountInvoice, self)._l10n_mx_edi_create_cfdi()

    @api.multi
    def _l10n_mx_edi_create_cfdi_values(self):
        """Create the values to fill the CFDI template with external trade.
        """
        values = super(AccountInvoice, self)._l10n_mx_edi_create_cfdi_values()
        if (not self.partner_id.l10n_mx_edi_external_trade or
                self.l10n_mx_edi_get_pac_version() == '3.2'):
            return values

        ctx = dict(company_id=self.company_id.id, date=self.date_invoice)
        customer = values['customer']
        values.update({
            'usd': self.env.ref('base.USD').with_context(ctx),
            'mxn': self.env.ref('base.MXN').with_context(ctx),
            'europe_group': self.env.ref('base.europe'),
            'receiver_reg_trib': customer.vat,
        })
        values['quantity_aduana'] = lambda p, i: sum([
            l.l10n_mx_edi_qty_umt for l in i.invoice_line_ids
            if l.product_id == p])
        values['unit_value_usd'] = lambda l, c, u: c.compute(
            l.l10n_mx_edi_price_unit_umt, u)
        values['amount_usd'] = lambda o, d, a: o.compute(a, d)
        values['total_usd'] = lambda i, u, c: sum([
            round(l.l10n_mx_edi_qty_umt * c.compute(
                l.l10n_mx_edi_price_unit_umt, u), 2) for l in i])

        return values

    @api.model
    def l10n_mx_edi_get_et_etree(self, cfdi):
        """Get the ComercioExterior node from the cfdi.
        :param cfdi: The cfdi as etree
        :type cfdi: etree
        :return: the ComercioExterior node
        :rtype: etree
        """
        if not hasattr(cfdi, 'Complemento'):
            return None
        attribute = 'cce11:ComercioExterior[1]'
        namespace = {'cce11': 'http://www.sat.gob.mx/ComercioExterior11'}
        node = cfdi.Complemento.xpath(attribute, namespaces=namespace)
        return node[0] if node else None


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    l10n_mx_edi_tariff_fraction = fields.Char(
        'Tariff Fraction', related='product_id.l10n_mx_edi_tariff_fraction',
        help='It is used to express the key of the tariff fraction '
        'corresponding to the description of the product to export. Node '
        '"FraccionArancelaria" to the concept.')
    l10n_mx_edi_qty_umt = fields.Float(
        'Qty UMT', help='Quantity expressed in the UMT from product. Is '
        'used in the attribute "CantidadAduana" in the CFDI',
        digits=dp.get_precision('Product Unit of Measure'))
    l10n_mx_edi_price_unit_umt = fields.Float(
        'Unit Value UMT', help='Unit value expressed in the UMT from product. '
        'Is used in the attribute "ValorUnitarioAduana" in the CFDI')

    @api.multi
    def _set_price_unit_umt(self):
        for res in self.filtered('partner_id.l10n_mx_edi_external_trade'):
            res.l10n_mx_edi_price_unit_umt = round(
                res.quantity * res.price_unit / res.l10n_mx_edi_qty_umt
                if res.l10n_mx_edi_qty_umt else
                res.l10n_mx_edi_price_unit_umt, 2)
            res.l10n_mx_edi_qty_umt = round(
                res.quantity * res.price_unit/res.l10n_mx_edi_price_unit_umt
                if res.l10n_mx_edi_price_unit_umt else
                res.l10n_mx_edi_qty_umt, 3)

    @api.onchange('quantity', 'product_id')
    @api.multi
    def onchange_quantity(self):
        """When change the quantity by line, update the QTY in the UMT"""
        for res in self.filtered(
            lambda l: l.partner_id.l10n_mx_edi_external_trade and
                l.product_id):
            pdt_aduana = res.product_id.mapped(
                'l10n_mx_edi_umt_aduana.l10n_mx_edi_code_aduana')
            if pdt_aduana == res.uom_id.mapped('l10n_mx_edi_code_aduana'):
                res.l10n_mx_edi_qty_umt = res.quantity
            elif '01' in pdt_aduana:
                res.l10n_mx_edi_qty_umt = round(
                    res.product_id.weight * res.quantity, 3)

# coding: utf-8
import base64
import os

from lxml import objectify

from odoo.addons.l10n_mx_edi.tests.common import InvoiceTransactionCase
from odoo.tools import misc


class TestL10nMxEdiExternalTrade(InvoiceTransactionCase):
    def setUp(self):
        super(TestL10nMxEdiExternalTrade, self).setUp()
        isr_tag = self.env['account.account.tag'].search(
            [('name', '=', 'ISR')])
        self.tax_negative.tag_ids |= isr_tag
        unit = self.env.ref('product.product_uom_unit')
        self.product.write({
            'l10n_mx_edi_umt_aduana': unit.id,
            'l10n_mx_edi_tariff_fraction': '84289099',
        })
        self.namespaces = {
            'cfdi': 'http://www.sat.gob.mx/cfd/3',
            'cce11': 'http://www.sat.gob.mx/ComercioExterior11',
        }
        self.set_currency_rates(mxn_rate=1, usd_rate=1)

    def create_invoice(self, inv_type='out_invoice', currency_id=None):
        res = super(TestL10nMxEdiExternalTrade, self).create_invoice()
        res.l10n_mx_edi_incoterm = 'FCA'
        return res

    def test_l10n_mx_edi_invoice_external_trade(self):
        self.xml_expected_str = misc.file_open(os.path.join(
            'l10n_mx_edi_external_trade', 'tests',
            'expected_cfdi_external_trade_33.xml')).read().encode('UTF-8')
        self.xml_expected = objectify.fromstring(self.xml_expected_str)

        self.company.partner_id.write({
            'property_account_position_id': self.fiscal_position.id,
            'l10n_mx_edi_locality_id': self.env.ref(
                'l10n_mx_edi.res_locality_mx_jal_03').id,
            'city_id': self.env.ref('l10n_mx_edi.res_city_mx_jal_039').id,
            'state_id': self.env.ref('base.state_mx_jal').id,
            'l10n_mx_edi_colony_code': '0002',
            'zip': '44009',
        })
        self.partner_agrolait.commercial_partner_id.write({
            'country_id': self.env.ref('base.us').id,
            'state_id': self.env.ref('base.state_us_23').id,
        })
        self.partner_agrolait.write({
            'country_id': self.env.ref('base.us').id,
            'state_id': self.env.ref('base.state_us_23').id,
            'l10n_mx_edi_external_trade': True,
            'zip': 39301,
            'vat': '123456789',
        })

        self.company._load_xsd_attachments()

        # -----------------------
        # Testing sign process with External Trade
        # -----------------------

        invoice = self.create_invoice()
        invoice.action_invoice_open()
        self.assertEqual(invoice.l10n_mx_edi_pac_status, "signed",
                         invoice.message_ids.mapped('body'))
        xml = objectify.fromstring(base64.b64decode(invoice.l10n_mx_edi_cfdi))
        self.assertTrue(xml.Complemento.xpath(
            'cce11:ComercioExterior', namespaces=self.namespaces),
            "The node '<cce11:ComercioExterior> should be present")
        xml_cce = xml.Complemento.xpath(
            'cce11:ComercioExterior', namespaces=self.namespaces)[0]
        xml_cce_expected = self.xml_expected.Complemento.xpath(
            'cce11:ComercioExterior', namespaces=self.namespaces)[0]
        self.assertEqualXML(xml_cce, xml_cce_expected)

        # -------------------------
        # Testing case UMT Aduana, l10n_mx_edi_code_duana == 1
        # -------------------------
        kg = self.env.ref('product.product_uom_kgm')
        kg.l10n_mx_edi_code_aduana = '01'
        self.product.write({
            'weight': 2,
            'l10n_mx_edi_umt_aduana': kg.id,
            'l10n_mx_edi_tariff_fraction': '72123099',
        })
        invoice = self.create_invoice()
        invoice.action_invoice_open()
        line = invoice.invoice_line_ids
        self.assertEqual(line.l10n_mx_edi_qty_umt,
                         line.product_id.weight * line.quantity,
                         'Qty UMT != weight * quantity')
        self.assertEqual(invoice.l10n_mx_edi_pac_status, "signed",
                         invoice.message_ids.mapped('body'))

        # ------------------------
        # Testing case UMT Aduana, UMT Custom != Kg and UMT Custom != uos_id
        # ------------------------
        kg.l10n_mx_edi_code_aduana = '08'
        self.product.write({
            'l10n_mx_edi_tariff_fraction': '27101299',
        })
        invoice = self.create_invoice()
        # Manually add the value Qty UMT
        line = invoice.invoice_line_ids
        self.assertEqual(line.l10n_mx_edi_qty_umt, 0,
                         'Qty umt must be manually assigned')
        invoice.invoice_line_ids.l10n_mx_edi_qty_umt = 2
        invoice.action_invoice_open()
        self.assertEqual(invoice.l10n_mx_edi_pac_status, "signed",
                         invoice.message_ids.mapped('body'))

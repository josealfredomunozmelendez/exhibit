# coding: utf-8
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64
import os
import unittest
from datetime import datetime, timedelta

from lxml import etree, objectify

import odoo
from odoo.tests.common import TransactionCase


class HRPayroll(TransactionCase):

    def setUp(self):
        super(HRPayroll, self).setUp()
        self.payslip_obj = self.env['hr.payslip']
        self.mail_obj = self.env['mail.compose.message']
        self.payslip_run_obj = self.env['hr.payslip.run']
        self.wizard_batch = self.env['hr.payslip.employees']

        self.employee = self.env.ref('hr.employee_qdp')
        self.contract = self.env.ref('hr_payroll.hr_contract_gilles_gravie')
        self.struct = self.env.ref(
            'l10n_mx_edi_payslip.payroll_structure_data_01')
        self.cat_excempt = self.env.ref(
            'l10n_mx_edi_payslip.hr_salary_rule_category_perception_mx_exempt')

        xml_expected_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), 'expected_cfdi.xml')
        xml_expected_f = open(xml_expected_path)
        self.xml_expected = objectify.parse(xml_expected_f).getroot()
        self.fiscal_position_model = self.env['account.fiscal.position']
        self.fiscal_position = self.fiscal_position_model.create({
            'name': 'Personas morales del régimen general',
            'l10n_mx_edi_code': '601',
        })
        self.partnerc = self.env.user.company_id.partner_id
        self.partnerc.property_account_position_id = self.fiscal_position
        self.env.user.company_id.l10n_mx_edi_minimum_wage = 80.04
        self.uid = self.env.ref('l10n_mx_edi_payslip.payroll_mx_manager')

    def test_001_xml_structure(self):
        """Use XML expected to verify that is equal to generated. And SAT
        status"""
        payroll = self.create_payroll()
        payroll.action_payslip_done()
        self.assertEquals(payroll.l10n_mx_edi_pac_status, 'signed',
                          payroll.message_ids.mapped('body'))
        payroll.l10n_mx_edi_update_sat_status()
        self.assertEquals(payroll.l10n_mx_edi_sat_status, 'not_found')
        xml = payroll.l10n_mx_edi_get_xml_etree()
        self.xml_expected.attrib['Fecha'] = xml.attrib['Fecha']
        self.xml_expected.attrib['Folio'] = xml.attrib['Folio']
        self.xml_expected.attrib['Sello'] = xml.attrib['Sello']
        node_payroll = payroll.l10n_mx_edi_get_payroll_etree(xml)
        node_expected = payroll.l10n_mx_edi_get_payroll_etree(
            self.xml_expected)
        self.assertTrue(node_payroll, 'Complement to payroll not added.')
        node_expected.Receptor.attrib['FechaInicioRelLaboral'] = node_payroll.Receptor.attrib['FechaInicioRelLaboral']  # noqa
        node_expected.attrib['FechaFinalPago'] = node_payroll.attrib['FechaFinalPago']  # noqa
        node_expected.attrib['FechaInicialPago'] = node_payroll.attrib['FechaInicialPago']  # noqa
        node_expected.attrib['FechaPago'] = node_payroll.attrib['FechaPago']
        node_expected.Receptor.attrib[u'Antig\xfcedad'] = node_payroll.Receptor.attrib[u'Antig\xfcedad']  # noqa

        # Replace node TimbreFiscalDigital
        tfd_expected = self.payslip_obj.l10n_mx_edi_get_tfd_etree(
            self.xml_expected)
        tfd_xml = objectify.fromstring(etree.tostring(
            self.payslip_obj.l10n_mx_edi_get_tfd_etree(xml)))
        self.xml_expected.Complemento.replace(tfd_expected, tfd_xml)
        # When the year is a leap year the values will change by a few
        # decimals
        year = float(payroll.l10n_mx_edi_payment_date.split('-')[0])
        if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
            self.xml_expected.attrib['Descuento'] = '4293.67'
            self.xml_expected.attrib['Total'] = '7506.33'
            self.xml_expected.Conceptos.Concepto.attrib[
                'Descuento'] = '4293.67'
            node_expected.attrib['TotalDeducciones'] = '4293.67'
            node_expected.Receptor.attrib['SalarioDiarioIntegrado'] = '766.39'
            node_expected.Deducciones.attrib[
                'TotalOtrasDeducciones'] = '2404.60'
            node_expected.Deducciones.Deduccion[0].attrib['Importe'] = '304.60'
        self.assertEqualXML(xml, self.xml_expected)

    def test_002_perception_022(self):
        """When perception code have 022, the payroll have node
        SeparacionIndemnizacion."""
        payroll = self.create_payroll()
        payroll.write({
            'input_line_ids': [(0, 0, {
                'code': 'pe_022',
                'name': u'Prima por antigüedad',
                'amount': 1000.0,
                'contract_id': self.contract.id,
            })],
            'l10n_mx_edi_extra_node_ids': [(0, 0, {
                'node': 'separation',
                'amount_total': 1000.0,
                'service_years': 5.0,
                'last_salary': 1000.0,
                'accumulable_income': 900.0,
                'non_accumulable_income': 100.0,
            })],
        })
        payroll.action_payslip_done()
        self.assertEquals(payroll.l10n_mx_edi_pac_status, 'signed',
                          payroll.message_ids.mapped('body'))
        # Cancel a payroll
        payroll.action_payslip_cancel()
        self.assertEqual(payroll.l10n_mx_edi_pac_status, 'cancelled',
                         "Payroll could not be cancelled")

    def test_003_perception_039(self):
        """When perception code have 039, the payroll have node
        JubilacionPensionRetiro."""
        payroll = self.create_payroll()
        payroll.write({
            'input_line_ids': [(0, 0, {
                'code': 'pe_039',
                'name': u'Jubilaciones, pensiones o haberes de retiro',
                'amount': 1000.0,
                'contract_id': self.contract.id,
            })],
            'l10n_mx_edi_extra_node_ids': [(0, 0, {
                'node': 'retirement',
                'amount_total': 1000.0,
                'accumulable_income': 900.0,
                'non_accumulable_income': 100.0,
            })],
        })
        payroll.action_payslip_done()
        self.assertEquals(payroll.l10n_mx_edi_pac_status, 'signed',
                          payroll.message_ids.mapped('body'))

    def test_004_other_payment_002(self):
        """When other payment have the code 002, this must have node
        SubsidioAlEmpleo."""
        payroll = self.create_payroll()
        # Contract with a low salary that requires subsidy
        self.contract.wage = 5000
        payroll.action_payslip_done()
        self.assertEquals(payroll.l10n_mx_edi_pac_status, 'signed',
                          payroll.message_ids.mapped('body'))

    def test_005_other_payment_004(self):
        """When other payment have the code 004, this must have node
        CompensacionSaldosAFavor."""
        payroll = self.create_payroll()
        payroll.write({
            'input_line_ids': [(0, 0, {
                'code': 'op_004',
                'name': u'Aplicación de saldo a favor por compensación anual.',
                'amount': 500.0,
                'contract_id': self.contract.id,
            })],
            'l10n_mx_edi_balance_favor': 500.0,
            'l10n_mx_edi_comp_year': 2016,
            'l10n_mx_edi_remaining': 500.0,
        })
        payroll.action_payslip_done()
        self.assertEquals(payroll.l10n_mx_edi_pac_status, 'signed',
                          payroll.message_ids.mapped('body'))

    def test_006_perception_045(self):
        """When one perception have the code 045, this must have node
        AccionesOTitulos,."""
        payroll = self.create_payroll()
        payroll.write({
            'input_line_ids': [(0, 0, {
                'code': 'pe_045',
                'name': u'Ingresos en acciones o títulos valor que representan bienes',  # noqa
                'amount': 500.0,
                'contract_id': self.contract.id,
            })],
            'l10n_mx_edi_action_title_ids': [(0, 0, {
                'category_id': self.cat_excempt.id,
                'market_value': 100.0,
                'price_granted': 100.0,
            })]
        })
        payroll.action_payslip_done()
        self.assertEquals(payroll.l10n_mx_edi_pac_status, 'signed',
                          payroll.message_ids.mapped('body'))

    @unittest.skip('Check PDF Format')
    def test_007_print_pdf(self):
        """Verify that PDF is generated"""
        # TODO: check this test
        payroll = self.create_payroll()
        payroll.action_payslip_done()
        self.assertEquals(payroll.l10n_mx_edi_pac_status, 'signed',
                          payroll.message_ids.mapped('body'))
        report = odoo.report.render_report(
            self.cr, self.uid, payroll.ids, 'hr_payroll.report_payslip',
            {'model': 'hr.payslip'}, context=self.env.context)
        self.assertTrue(report, 'Report not generated.')

    def test_008_cancel_xml(self):
        """Verify that XML is cancelled"""
        payroll = self.create_payroll()
        payroll.action_payslip_cancel()
        payroll.action_payslip_draft()
        payroll.action_payslip_done()
        self.assertEquals(payroll.l10n_mx_edi_pac_status, 'signed',
                          payroll.message_ids.mapped('body'))
        payroll.action_payslip_cancel()
        self.assertEquals(payroll.l10n_mx_edi_pac_status, 'cancelled',
                          payroll.message_ids.mapped('body'))

    @unittest.skip('Check PDF Format')
    def test_009_send_payroll_mail(self):
        """Verify that XML is attach on wizard that send mail"""
        # TODO: check this test
        payroll = self.create_payroll()
        payroll.action_payslip_done()
        mail_data = payroll.action_payroll_sent()
        template = mail_data.get('context', {}).get('default_template_id', [])
        template = self.env['mail.template'].browse(template)
        mail = template.generate_email(payroll.ids)
        self.assertEquals(len(mail[payroll.id].get('attachments')), 2,
                          'Documents not attached')

    def test_010_batches(self):
        """Verify payroll information from batches"""
        date = (datetime.today() + timedelta(days=5)).strftime('%Y-%m-%d')
        payslip_run = self.payslip_run_obj.create({
            'name': 'Payslip VX',
            'l10n_mx_edi_payment_date': date,
        })
        self.wizard_batch.create({
            'employee_ids': [(6, 0, self.employee.ids)]
        }).with_context(active_id=payslip_run.id).compute_sheet()
        self.assertEquals(payslip_run.slip_ids.l10n_mx_edi_payment_date, date,
                          'Payment date not assigned in the payroll created.')

    def test_011_aguinaldo(self):
        """When in payslip has a perception of Christmas bonuses (Aguinaldo)"""
        self.struct = self.env.ref(
            'l10n_mx_edi_payslip.payroll_structure_data_02')
        payroll = self.create_payroll()
        date = datetime.strptime(payroll.l10n_mx_edi_payment_date,
                                 '%Y-%m-%d').date() - timedelta(days=380)
        self.contract.write({
            'date_start': date,
        })
        payroll.action_payslip_done()
        self.assertEquals(payroll.l10n_mx_edi_pac_status, 'signed',
                          payroll.message_ids.mapped('body'))
        xml = payroll.l10n_mx_edi_get_xml_etree()
        node_payroll = payroll.l10n_mx_edi_get_payroll_etree(xml)
        self.assertEquals(
            '11000.00', node_payroll.get('TotalPercepciones', ''))

    def test_012_onchange_employee(self):
        """check if the company_id is set with onchange_employee"""
        company2 = self.env['res.company'].create({'name': 'Company2'})
        company3 = self.env['res.company'].create({'name': 'Company3'})
        self.employee.company_id = company2
        self.contract.company_id = company3
        payroll = self.create_payroll()
        payroll.onchange_employee()
        # payroll company is the same that employee
        self.assertEquals(payroll.company_id, company2,
                          'Company is not the employee company')
        self.employee.company_id = False
        payroll.onchange_employee()
        # payroll company is the same that contract
        self.assertEquals(payroll.company_id, company3,
                          'Company is not the contract company')
        self.contract.company_id = False
        payroll.onchange_employee()
        # payroll company is the default company
        self.assertEquals(payroll.company_id,
                          self.env['res.company']._company_default_get(),
                          'Company is not the default company')

    def test_013_resign_process(self):
        """Tests the re-sign process (recovery a previously signed xml)
        """
        payroll = self.create_payroll()
        payroll.action_payslip_done()
        self.assertEqual(payroll.l10n_mx_edi_pac_status, 'signed',
                         payroll.message_ids.mapped('body'))
        payroll.l10n_mx_edi_pac_status = 'retry'
        payroll.l10n_mx_edi_update_pac_status()
        self.assertEqual(payroll.l10n_mx_edi_pac_status, 'signed',
                         payroll.message_ids.mapped('body'))
        xml_attachs = payroll.l10n_mx_edi_retrieve_attachments()
        self.assertEqual(len(xml_attachs), 2)
        xml_1 = objectify.fromstring(base64.b64decode(xml_attachs[0].datas))
        xml_2 = objectify.fromstring(base64.b64decode(xml_attachs[1].datas))
        self.assertEqualXML(xml_1, xml_2)

    def create_payroll(self):
        return self.payslip_obj.create({
            'name': 'Payslip Test',
            'employee_id': self.employee.id,
            'contract_id': self.contract.id,
            'struct_id': self.struct.id,
            'l10n_mx_edi_source_resource': 'IP',
            'worked_days_line_ids': [(0, 0, {
                'name': 'Normal Working Days',
                'code': 'TESTNW',
                'number_of_days': 15,
                'number_of_hours': 40,
                'contract_id': self.contract.id,
            })],
            'input_line_ids': [(0, 0, {
                'code': 'pe_005',
                'name': 'Fondo de Ahorro',
                'amount': 200.0,
                'contract_id': self.contract.id,
            }), (0, 0, {
                'code': 'pg_019',
                'name': 'Horas extra',
                'amount': 300.0,
                'contract_id': self.contract.id,
            }), (0, 0, {
                'code': 'd_006',
                'name': 'Descuento por incapacidad',
                'amount': 100.0,
                'contract_id': self.contract.id,
            }), (0, 0, {
                'code': 'op_003',
                'name': u'Viáticos',
                'amount': 300.0,
                'contract_id': self.contract.id,
            })],
            'l10n_mx_edi_inability_line_ids': [(0, 0, {
                'amount': 100.0,
                'days': 1,
                'inability_type': '02',
            })],
            'l10n_mx_edi_overtime_line_ids': [(0, 0, {
                'amount': 300.0,
                'name': 'Overtime Test',
                'days': 1,
                'hours': 1,
                'overtime_type': '02',
            })],
        })

    def xml2dict(self, xml):
        """Receive 1 lxml etree object and return a dict string.
        This method allow us have a precise diff output"""
        def recursive_dict(element):
            return (element.tag,
                    dict(map(recursive_dict, element.getchildren()),
                         **element.attrib))
        return dict([recursive_dict(xml)])

    def assertEqualXML(self, xml_real, xml_expected):
        """Receive 2 objectify objects and show a diff assert if exists."""
        xml_expected = self.xml2dict(xml_expected)
        xml_real = self.xml2dict(xml_real)
        # noqa "self.maxDiff = None" is used to get a full diff from assertEqual method
        # This allow us get a precise and large log message of where is failing
        # expected xml vs real xml More info:
        # noqa https://docs.python.org/2/library/unittest.html#unittest.TestCase.maxDiff
        self.maxDiff = None
        self.assertEqual(xml_real, xml_expected)

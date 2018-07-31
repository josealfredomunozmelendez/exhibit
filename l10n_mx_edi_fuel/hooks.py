# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64
import logging
from os.path import join

# TODO: Add after merge https://github.com/Vauxoo/enterprise/pull/232/files
# from odoo.addons.l10n_mx_edi.hooks import _load_xsd_files
import requests
from lxml import etree, objectify

from odoo import SUPERUSER_ID, api, tools


def post_init_hook(cr, registry):
    complement_data = [
        {'url': 'http://www.sat.gob.mx/sitio_internet/cfd'
         '/EstadoDeCuentaCombustible/ecc12.xsd',
         'namespace': 'http://wwww.sat.gob.mx/EstadoDeCuentaCombustible12'},
        {'url': 'http://www.sat.gob.mx/sitio_internet/cfd'
         '/ConsumoDeCombustibles/consumodeCombustibles11.xsd',
         'namespace': 'http://wwww.sat.gob.ve/ConsumoDeCombustibles11'}]
    for complement in complement_data:
        _load_xsd_complement(cr, registry, complement.get('url'),
                             complement.get('namespace'))


def _load_xsd_complement(cr, registry, url, nspace):
    db_fname = _load_xsd_files(cr, registry, url)
    env = api.Environment(cr, SUPERUSER_ID, {})
    xsd = env.ref('l10n_mx_edi.xsd_cached_cfdv33_xsd', False)
    if not xsd:
        return False
    complement = {
        'namespace': nspace,
        'schemaLocation': db_fname,
    }
    node = etree.Element('{http://www.w3.org/2001/XMLSchema}import',
                         complement)
    res = objectify.fromstring(base64.decodebytes(xsd.datas))
    res.insert(0, node)
    xsd_string = etree.tostring(res, pretty_print=True)
    xsd.datas = base64.encodebytes(xsd_string)
    return True


def _load_xsd_files(cr, registry, url_dir):
    # TODO: Remove method after merge this PR
    # https://github.com/Vauxoo/enterprise/pull/232/files
    fname = url_dir.split('/')[-1]
    try:
        response = requests.get(url_dir, timeout=10)
        response.raise_for_status()
        res = objectify.fromstring(response.content)
    except (requests.exceptions.HTTPError, etree.XMLSyntaxError) as e:
        logging.getLogger(__name__).info(
            'I cannot connect with the given URL or you are trying to load an '
            'invalid xsd file.\n%s', e.message)
        return ''
    name_space = {'xs': 'http://www.w3.org/2001/XMLSchema'}
    sub_urls = res.xpath('//xs:import', namespaces=name_space)
    for url in sub_urls:
        url_catch = _load_xsd_files(
            cr, registry, url.get('schemaLocation'))
        url.attrib['schemaLocation'] = url_catch
    try:
        xsd_string = etree.tostring(res, pretty_print=True)
    except etree.XMLSyntaxError:
        logging.getLogger(__name__).info('XSD file downloaded is not valid')
        return ''
    env = api.Environment(cr, SUPERUSER_ID, {})
    xsd_fname = 'xsd_cached_%s' % fname.replace('.', '_')
    attach = env.ref('l10n_mx_edi.%s' % xsd_fname, False)
    filestore = tools.config.filestore(cr.dbname)
    if attach:
        return join(filestore, attach.store_fname)
    attach = env['ir.attachment'].create({
        'name': xsd_fname,
        'datas_fname': fname,
        'datas': base64.encodebytes(xsd_string),
    })
    # Forcing the triggering of the store_fname
    attach._inverse_datas()
    cr.execute(
        """INSERT INTO ir_model_data (name, res_id, module, model)
           VALUES (%s, %s, 'l10n_mx_edi', 'ir.attachment')""",
        (xsd_fname, attach.id))
    return join(filestore, attach.store_fname)

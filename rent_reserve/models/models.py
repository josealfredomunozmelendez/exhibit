# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import dateutil.parser

from dateutil import parser

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    devolution_date = fields.Date(string=_('Fecha de devolución'))
    location_id = fields.Many2one('stock.location', 'Ubicación')

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    @api.onchange('product_uom_qty')
    def _verify_reserved(self):
        location_id = 14#self.order_id.location_id.id
        
        if self.order_id.requested_date:
            requested_date = self.order_id.requested_date
        else:
            warning = {
                'title': _('Advertencia!'),
                'message': _('No ha definido la Fecha solicitada en Detalles del evento. No se ha podido verificar el inventario.'),
            }
            return {'warning': warning}
            #requested_date = '{}'.format(fields.datetime.now().replace( microsecond = 0 ))

        #check if we have pending product moves in the requested date
        product_pickings    = self.env['stock.move'].search(
            [
                ('product_id', '=', self.product_id.id),
                ('location_id', '=', location_id),
                ('date_expected', '>=', requested_date[:10] + " 00:00:00" ),
                ('date_expected', '<=', requested_date[:10] + " 23:59:59"),
            ]
        )
        print('##########################################')
        print(product_pickings)
        print('##########################################')
        
        # Falta filtrar por fechas, rango de fecha mayor y menor que
        if product_pickings:
            reserved = 0
            for product in product_pickings:
                reserved += product.product_uom_qty

            product = self.env['stock.quant'].search([
                ('product_id', '=', self.product_id.id),
                ('location_id', '=', location_id),
            ])
            available = product.quantity - reserved
            
            if available < self.product_uom_qty:
                warning = {
                    'title': _('Advertencia!'),
                    'message': _('No tiene suficientes {} para rentar ese día. Necesita al menos {} más en inventario para satisfacer la demanda.'.format(self.product_id.name, self.product_uom_qty - available)),
                }
                return {'warning': warning}
            
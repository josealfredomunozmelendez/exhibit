# -*- coding: utf-8 -*-

from odoo import models, fields


# class MrpProductionWorkcenterLine(models.Model):
#     _inherit = "mrp.workorder"

#     employee = fields.Many2one('hr.employee', 'Empleado')

#     def do_finish(self):
#         location_id = 15
#         has_stock = True

#         for line in self.production_id.bom_id.bom_line_ids:
#             stock = self.env['stock.quant'].search([
#                 ('product_id', '=', line.product_id.id),
#                 ('location_id', '=', location_id),
#             ])

#             if not stock or stock.quantity < line.product_qty:
#                 has_stock = False
#                 break

#         if has_stock:
#             self.record_production()
#             action = self.env.ref(
#                 'quality_mrp.mrp_workorder_action_tablet').read()[0]
#             action['domain'] = [('state', 'not in', [
#                                  'done', 'cancel', 'pending']), ('workcenter_id', '=', self.workcenter_id.id)]
#             return action
#         else:
#             raise exceptions.UserError(
#                 _('No tienes suficiente material en tu inventario para procesar esta orden.'))


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    priority = fields.Selection([
        (0, 'Baja'),
        (1, 'Media'),
        (2, 'Alta')], string='Prioridad')

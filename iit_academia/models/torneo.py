from odoo import models,fields

class Torneo(models.Model):
    _name = 'aca.torneo'

    name = fields.Char(string='Torneo', copy=False, default = 'Nuevo')
    fecha_inicial = fields.Date(string='Fecha Inicial',required=True)
    fecha_final = fields.Date(string='Fecha Final',required=True)
    inscripcion = fields.Float(string="Monto de Inscripcion", required=True, default = 0)
    observaciones = fields.Char(string='Observaciones')
    status = fields.Selection([ ('1','Activo'),('0','Inactivo')],string='Status',default='1',required=True)
    torneos_lines = fields.Many2many(comodel_name="aca.torneo.lines", inverse_name="torneo_id")


    def action_view_cargos(self):
        action = self.env.ref('iit_academia.cargos_generados_action').read()[0]
        action['domain'] = [('torneo_id','=',self.id)]
        return action

class TorneoLines(models.Model):
    _name = 'aca.torneo.lines'

    estudiante_id = fields.Many2one(string="Estudiante", comodel_name='aca.estudiante', required=True)
    torneo_id = fields.Many2one(comodel_name='aca.torneo')

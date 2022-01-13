import json

from odoo import models,fields,api

class Contrato(models.Model):
    _name = 'aca.contrato'

    name = fields.Char(string='Contrato', copy=False, readonly=True, default = 'Nuevo')
    fecha_inicial = fields.Date(string='Fecha Inicial',required=True)
    fecha_final = fields.Date(string='Fecha Final',required=True)
    inscripcion = fields.Float(string="Monto de Inscripcion", required=True, default = 0)
    mensualidad = fields.Float(string="Mensualidad", required=True, default = 0)
    observaciones = fields.Char(string='Observaciones')
    responsable_id = fields.Many2one(comodel_name='res.partner', required=True)
    estudiante_id = fields.Many2one(comodel_name='aca.estudiante', required=True)
    status = fields.Selection([ ('1','Activo'),('0','Inactivo')],string='Status',default='1',required=True)
    contratos_lines = fields.One2many(comodel_name="aca.contrato.lines", inverse_name="contrato_id")
    state = fields.Char(string="Estado", compute="_cargo_", readonly=True )
    payment_state = fields.Char(string="Estado de pago", compute="_cargo_", readonly=True)
    fecha_cargo = fields.Date(string='Fecha', readonly=True)




    _sql_constraints = [
        ('contrato_unico', 'unique(name)', "Ese contrato ya existe revisa la secuencia")
    ]

    def action_view_cargos(self):
        action = self.env.ref('iit_academia.cargos_generados_action').read()[0]
        action['domain'] = [('contrato_id','=',self.id)]
        return action

    @api.model
    def create(self,vals):
        if vals.get('name','Nuevo') == 'Nuevo':
            vals['name'] = self.env['ir.sequence'].next_by_code('aca.contratos.codigo') or 'Nuevo'

        estudiante = self.env['aca.estudiante'].browse(vals['estudiante_id'])
        resp = {
              "responsable_id" : vals['responsable_id']
        }
        estudiante.write(resp)

        result = super(Contrato,self).create(vals)
        return result

    def write(self,vals):
        result = super(Contrato,self).write(vals)
        estudiante = self.env['aca.estudiante'].browse(self.estudiante_id.id)
        resp = {
              "responsable_id" : self.responsable_id
        }
        estudiante.write(resp)
        return result



class ContratoLines(models.Model):
    _name = 'aca.contrato.lines'

    producto_id = fields.Many2one(string="Articulo", comodel_name='product.template', required=True)
    cantidad = fields.Integer(string="Cantidad", default=1, required=True)
    precio = fields.Float(Strig="Precio", default=0, required=True)
    contrato_id = fields.Many2one(comodel_name='aca.contrato')


    @api.onchange('producto_id')
    def _onchange_product_id(self):
        for line in self:
            line.precio = self.producto_id.list_price
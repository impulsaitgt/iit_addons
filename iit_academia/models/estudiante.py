from odoo import models,fields,api

class Estudiante(models.Model):
    _name = 'aca.estudiante'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nombre Completo', required=True)
    codigo = fields.Char(string='Codigo', copy='False', default='Nuevo', readonly=True)
    fecha_nacimiento = fields.Date(string='Fecha de nacimiento',required=True)
    genero = fields.Selection([ ('M','Masculino'),('F','Femenino')],string='Genero',required=True)
    cui = fields.Char(string='CUI', required=True)
    status_contratos = fields.Char(string='Status Contratos',compute="_contratos_",default='Nuevo')
    status_torneos = fields.Char(string='Status Torneos',compute="_torneos_",default='Nuevo')
    estatura = fields.Float(string="Estatura en metros", required=True, tracking=True)
    talla = fields.Selection([ ('8','8'),('10','10'),('12','12'),('14','14'),('S','Small'),('M','Medium'),('L2','Large'),('XL','Extra Large')],string="Talla de Uniforme", default='8', required=True, tracking=True)
    peso = fields.Float(string="Peso en libras", required=True, tracking=True)
    anio_nacimiento = fields.Integer(string="Año de nacimiento", compute="_calcula_anio_", readonly=True)
    responsable_id = fields.Many2one(comodel_name='res.partner')
    foto = fields.Binary(string="Foto")

    _sql_constraints = [
        ('codigo_unico', 'unique(codigo)', "Ese codigo ya existe revisa la secuencia")
    ]


    def _calcula_anio_(self):
        anio_nacimiento = self.fecha_nacimiento.year
        self.anio_nacimiento = anio_nacimiento

    def _contratos_(self):
        for estudiante in self:
            contratos = (self.env['aca.contrato'].search_count([('estudiante_id','=',estudiante.id),
                                                               ('status','=','1')])) > 0
            if contratos:
                estudiante.status_contratos = 'Activo'
            else:
                estudiante.status_contratos = 'Inactivo'

    def _torneos_(self):
        for estudiante in self:
            torneos = (self.env['aca.torneo'].search_count([('torneos_lines.estudiante_id','=',estudiante.id),
                                                                 ('status','=','1')])) > 0
            if torneos:
                estudiante.status_torneos = 'Activo'
            else:
                estudiante.status_torneos = 'Inactivo'


    def action_view_contratos(self):
        action = self.env.ref('iit_academia.contratos_action').read()[0]
        action['domain'] = [('estudiante_id','=',self.id)]
        return action

    def action_view_torneos(self):
        action = self.env.ref('iit_academia.torneos_action').read()[0]
        action['domain'] = [('torneos_lines.estudiante_id','=',self.id)]
        return action

    def action_view_cargos(self):
        action = self.env.ref('iit_academia.cargos_generados_action').read()[0]
        action['domain'] = [('estudiante_id','=',self.id)]
        return action

    @api.model
    def create(self,vals):
        if vals.get('codigo','Nuevo') == 'Nuevo':
            vals['codigo'] = self.env['ir.sequence'].next_by_code('aca.estudiantes.codigo') or 'Nuevo'

        result = super(Estudiante,self).create(vals)
        return result


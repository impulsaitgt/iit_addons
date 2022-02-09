from odoo import models,fields,api

class Cotizador(models.Model):
    _name = 'lot.cotizador'

    name = fields.Char(string='Cotizacion', copy=False, readonly=True, default='Nuevo')
    inmueble_id = fields.Many2one(comodel_name='lot.inmueble', required=True)
    enganche = fields.Float(string="Enganche",required=True)
    fecha_inicial = fields.Date(string="Fecha inicial",required=True)
    plazo = fields.Integer(string="Plazo",required=True)
    tipo_de_interes = fields.Selection([ ('1','Sobre saldos'),('0','Flat')],string='Tipo de interes',required=True)
    tasa_de_interes = fields.Float(string="Tasa de interes",required=True)
    cliente_id = fields.Many2one(comodel_name='res.partner', string="Cliente", required=True)
    cotizador_lines = fields.One2many(comodel_name='lot.cotizador.lines', inverse_name='cotizador_id')
    state = fields.Selection([('draft', 'Borrador'), ('published', 'Publicado'), ('cancelled', 'Cancelado')],
                             string='Estado', default='draft')

    @api.model
    def create(self, vals):
        if vals.get('name','Nuevo') == 'Nuevo':
            vals['name'] = self.env['ir.sequence'].next_by_code('lot.cotizador.numero') or 'Nuevo'

        result = super(Cotizador,self).create(vals)
        return result

    def action_genera_cuotas(self):
        # elimino cuotas anteriores
        lineas = self.cotizador_lines
        for linea in lineas:
            linea.unlink()

        # genero cuotas
        i = 0
        while i < self.plazo:
            i += 1
            valscuota = {
                'cuota': i,
                'fecha': self.fecha_inicial,
                'capital': 1000,
                'intereses': 100,
                'cotizador_id': self.id
            }
            cotizador = self.env["lot.cotizador"].search([("id", "=", self.id)])
            cotizador.cotizador_lines.create(valscuota)

    def action_confirma_cuotas(self):
        print("Le di confirmar")
        self.state="published"

    def action_reestablece_borrador(self):
        print("Restablecer")
        self.state="draft"

    def action_cancela(self):
        print("Cancelar")

class CotizadorLines(models.Model):
    _name = 'lot.cotizador.lines'

    cotizador_id = fields.Many2one(comodel_name='lot.cotizador')
    fecha = fields.Date(string="Fecha", required=True)
    capital = fields.Float(string="Capital", default=0)
    intereses = fields.Float(string="Intereses", default=0)
    cuota = fields.Integer(string="Cuota", default=0)
    cuota_total = fields.Float(string="Cuota total", compute="_cuota_total_")

    def _cuota_total_(self):
        for linea in self:
            linea.cuota_total = linea.capital + linea.intereses



from odoo import models,fields

class Boleta(models.Model):
    _name = 'lot.boleta'

    name = fields.Char(string="Nombre",required=True)
    monto = fields.Float(string="Monto Boleta",required=True, default=0)
    cotizador_lines = fields.One2many(comodel_name='lot.cotizador.lines', inverse_name='boleta_id')

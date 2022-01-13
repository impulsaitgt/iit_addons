from odoo import models, fields


class Estudiante(models.Model):
    _name = 'tie.juego'

    name = fields.Char(string='Juego', required=True)
    precio = fields.Float(sring="Precio", required=True, Default=0)
    activo = fields.Selection([('S', 'Si'), ('N', 'No')], string='Esta activo', required=True)

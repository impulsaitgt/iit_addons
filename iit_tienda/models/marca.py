from odoo import models, fields


class Marca(models.Model):
    _name = 'tie.marca'

    name = fields.Char(string='Marca', required=True)
    descripcion = fields.Char(sring="Descripcion", required=True)

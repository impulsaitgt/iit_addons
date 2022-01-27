from odoo import models,fields,api

class Inmueble(models.Model):
    _name = 'lot.inmueble'

    name = fields.Char(string="Nombre",required=True)
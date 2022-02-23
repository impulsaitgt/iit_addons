from odoo import models,fields,api

class Inmueble(models.Model):
    _name = 'lot.inmueble'

    name = fields.Char(string="Nombre",required=True)
    direccion = fields.Char(string="Direccion")
    numero_de_escritura = fields.Char(string="Numero de escritura")
    precio_a_publico = fields.Float(string="Precio a publico",required=True, default=0)
    precio_minimo = fields.Float(string="Precio a minimo",required=True, default=0)
    reserva = fields.Float(string="Reserva",required=True, default=0)
    foto = fields.Binary(string="Foto")






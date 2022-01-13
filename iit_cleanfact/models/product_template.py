from odoo import api, models, fields


class product_template(models.Model):
    _inherit = "product.template"

    cf_unixcaja = fields.Integer(string='Unidades por caja', default=0) # Unidades por caja
    cf_preslitros = fields.Integer(string='Presentacion en litros', default=0) # Presentacion en litros


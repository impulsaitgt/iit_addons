from odoo import models, fields


class product_template(models.Model):
    _inherit = "product.template"

    aca_mensualidad_academia = fields.Boolean(string='Mensualidad Academia',default=False)
    aca_inscripcion_academia = fields.Boolean(string='Inscripcion Academia', default=False)
    aca_torneo_academia = fields.Boolean(string='Inscripcion Torneo', default=False)



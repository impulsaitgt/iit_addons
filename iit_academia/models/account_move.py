from odoo import models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    estudiante_id = fields.Many2one(comodel_name='aca.estudiante')

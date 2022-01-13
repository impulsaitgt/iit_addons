from odoo import models, fields



class AccountJournal(models.Model):
    _inherit = 'account.journal'

    aca_tipo_registro = fields.Selection([ ('1','Otro'),('2','Normal'),('3','Donacion')],string='Tipo de Registro',default='1',required=True)

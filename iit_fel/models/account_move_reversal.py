from odoo import api, models, fields

class account_move_reversal(models.TransientModel):
    _inherit = "account.move.reversal"

    # @api.model
    # def reverse_moves(self, vals):
    #     print("previo capturo al revertir")
    #     res = super(account_move_reversal, self).reverse_moves()
    #     print("capturo al revertir")
    #     return res

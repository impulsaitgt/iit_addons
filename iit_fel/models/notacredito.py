from odoo import api, models
from odoo.exceptions import ValidationError


class account_move_reversal(models.TransientModel):
    _inherit = "account.move.reversal"

    @api.model
    def reverse_moves(self,vals):
        print('Aqui llegamos')
        print(self)
        print(vals[0])
        print(super)

        res = super().reverse_moves()

        print(self.move_ids)

        return res

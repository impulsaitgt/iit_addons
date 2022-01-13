from odoo import api, models, fields
from odoo.exceptions import ValidationError

class sale_order(models.Model):
    _inherit = "account.move"

    factura_fel = fields.Char(string='Autorizacion FEL') #registro electronico

# class sale_advance_payment_inv(models.Model):
#     _inherit = "sale.order"
#
#     @api.model
#     def create_invoices(self,vals):
#         res = super(sale_advance_payment_inv, self).create_invoices(vals)
#
#         print("Res = ", res)
#
#         raise ValidationError('Estas por fin donde debes estar')
#
#         return res
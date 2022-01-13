from odoo import api, models, fields
from odoo.exceptions import ValidationError
import urllib, json

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    felectronica = fields.Char(string='Factura Electronica') #nombre del campo que es de tipo cadena


    @api.model
    def create(self,vals):
        res = super(ProductTemplate, self).create(vals)

        url = "https://jsonplaceholder.typicode.com/todos/1"
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())

        print("Res = ", res)
        print("vals = ", vals)
        print("nombre = ", vals.get('name', 'Error'))

        vals['felectronica'] = data.get('title','Error')
        vals['name'] = 'me la pela'
        print("vals = ", vals)
        print("felectronica = ", vals.get('felectronica', 'Error'))

        self = self.with_context({
            'felectronica': 'sera?',
            'name' : 'me la pela'
        })

        print(data)
        print("felectronica =", self._context)

        return res

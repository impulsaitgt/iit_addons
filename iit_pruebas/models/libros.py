from odoo import api, models, fields
from odoo.exceptions import ValidationError
import urllib, json


#Creando un modelo (tabla de la base de datos) a partir de una clase
class Libros(models.Model):
    _name='libros' #nombre de la tabla que se va a generar
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def action_test(self):
        raise ValidationError("Mensaje en Accion")

    def accion_prueba(self):
        raise ValidationError("Mensaje en Accion de Prueba")


    name = fields.Char(string='Nombre del libro', required=True, tracking=True) #nombre del campo que es de tipo cadena
    editorial = fields.Char(string='Editorial del libro',required=True) #editorial del libro
    isbn = fields.Char(string='ISBN del libro',required=True) #isbn del libro
    autor_id = fields.Many2one(comodel_name="autores", string='Autor', required=True)
    image = fields.Binary(string="Image")
    categoria_id = fields.Many2one(comodel_name='categoria.libro')
    state = fields.Selection([('draft','Borrador'),('published','Publicado')], default='draft')

    _sql_constraints = [("name_unique","unique(name)","El nombre del libro ya existe")]


class CategoriaLibro(models.Model):
    _name = 'categoria.libro'

    name = fields.Char(string="Nombre de la categoria")


    # nombre del sql constraint
    # unique () los valores que no queremos que se dupliquen
    # mensaje de error

    #
    # @api.model
    # def create(self,vals):
    #     res = super(Libros, self).create(vals)
    #     print("Res = ", res)
    #     print("vals = ", vals)
    #
    #     url = "https://jsonplaceholder.typicode.com/todos"
    #     response = urllib.request.urlopen(url)
    #     data = json.loads(response.read())
    #
    #     print(data)
    #
    #     raise ValidationError(data)
    #     return res

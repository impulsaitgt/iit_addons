from odoo import api, models, fields
import json, requests

class Libros(models.Model):
    _name='autores' #nombre de la tabla que se va a generar

    name = fields.Char(string='Nombre del autor', required=True) #nombre del campo que es de tipo cadena
    nit = fields.Char(string='Nit', default='CF', required=True) #nombre del campo que es de tipo cadena
    nombre_comercial = fields.Char(string='Nombre comercial', required=True) #nombre de la sat

    @api.onchange('nit')
    def onchange_nit(self):
        if (self.nit):
            self.nombre_comercial = "Aqui se actualiza "+self.nit

            url = "https://consultareceptores.feel.com.gt/rest/action"

            data = {
                'emisor_codigo': "2459413K",
                'emisor_clave': "46155CE198281D56C1F479082C6946C7",
                'nit_consulta': self.nit
            }

            headers = {
                 'Content-Type': "application/json"
            }


            response = requests.post(url, json=data, headers=headers)

            data = json.loads(response.text)

            self.nombre_comercial = data['nombre']

from odoo import api, models, fields
import json, requests


class ResPartner(models.Model):
    _inherit = 'res.partner'

    fel_nombre_sat = fields.Char(string='Nombre SAT', default="Consumidor Final") # Nombre SAT

    @api.onchange('vat')
    def onchange_vat(self):
        if (self.vat):

            url = "https://consultareceptores.feel.com.gt/rest/action"

            data = {
                # 'emisor_codigo': "2459413K",
                # 'emisor_clave': "46155CE198281D56C1F479082C6946C7",
                'emisor_codigo': self.env.company.fel_emisor_codigo,
                'emisor_clave': self.env.company.fel_emisor_clave,
                'nit_consulta': self.vat
            }

            headers = {
                 'Content-Type': "application/json"
            }


            response = requests.post(url, json=data, headers=headers)

            data = json.loads(response.text)

            self.fel_nombre_sat = data['nombre']


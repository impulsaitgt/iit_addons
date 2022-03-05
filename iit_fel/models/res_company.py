from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.company'

    fel_emisor_codigo = fields.Char(string='Emisor Codigo')
    fel_emisor_clave = fields.Char(string='Emisor Clave')
    fel_entorno = fields.Selection([ ('P','Produccion'),('D','Desarrollo/Pruebas')],string='Entorno',required=True, default='D')

    fel_UsuarioFirma = fields.Char(string='Usuario Firma')
    fel_LlaveFirma = fields.Char(string='Llave Firma')
    fel_UsuarioApi = fields.Char(string='Usuario Api')
    fel_LlaveApi = fields.Char(string='Llave Api')
    fel_service = fields.Selection([ ('S','Si'),('N','No')],string='Usa Web Service',required=True, default='N')

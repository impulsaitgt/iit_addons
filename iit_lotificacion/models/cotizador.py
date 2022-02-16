from odoo import models,fields,api
from dateutil.relativedelta import relativedelta

class Cotizador(models.Model):
    _name = 'lot.cotizador'

    name = fields.Char(string='Cotizacion', copy=False, readonly=True, default='Nuevo')
    inmueble_id = fields.Many2one(comodel_name='lot.inmueble', required=True)
    enganche = fields.Float(string="Enganche",required=True)
    fecha_inicial = fields.Date(string="Fecha inicial",required=True)
    plazo = fields.Integer(string="Plazo",required=True)
    tipo_de_interes = fields.Selection([ ('1','Sobre saldos'),('0','Flat')],string='Tipo de interes',required=True)
    tasa_de_interes = fields.Float(string="Tasa de interes",required=True)
    cliente_id = fields.Many2one(comodel_name='res.partner', string="Cliente", required=True)
    cotizador_lines = fields.One2many(comodel_name='lot.cotizador.lines', inverse_name='cotizador_id')
    state = fields.Selection([('draft', 'Borrador'), ('published', 'Publicado'), ('cancelled', 'Cancelado')],
                             string='Estado', default='draft')
    precio = fields.Float(string="Precio", default=0)
    monto_financiar = fields.Float(string="Monto a financiar", readonly=True, compute="_montof_")
    suma_capital = fields.Float(string="Total Capital", readonly=True, compute="_montof_")
    suma_intereses = fields.Float(string="Total Interes", readonly=True, compute="_montof_")
    suma_cuotas = fields.Float(string="Total", readonly=True, compute="_montof_")

    @api.model
    def create(self, vals):
        if vals.get('name','Nuevo') == 'Nuevo':
            vals['name'] = self.env['ir.sequence'].next_by_code('lot.cotizador.numero') or 'Nuevo'

        result = super(Cotizador,self).create(vals)
        return result


    def action_genera_cuotas(self):
        # elimino cuotas anteriores
        lineas = self.cotizador_lines
        for linea in lineas:
            linea.unlink()

        # genero cuotas
        tasa_mensual = self.tasa_de_interes / 100 / 12
        factor1 = 1 - ((1 + tasa_mensual) ** (self.plazo * -1))
        factor2 = factor1 / tasa_mensual
        cuota_base = round(self.monto_financiar / factor2, 2)
        financiamiento = self.monto_financiar
        fecha_cuota = self.fecha_inicial
        delta_mes = relativedelta(months=1)


        i = 0
        while i < self.plazo:
            interes = round(financiamiento * tasa_mensual, 2)
            capital = round(cuota_base - interes, 2)
            financiamiento = financiamiento - capital

            i += 1
            valscuota = {
                'cuota': i,
                'fecha': fecha_cuota,
                'capital': capital,
                'intereses': interes,
                'cotizador_id': self.id
            }
            cotizador = self.env["lot.cotizador"].search([("id", "=", self.id)])
            cotizador.cotizador_lines.create(valscuota)
            fecha_cuota = fecha_cuota + delta_mes

    def action_confirma_cuotas(self):
        self.state="published"

    def action_reestablece_borrador(self):
        self.state="draft"

    def action_cancela(self):
        print("Cancelar")

    def _montof_(self):
        for cotizador in self:
            cotizador.monto_financiar = cotizador.precio - cotizador.enganche
            capital = 0
            intereses = 0
            cuotas = 0
            for linea in cotizador.cotizador_lines:
                capital = capital + linea.capital
                intereses = intereses + linea.intereses
                cuotas = cuotas + linea.cuota_total
            cotizador.suma_capital = capital
            cotizador.suma_intereses = intereses
            cotizador.suma_cuotas = cuotas


class CotizadorLines(models.Model):
    _name = 'lot.cotizador.lines'

    cotizador_id = fields.Many2one(comodel_name='lot.cotizador')
    fecha = fields.Date(string="Fecha", required=True)
    capital = fields.Float(string="Capital", default=0)
    intereses = fields.Float(string="Intereses", default=0)
    cuota = fields.Integer(string="Cuota", default=0)
    cuota_total = fields.Float(string="Cuota total", compute="_cuota_total_")
    valor_pagado = fields.Float(string="Valor Pagado", default=0)
    state = fields.Char(string="Estado",compute="_estado_")

    def _cuota_total_(self):
        for linea in self:
            linea.cuota_total = linea.capital + linea.intereses




from odoo import models,fields,api
from dateutil.relativedelta import relativedelta
from datetime import datetime
import math

class Cotizador(models.Model):
    _name = 'lot.cotizador'

    name = fields.Char(string='Cotizacion', copy=False, readonly=True, default='Nuevo')
    inmueble_id = fields.Many2one(comodel_name='lot.inmueble', required=True)
    enganche = fields.Float(string="Enganche",required=True)
    fecha_inicial = fields.Date(string="Fecha inicial",required=True)
    fecha_generacion = fields.Date(string="Fecha inicial",required=True, readonly=True)
    plazo = fields.Integer(string="Plazo",required=True)
    tipo_de_interes = fields.Selection([ ('1','Sobre saldos'),('0','Flat')],string='Tipo de interes',required=True)
    tasa_de_interes = fields.Float(string="Tasa de interes",required=True)
    cliente_id = fields.Many2one(comodel_name='res.partner', string="Cliente", required=True)
    cotizador_lines = fields.One2many(comodel_name='lot.cotizador.lines', inverse_name='cotizador_id')
    cotizador_enganche_lines = fields.One2many(comodel_name='lot.cotizador.enganche.lines', inverse_name='cotizador_id')

    state = fields.Selection([('draft', 'Borrador'), ('published', 'Publicado'), ('cancelled', 'Cancelado')],
                             string='Estado', default='draft')
    precio = fields.Float(string="Precio", default=0)
    monto_financiar = fields.Float(string="Monto a financiar", readonly=True, compute="_montof_")
    suma_capital = fields.Float(string="Total Capital", readonly=True, compute="_montof_")
    suma_intereses = fields.Float(string="Total Interes", readonly=True, compute="_montof_")
    suma_cuotas = fields.Float(string="Total", readonly=True, compute="_montof_")
    cuota_uno = fields.Float(string="Cuota 1", readonly=True, default=0)
    cuota_normal = fields.Float(string="Cuota Normal", readonly=True, default=0)
    enganche_pagado = fields.Float(string="Enganche Pagado", readonly=True, compute="_montof_")
    cuota_final = fields.Float(string="Cuota Normal", readonly=True, default=0)


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
        cbd10 = cuota_base / 10
        truncado = math.trunc(cbd10) * 10
        valsnormal = {
            'cuota_normal': truncado,
            'fecha_generacion': datetime.today()
        }
        self.write(valsnormal)
        delta = round(cuota_base - truncado, 2)
        financiamiento = self.monto_financiar
        fecha_cuota = self.fecha_inicial
        delta_mes = relativedelta(months=1)


        i = 0
        while i < self.plazo:
            if (i == 0):
                interes = round(financiamiento * tasa_mensual, 2)
                capital = round(cuota_base - interes + (delta * (self.plazo - 1)), 2)
                financiamiento = financiamiento - capital

                vals1 = {
                    'cuota_uno': round(interes + capital, 2)
                }
                self.write(vals1)


            elif (i == self.plazo - 1):
                capital = financiamiento
                interes = round(financiamiento * tasa_mensual, 2)

                valsfinal = {
                    'cuota_final': round(interes + capital, 2)
                }
                self.write(valsfinal)
            else:
                interes = round(financiamiento * tasa_mensual, 2)
                capital = round(truncado - interes, 2)
                financiamiento = financiamiento - capital

            i += 1
            valscuota = {
                'cuota': i,
                'fecha': fecha_cuota,
                'capital': capital,
                'intereses': interes,
                'cotizador_id': self.id
            }
            # cotizador = self.env["lot.cotizador"].search([("id", "=", self.id)])
            # cotizador.cotizador_lines.create(valscuota)
            # self.env["lot.cotizador"].search([("id", "=", self.id)]).cotizador_lines.create(valscuota)
            self.cotizador_lines.create(valscuota)

            fecha_cuota = fecha_cuota + delta_mes

    def action_confirma_cuotas(self):
        self.state="published"

    def action_reestablece_borrador(self):
        self.state="draft"

    def action_cancela(self):
        self.state="cancelled"

    def action_registrar_pago(self):
        action = self.env.ref('iit_lotificacion.action_registra_pago').read()[0]
        action['domain'] = [('lot.registra.pago.wizard.cotizador_id', '=', self.id)]
        return action

    def action_imprime_cotizacion(self):
        print("aqui imprimo cotizacion: ", self)

    def action_imprime_estado_cuenta(self):
        print("aqui imprimo estado de cuenta: ", self)

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
            enganche_pagado = 0
            for eng in cotizador.cotizador_enganche_lines:
                enganche_pagado = enganche_pagado + eng.valor_pagado
            cotizador.enganche_pagado = enganche_pagado


class CotizadorLines(models.Model):
    _name = 'lot.cotizador.lines'

    cotizador_id = fields.Many2one(comodel_name='lot.cotizador')
    fecha = fields.Date(string="Fecha", required=True)
    fecha_pago = fields.Date(string="Fecha Pagado")
    capital = fields.Float(string="Capital", default=0)
    intereses = fields.Float(string="Intereses", default=0)
    cuota = fields.Integer(string="Cuota", default=0)
    cuota_total = fields.Float(string="Cuota total", compute="_cuota_total_")
    valor_pagado = fields.Float(string="Valor Pagado", default=0)
    boleta_id = fields.Many2one(comodel_name='lot.boleta')
    cargo_capital_id = fields.Many2one(string="Cargo capital", comodel_name='account.move', readonly=True)
    cargo_intereses_id = fields.Many2one(string="Factura Interes", comodel_name='account.move', readonly=True)
    cargo_mora_id = fields.Many2one(string="Factura Mora", comodel_name='account.move', readonly=True)


    def _cuota_total_(self):
        for linea in self:
            linea.cuota_total = linea.capital + linea.intereses

class CotizadorEngancheLines(models.Model):
    _name = 'lot.cotizador.enganche.lines'

    cotizador_id = fields.Many2one(comodel_name='lot.cotizador')
    fecha = fields.Date(string="Fecha", required=True)
    valor_pagado = fields.Float(string="Valor Pagado", default=0)
    boleta_id = fields.Many2one(comodel_name='lot.boleta')
    cargo_enganche_id = fields.Many2one(string="Cargo Enganche", comodel_name='account.move', readonly=True)


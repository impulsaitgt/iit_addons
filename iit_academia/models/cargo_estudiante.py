from odoo import models,fields,api
from datetime import datetime
from odoo.exceptions import ValidationError


class CargoEstudiante(models.Model):
    _name = 'aca.cargo.estudiante'

    name = fields.Char(string='Referencia', default = 'Nuevo')
    fecha = fields.Date(string='Fecha',default=datetime.today(), readonly=True)
    cargo_estudiante_lines = fields.One2many(comodel_name="aca.cargo.estudiante.lines",inverse_name='cargo_estudiante_id')
    state = fields.Selection([('draft', 'Borrador'), ('published', 'Publicado'), ('cancelled', 'Cancelado')], string='Estado', default='draft')
    monto = fields.Float(string='Monto Total', readonly=True, compute='_monto_')


    _sql_constraints = [
        ('referencia_unica', 'unique(name)', "Esa referencia ya existe, escoge otra")
    ]

    def _monto_(self):
        for cargoEstudiante in self:
            monto = 0
            for linea in cargoEstudiante.cargo_estudiante_lines:
                monto = monto + linea.monto
            cargoEstudiante.monto = monto

    def _mes_(self):
        mes = int(str(self.fecha).split('-')[1])
        self.mes = mes

    def action_genera_cargos(self):

        lineas = self.cargo_estudiante_lines
        for linea in lineas:
            if linea.cargo_id.state == 'draft' and not linea.cargo_id.posted_before:
                cargo_id = linea.cargo_id.id
                linea.unlink()
                cargo = self.env['account.move'].search([('id', '=', cargo_id)])
                cargo.unlink()

        contratos = self.env['aca.contrato'].search([('status', '=', '1')])
        torneos = self.env['aca.torneo'].search([('status', '=', '1')])
        mes = int(str(self.fecha).split('-')[1])
        anio = int(str(self.fecha).split('-')[0])

        normal = self.env['account.journal'].search([('aca_tipo_registro', '=', '2')]).id
        donacion = self.env['account.journal'].search([('aca_tipo_registro', '=', '3')]).id
        mensualidad = self.env['product.template'].search([('aca_mensualidad_academia', '=', True)]).id
        inscripcion = self.env['product.template'].search([('aca_inscripcion_academia', '=', True)]).id
        inscripcion_torneo = self.env['product.template'].search([('aca_torneo_academia', '=', True)]).id



        # Genera cargos para contratos
        for contrato in contratos:

            # Genera el cargo de inscripcion
            inscripcion_cargo = (self.env['aca.cargo.estudiante.lines'].search_count([('contrato_id', '=', contrato.id),
                                                                                      ('cargo_id.state', '!=', 'cancel'),
                                                                                      ('tipo', '=', 'Inscripcion')])) > 0

            if (contrato.inscripcion > 0 and not inscripcion_cargo):
                valscargo = {
                    'move_type' : 'out_invoice',
                    'state' : 'draft',
                    'partner_id' : contrato.responsable_id.id,
                    'estudiante_id': contrato.estudiante_id,
                    'journal_id' : donacion,
                    'payment_reference' : contrato.name,
                    'invoice_line_ids': [(0, 0, {'product_id': inscripcion, 'price_unit': contrato.inscripcion})]
                }

                cargo = self.env['account.move'].create(valscargo)
                valslines = {'contrato_id': contrato.id,
                             'cargo_id' : cargo.id,
                             'estudiante_id': contrato.estudiante_id.id,
                             'responsable_id': contrato.responsable_id.id,
                             'cargo_estudiante_id': self.id,
                             'tipo' : 'Inscripcion'}

                cargos_estudiante = self.env['aca.cargo.estudiante'].search([('id', '=', self.id)])
                cargos_estudiante.cargo_estudiante_lines.create(valslines)


            # Genera el cargo de articulos
            lineas_articulos = contrato.contratos_lines

            articulos_cargo = (self.env['aca.cargo.estudiante.lines'].search_count([('contrato_id', '=', contrato.id),
                                                                                    ('cargo_id.state', '!=', 'cancel'),
                                                                                    ('tipo', '=', 'Articulos')])) > 0

            if (lineas_articulos and not articulos_cargo):
                valscargo = {
                    'move_type': 'out_invoice',
                    'state': 'draft',
                    'partner_id': contrato.responsable_id.id,
                    'estudiante_id': contrato.estudiante_id,
                    'journal_id': normal,
                    'payment_reference': contrato.name
                }
                cargo = self.env['account.move'].create(valscargo)

                valslines = {'contrato_id': contrato.id,
                             'cargo_id': cargo.id,
                             'estudiante_id': contrato.estudiante_id.id,
                             'responsable_id': contrato.responsable_id.id,
                             'cargo_estudiante_id': self.id,
                             'tipo' : 'Articulos'}

                cargos_estudiante = self.env['aca.cargo.estudiante'].search([('id', '=', self.id)])
                cargos_estudiante.cargo_estudiante_lines.create(valslines)

                for linea in lineas_articulos:
                    if linea.producto_id.taxes_id:
                        valslinea = {
                            'invoice_line_ids': [(0, 0,
                                                 {'product_id': linea.producto_id.id, 'price_unit': linea.precio,
                                                  'tax_ids': linea.producto_id.taxes_id})]
                            }
                    else:
                        valslinea = {
                           'invoice_line_ids': [
                               (0, 0, {'product_id': linea.producto_id.id, 'price_unit': linea.precio})]
                            }

                    cargo.write(valslinea)

            # Genera el cargo mensualidad
            cargos = (self.env['aca.cargo.estudiante.lines'].search_count([('mes', '=', mes),
                                                                           ('anio', '=', anio),
                                                                           ('contrato_id', '=', contrato.id),
                                                                           ('cargo_id.state', '!=', 'cancel'),
                                                                           ('tipo', '=', 'Mensualidad')])) > 0

            # Verifica si no tiene ya creados cargos
            if not cargos:

                valscargo = {
                    'move_type' : 'out_invoice',
                    'state' : 'draft',
                    'partner_id' : contrato.responsable_id.id,
                    'estudiante_id': contrato.estudiante_id,
                    'journal_id' : donacion,
                    'payment_reference' : contrato.name,
                    'invoice_line_ids': [(0, 0, {'product_id': mensualidad, 'price_unit': contrato.mensualidad})]
                }

                cargo = self.env['account.move'].create(valscargo)

                valslines = {'contrato_id': contrato.id,
                             'cargo_id' : cargo.id,
                             'estudiante_id': contrato.estudiante_id.id,
                             'responsable_id': contrato.responsable_id.id,
                             'cargo_estudiante_id': self.id,
                             'anio' : anio,
                             'mes' : mes,
                             'tipo' : 'Mensualidad'}

                cargos_estudiante = self.env['aca.cargo.estudiante'].search([('id', '=', self.id)])
                cargos_estudiante.cargo_estudiante_lines.create(valslines)

        # Genera cargos para torneos
        for torneo in torneos:
            estudiantes_torneo = torneo.torneos_lines
            for estudiante in estudiantes_torneo:
                torneo_cargo = (self.env['aca.cargo.estudiante.lines'].search_count([('torneo_id', '=', torneo.id),
                                                                                     ('cargo_id.state', '!=', 'cancel'),
                                                                                     ('tipo', '=', 'Torneo'),
                                                                                     ('estudiante_id', '=', estudiante.estudiante_id.id)])) > 0
                if not torneo_cargo:
                    valscargo = {
                        'move_type': 'out_invoice',
                        'state': 'draft',
                        'partner_id': estudiante.estudiante_id.responsable_id.id,
                        'estudiante_id': estudiante.estudiante_id.id,
                        'journal_id': donacion,
                        'payment_reference': torneo.name,
                        'invoice_line_ids': [(0, 0, {'product_id': inscripcion_torneo, 'price_unit': torneo.inscripcion})]
                    }

                    cargo = self.env['account.move'].create(valscargo)
                    valslines = {'torneo_id': torneo.id,
                                 'cargo_id': cargo.id,
                                 'estudiante_id': estudiante.estudiante_id.id,
                                 'responsable_id': estudiante.estudiante_id.responsable_id.id,
                                 'cargo_estudiante_id': self.id,
                                 'tipo': 'Torneo'}

                    cargos_estudiante = self.env['aca.cargo.estudiante'].search([('id', '=', self.id)])
                    cargos_estudiante.cargo_estudiante_lines.create(valslines)




    def action_confirma_cargos(self):
        self.state = 'published'
        lineas = self.cargo_estudiante_lines
        for linea in lineas:
            if linea.cargo_id.state == 'draft':
                linea.cargo_id.action_post()

    def action_reestablece_borrador(self):
        self.state = 'draft'
        lineas = self.cargo_estudiante_lines
        for linea in lineas:
            if linea.cargo_id.state == 'posted' or linea.cargo_id.state == 'cancel':
                linea.cargo_id.button_draft()

    def action_cancela(self):
        self.state = 'cancelled'
        lineas = self.cargo_estudiante_lines
        for linea in lineas:
            if linea.cargo_id.state == 'posted':
                raise ValidationError('No se pueden cancelar cargos publicados debes reestablecer a borrador primero')
            if linea.cargo_id.state == 'draft':
                linea.cargo_id.button_cancel()

    def write(self, vals):
        lineas_self_antes = self.cargo_estudiante_lines
        cargos_lines = {}
        for linea_self_antes in lineas_self_antes:
           cargos_lines[linea_self_antes.id] = linea_self_antes.cargo_id.id

        res = super(CargoEstudiante, self).write(vals)

        lineas_vals_dic = vals.get('cargo_estudiante_lines')
        if lineas_vals_dic:
            for linea_vals in lineas_vals_dic:
                if not linea_vals[1] in self.cargo_estudiante_lines.ids:
                    cargo_id = cargos_lines.get(linea_vals[1])
                    cargo = self.env['account.move'].search([('id', '=', cargo_id)])
                    cargo.unlink()


        # raise ValidationError('detenido bien')

        return res


class CargoEstudianteLines(models.Model):
    _name = 'aca.cargo.estudiante.lines'

    contrato_id = fields.Many2one(string="Contrato", comodel_name='aca.contrato')
    torneo_id = fields.Many2one(string="Torneo", comodel_name='aca.torneo')
    estudiante_id = fields.Many2one(string="Estudiante", comodel_name='aca.estudiante', required=True)
    responsable_id = fields.Many2one(string="Responsable", comodel_name='res.partner', required=True)
    monto = fields.Float(string="Monto",compute="_lineas_" )
    cargo_id = fields.Many2one(string="Cargo", comodel_name='account.move', required=True, readonly=True)
    cargo_estudiante_id = fields.Many2one(comodel_name='aca.cargo.estudiante')
    state = fields.Char(string="Estado",compute="_lineas_" )
    diario = fields.Char(string="Diario Contable",compute="_lineas_")
    payment_state = fields.Char(string="Estado de pago",compute="_lineas_" )
    fecha_cargo = fields.Date(string='Fecha', readonly=True)
    tipo = fields.Char(string='Tipo de Cargo', readonly=True)
    mes = fields.Integer(string='Mes', readonly=True, default=0)
    anio = fields.Integer(string='Mes', readonly=True, default=0)


    def _lineas_(self):
        for linea in self:
            cargo = self.env['account.move'].search([('id', '=', linea.cargo_id.id)])
            linea.diario = cargo.journal_id.name
            linea.monto = cargo.amount_total_signed
            linea.fecha_cargo = cargo.create_date

            if cargo.state == 'draft':
                linea.state = 'Borrador'
            elif cargo.state == 'posted':
                linea.state = 'Publicado'
            else:
                linea.state = 'Cancelado'

            if cargo.payment_state == 'not_paid':
                linea.payment_state = 'No pagadas'
            elif cargo.payment_state == 'in_payment':
                linea.payment_state = 'En proceso de pago'
            elif cargo.payment_state == 'paid':
                linea.payment_state = 'Pagado'
            elif cargo.payment_state == 'partial':
                linea.payment_state = 'Pagado Parcialmente'
            elif cargo.payment_state == 'reversed':
                linea.payment_state = 'Revertido'
            elif cargo.payment_state == 'invoincing_legacy':
                linea.payment_state = 'Factura Sistema Anterior'






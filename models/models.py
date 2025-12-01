# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date


class autoescuela(models.Model):
    _name = 'autoescuela.autoescuela'
    _description = 'Autoescuela'

    name = fields.Char(string="Nombre", required=True)
    domicilio = fields.Char(string="Domicilio")
    localidad = fields.Char(string="Localidad")
    provincia = fields.Char(string="Provincia")
    contacto = fields.Char(string="Contacto")

    # Relaciónes
    examen_ids = fields.Many2many('autoescuela.examen', string="Exámenes")
    profesor_ids = fields.One2many('autoescuela.profesor', 'autoescuela_id', string="Profesores")
    alumno_ids = fields.One2many('autoescuela.alumno', 'autoescuela_id', string="Alumnos")

     # Contadores
    alumnos_count = fields.Integer(string="Número de alumnos", compute='_compute_counts')
    profesores_count = fields.Integer(string="Número de profesores", compute='_compute_counts')


    @api.depends('alumnos_ids', 'profesor_ids')
    def _compute_counts(self):
         for record in self:
           record.alumnos_count = len(record.alumno_ids)
           record.profesores_count = len(record.profesores_ids)

class Profesor(models.Model):
    _name = 'autoescuela.profesor'
    _description = 'Profesor de la Autoescuela'

    name = fields.Char(string="Nombre", required=True)
    dni = fields.Char(string="DNI", required=True)
    coche = fields.Char(string="Coche")
    autoescuela_id = fields.Many2one('autoescuela.autoescuela', string="Autoescuela")
    incorporacion = fields.Date(string="Fecha de incorporación")
    antiguedad = fields.Integer(string="Antigüedad (años)", compute='_compute_antiguedad')
    alumnos_ids = fields.One2many('autoescuela.alumno', 'profesor_id', string="Alumno")

    @api.depends('incorporacion')
    def _compute_antiguedad(self):
         for rec in self:
            if rec.incorporacion:
                hoy = date.today()
                rec.antiguedad = hoy.year - rec.incorporacion.year - ((hoy.month, hoy.day) < (rec.incorporacion.month, rec.incorporacion.day))
            else:
                rec.antiguedad = 0

class Alumno(models.Model):
    _name = 'autoescuela.alumno'
    _description = 'Alumno de la Autoescuela'

    name = fields.Char(string="Nombre", required=True)
    dni = fields.Char(string="DNI", required=True)
    autoescuela_id = fields.Many2one('autoescuela.autoescuela', string="Autoescuela")
    profesor_id = fields.Many2one('autoescuela.profesor', 'alumno_id', string="Profesor asignado")
    examen_ids = fields.One2many('autoescuela.examen', 'alumno_id', string="Exámenes")
    domicilio = fields.Date(string="Domicilio")
    matricula = fields.Integer(string="Matrícula")
    fecha_nacimiento = fields.Date(string="Fecha de nacimiento")
    numero_practicas = fields.Integer(string="Prácticas Realizadas", default = 0)
    aprobado_teorico = fields.Boolean(string="Aprobado Teórico")
    aprobado_practico = fields.Boolean(string="Aprobado Práctico")
    _sql_constraints = [('dni_uniq', 'unique(dni)', 'Ya existe un alumno con ese DNI.')]

class Examen(models.Model):
    _name = 'autoescuela.examen'
    _description = 'Examen de la autoescuela'
    _order = 'fecha desc, id desc'

    name = fields.Char(string="Referencia", required=True, copy=False,
                       default=lambda self: self.env['ir.sequence'].next_by_code('autoescuela.examen') if self.env['ir.sequence'].search([('code', '=', 'autoescuela.examen')]) else '/')
    fecha = fields.Date(string="Fecha")
    autoescuela_ids = fields.Many2many('autoescuela.autoescuela', string="Autoescuelas")
    alumno_id = fields.Many2one('autoescuela.alumno', string="Alumno", required=True, ondelete='cascade')
    moneda_id = fields.Many2one('res.currency', string="Moneda")
    precio = fields.Monetary(string="Precio", currency_field='moneda_id')
    clases = fields.Integer(string="Número de clases")
    carnet = fields.Char(string="Carnet (tipo)")

    estado = fields.Selection([
        ('programado','Programado'),
        ('presentado','Presentado'),
        ('aprobado','Aprobado'),
        ('suspendido','Suspendido')
    ], string="Estado", default='programado')

    @api.constrains('clases')
    def _check_clases(self):
        for rec in self:
            if rec.clases and rec.clases < 0:
                raise ValidationError("El número de clases no puede ser negativo.")
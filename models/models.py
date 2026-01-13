# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date


class Autoescuela(models.Model):
    _name = 'autoescuela.autoescuela'
    _description = 'Autoescuela'

    name = fields.Char(string="Nombre", required=True)
    domicilio = fields.Char(string="Domicilio")
    localidad = fields.Char(string="Localidad")
    provincia = fields.Char(string="Provincia")
    contacto = fields.Char(string="Contacto")

    profesor_ids = fields.One2many(
        'autoescuela.profesor',
        'autoescuela_id',
        string="Profesores"
    )

    alumno_ids = fields.One2many(
        'autoescuela.alumno',
        'autoescuela_id',
        string="Alumnos"
    )

    examen_ids = fields.Many2many(
        'autoescuela.examen',
        string="Exámenes"
    )

    alumnos_count = fields.Integer(
        compute='_compute_counts',
        string="Número de alumnos"
    )

    profesores_count = fields.Integer(
        compute='_compute_counts',
        string="Número de profesores"
    )

    @api.depends('alumno_ids', 'profesor_ids')
    def _compute_counts(self):
        for record in self:
            record.alumnos_count = len(record.alumno_ids)
            record.profesores_count = len(record.profesor_ids)


class Profesor(models.Model):
    _name = 'autoescuela.profesor'
    _description = 'Profesor'

    name = fields.Char(string="Nombre", required=True)
    dni = fields.Char(string="DNI", required=True)
    coche = fields.Char(string="Coche")

    autoescuela_id = fields.Many2one(
        'autoescuela.autoescuela',
        string="Autoescuela"
    )

    incorporacion = fields.Date(string="Fecha de incorporación")

    antiguedad = fields.Integer(
        compute='_compute_antiguedad',
        string="Antigüedad (años)"
    )

    alumno_ids = fields.One2many(
        'autoescuela.alumno',
        'profesor_id',
        string="Alumnos"
    )

    @api.depends('incorporacion')
    def _compute_antiguedad(self):
        for rec in self:
            if rec.incorporacion:
                hoy = date.today()
                rec.antiguedad = hoy.year - rec.incorporacion.year - (
                    (hoy.month, hoy.day) < (rec.incorporacion.month, rec.incorporacion.day)
                )
            else:
                rec.antiguedad = 0


class Alumno(models.Model):
    _name = 'autoescuela.alumno'
    _description = 'Alumno'

    name = fields.Char(string="Nombre", required=True)
    dni = fields.Char(string="DNI", required=True)

    autoescuela_id = fields.Many2one(
        'autoescuela.autoescuela',
        string="Autoescuela"
    )

    profesor_id = fields.Many2one(
        'autoescuela.profesor',
        string="Profesor asignado"
    )

    examen_ids = fields.One2many(
        'autoescuela.examen',
        'alumno_id',
        string="Exámenes"
    )

    domicilio = fields.Char(string="Domicilio")
    matricula = fields.Integer(string="Matrícula")
    fecha_nacimiento = fields.Date(string="Fecha de nacimiento")
    numero_practicas = fields.Integer(default=0, string="Prácticas realizadas")
    aprobado_teorico = fields.Boolean(string="Aprobado teórico")
    aprobado_practico = fields.Boolean(string="Aprobado práctico")

    _sql_constraints = [
        ('dni_unique', 'unique(dni)', 'Ya existe un alumno con ese DNI.')
    ]


class Examen(models.Model):
    _name = 'autoescuela.examen'
    _description = 'Examen'
    _order = 'fecha desc, id desc'

    name = fields.Char(
        required=True,
        copy=False,
        default=lambda self: self.env['ir.sequence'].next_by_code('autoescuela.examen') or '/'
    )

    fecha = fields.Date(string="Fecha")

    alumno_id = fields.Many2one(
        'autoescuela.alumno',
        string="Alumno",
        required=True,
        ondelete='cascade'
    )

    autoescuela_ids = fields.Many2many(
        'autoescuela.autoescuela',
        string="Autoescuelas"
    )

    moneda_id = fields.Many2one('res.currency', string="Moneda")
    precio = fields.Monetary(currency_field='moneda_id', string="Precio")
    clases = fields.Integer(string="Número de clases")
    carnet = fields.Char(string="Carnet")

    estado = fields.Selection(
        [
            ('programado', 'Programado'),
            ('presentado', 'Presentado'),
            ('aprobado', 'Aprobado'),
            ('suspendido', 'Suspendido'),
        ],
        default='programado',
        string="Estado"
    )

    @api.constrains('clases')
    def _check_clases(self):
        for rec in self:
            if rec.clases is not None and rec.clases < 0:
                raise ValidationError("El número de clases no puede ser negativo.")

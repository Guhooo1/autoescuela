# -*- coding: utf-8 -*-
{
    'name': "Autoescuela",
    'summary': "Gestión de autoescuelas",
    'description': """ 
        Módulo completo para la gestión integral de autoescuelas:
        - Autoescuelas, profesores y alumnos
        - Gestión de exámenes teóricos/prácticos
        - Estadísticas y reportes
        - Calendario de exámenes
    """,
    'author': "Sergio, Juan y Hugo",
    'category': 'Education',
    'version': '1.0.0',
    'depends': ['base'],
    'application': True,

    'data': [
        'security/autoescuela_groups.xml',
        'security/ir.model.access.csv',
        'data/autoescuela_sequence.xml',  
        'views/autoescuela_autoescuela_view.xml',
        'views/autoescuela_profesor_view.xml',
        'views/autoescuela_alumno_view.xml',
        'views/autoescuela_examen_view.xml',
        'views/autoescuela_menus.xml',
        'reports/alumno_report.xml',
        'reports/report_templates.xml',
        'reports/examen_report.xml',
        'reports/profesor_report.xml',
    ],

    'demo': [
        'demo/demo.xml',
    ],
    
   'installable': True,
}
# -*- coding: utf-8 -*-
{
    'name': "autoescuela",

    'summary': "Gestion de autoescuelas",

    'description': """
        Modulo para la gestion de autoescuelas 
    """,

    'author': "Sergio, Juan y Hugo",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'education',
    'version': '0.1',
    'application': 'True'

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/autoescuela_groups.xml'
        'views/views.xml',
        'views/autoescuela_alumno_view.xml',
        'views/autoescuela_autoescuela_view.xml',
        'views/autoescuela_examen_view.xml',
        'views/autoescuela_menus.xml',
        'views/autoescuela_profesor_view.xml'
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}


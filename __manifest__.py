{
    'name': "Autoescuela",
    'summary': "Gestión de autoescuelas",
    'description': "Módulo para la gestión de autoescuelas",
    'author': "Sergio, Juan y Hugo",
    'category': 'Education',
    'version': '1.0',
    'depends': ['base'],
    'application': True,

    'data': [
        'security/ir.model.access.csv',
        'security/autoescuela_groups.xml',

        'views/autoescuela_autoescuela_view.xml',
        'views/autoescuela_profesor_view.xml',
        'views/autoescuela_alumno_view.xml',
        'views/autoescuela_examen_view.xml',
        'views/autoescuela_menus.xml',
    ],
}


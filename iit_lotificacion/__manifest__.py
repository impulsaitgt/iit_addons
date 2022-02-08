# -*- coding: utf-8 -*-
{
    'name' : 'Especializacion Lotificacion ',
    'summary':"""
        Especializacion Lotificacion
    """,
    'author':'Alexander Paiz/Lester Paiz',
    'category': 'General',
    'version' : '1.0.0',
    'depends': [
        "account"
    ],
    'data': [
        'security/lotificacion_security.xml',
        'security/ir.model.access.csv',
        'views/menu_view.xml',
        'views/inmueble_view.xml',
        'views/mora_view.xml',
        'views/cotizador_view.xml',
        'views/sequences.xml'
    ]
}
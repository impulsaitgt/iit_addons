# -*- coding: utf-8 -*-
{
    'name' : 'Pruebas Impulsa IT',
    'summary':"""
        Primeras pruebas de Impulsa IT en Odoo
    """,
    'author':'Alexander Paiz',
    'category': 'General',
    'version' : '1.0.0',
    'depends': [
        "sale",
        "mail",
        "account"
    ],
    'data': [
        'views/menu_view.xml',
        'views/libros_view.xml',
        'views/sale.xml',
        'security/libreria_security.xml',
        'security/ir.model.access.csv',
        'report/libros.xml',
        'report/detalle_libro.xml'
    ]
}
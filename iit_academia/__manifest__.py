# -*- coding: utf-8 -*-
{
    'name' : 'Especializacion Academia ',
    'summary':"""
        Especializacion Academia
    """,
    'author':'Lester Paiz',
    'category': 'General',
    'version' : '1.0.0',
    'depends': [
        "account",
        "mail"
    ],
    'data': [
        'security/academia_security.xml',
        'security/ir.model.access.csv',
        'views/menu_view.xml',
        'views/estudiante_view.xml',
        'views/contrato_view.xml',
        'views/torneo_view.xml',
        'views/cargo_estudiante_view.xml',
        'views/account_journal_view.xml',
        'views/account_move_view.xml',
        'views/product_template_view.xml',
        'views/sequences.xml',
        'report/report.xml',
        'report/contrato_template.xml',
        'report/torneo_template.xml'
    ]
}
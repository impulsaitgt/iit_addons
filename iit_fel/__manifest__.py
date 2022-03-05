# -*- coding: utf-8 -*-
{
    'name' : 'Factura Electronica Impulsa IT',
    'summary':"""
        Implementacion Factura Electronica FEL con Infile
    """,
    'author':'Alexander Paiz',
    'category': 'General',
    'version' : '1.0.0',
    'depends': [
        "account",
        "account_debit_note"
    ],
    'data': [
        "views/account_move.xml",
        "views/res_partner.xml",
        "views/res_company.xml"
    ]
}
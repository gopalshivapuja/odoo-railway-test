{
    'name': 'MOAR Backend Brand',
    'description': 'Applies MOAR Advisory branding to the Odoo backend interface',
    'category': 'Hidden/Tools',
    'version': '19.0.1.0.0',
    'author': 'MOAR Advisory',
    'license': 'LGPL-3',
    'depends': ['web'],
    'data': [
        'views/webclient_templates.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            ('prepend',
             'moar_backend_brand/static/src/scss/primary_variables.scss'),
        ],
        'web._assets_bootstrap': [
            'moar_backend_brand/static/src/scss/bootstrap_overridden.scss',
        ],
        'web.assets_backend': [
            'moar_backend_brand/static/src/scss/backend_theme.scss',
        ],
        'web.assets_frontend': [
            'moar_backend_brand/static/src/scss/login.scss',
        ],
    },
}

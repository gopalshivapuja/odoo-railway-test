{
    'name': 'MOAR Advisory Theme',
    'description': 'Custom theme for MOAR Advisory website — matches moaradvisory.com',
    'category': 'Website/Theme',
    'version': '19.0.1.0.0',
    'author': 'MOAR Advisory',
    'license': 'LGPL-3',
    'depends': ['website'],
    'data': [
        'data/presets.xml',
        'views/website_templates.xml',
        'views/snippets.xml',
        'views/pages.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            ('prepend', 'theme_moar_advisory/static/src/scss/primary_variables.scss'),
        ],
        'web._assets_frontend_helpers': [
            ('prepend', 'theme_moar_advisory/static/src/scss/bootstrap_overridden.scss'),
        ],
        'web.assets_frontend': [
            'theme_moar_advisory/static/src/scss/theme.scss',
        ],
    },
}

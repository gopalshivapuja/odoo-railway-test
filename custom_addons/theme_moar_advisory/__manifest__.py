{
    'name': 'MOAR Advisory Theme',
    'description': 'Custom theme for MOAR Advisory website — matches moaradvisory.com',
    'category': 'Website',
    'version': '19.0.1.0.0',
    'author': 'MOAR Advisory',
    'license': 'LGPL-3',
    'depends': ['website'],
    'data': [
        'views/website_templates.xml',
        'views/snippets.xml',
        'views/pages.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'theme_moar_advisory/static/src/scss/theme.scss',
            'theme_moar_advisory/static/src/js/header_social.js',
        ],
    },
}

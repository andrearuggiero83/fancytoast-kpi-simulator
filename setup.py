from setuptools import setup

APP = ['fancytoast_kpi_app.py']
DATA_FILES = ['LOGO_Fancytoast.png']
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'Fancytoast_Logo.icns',
    'packages': ['pandas']
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)

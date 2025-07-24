from setuptools import setup

APP = ['sudoku_printer.py']  # your main script here
OPTIONS = {
    'argv_emulation': True,
    'packages': ['reportlab'],  # any extra packages you use
}

setup(
    app=APP,              # <--- this is required by py2app
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
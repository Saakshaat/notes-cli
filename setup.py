from setuptools import setup

setup(
    name='notes',
    version='1.0.0',
    py_modules=['notes'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        notes=notes:cli
    ''',
)

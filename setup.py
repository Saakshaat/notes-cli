from setuptools import setup

setup(
    name='notes',
    version='0.1',
    py_modules=['notes'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        notes=notes:cli
    ''',
)

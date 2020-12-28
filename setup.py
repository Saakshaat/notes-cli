import pathlib

from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='py-notes',
    version='1.0.0',
    description="Take notes directly in your terminal.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Saakshaat/notes-cli/",
    author="Saakshaat Singh",
    author_email="saakshaat2001@gmail.com",
    license="MIT",
    keywords = ['cli', 'notes', 'terminal'],
    py_modules=['notes'],
    include_package_data=True,
    install_requires=[
        'Click'
    ],
    entry_points='''
        [console_scripts]
        notes=notes:cli
    ''',
)

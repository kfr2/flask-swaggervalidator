"""
Flask-SwaggerValidator
-----------------------

Validate Flask Requests and Responses against Swagger (OpenAPI Specification)
specification files.
"""
from setuptools import setup

setup(
    name='Flask-SwaggerValidator',
    version='0.0.1',
    url='',
    license='ISC',
    author='Kevin Richardson',
    author_email='kevin@kevinrichardson.co',
    description='',
    long_description=__doc__,
    packages=['flask_swaggervalidator'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'bravado_core',
        'flask'
    ],
    classifiers=[
    ]
)

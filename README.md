# Flask-SwaggerValidator

[![Build Status](https://travis-ci.org/kfr2/flask-swaggervalidator.svg?branch=add-travis)](https://travis-ci.org/kfr2/flask-swaggervalidator)

This project exposes a couple of decorators that can be used to validate
a Flask Request or Response based on an operation within a Swagger (OpenAPI Specification)
specification file. It currently uses bravado-core for this validation. Note that this
project is in the very early stages of development and its interfaces are likely to change
substantially.

## Documentation

Documentation is available on [Read the Docs](http://flask-swaggervalidator.rtfd.io/).

## Running tests

Tests can be invoked through either `python setup.py test` or `nosetests`. In either
case, [nose](http://nose.readthedocs.io/en/latest/) must be in the environment.

## To Do

Although bravado-core is a nice library, these Swagger validation libraries should be
examined to see if they offer any additional benefits. For example, I'd like the library
to validate that all attributes in a response body are listed in the specification file.

* https://pypi.python.org/pypi/flex
* https://pypi.python.org/pypi/swagger-spec-validator

# Flask-SwaggerValidator

This project exposes a couple of decorators that can be used to validate
a Flask Request or Response based on an operation within a Swagger (OpenAPI Specification)
specification file. It currently uses bravado-core for this validation. Note that this
project is in the very early stages of development and its interfaces are likely to change
substantially.

## decorators

* decorators.validate_swagger_request(operation_id, swagger_spec_path='swagger.yaml')
* decorators.validate_swagger_response(operation_id, swagger_spec_path='swagger.yaml')

## To Do
These Swagger validation libraries should be examined:
* https://pypi.python.org/pypi/flex
* https://pypi.python.org/pypi/swagger-spec-validator

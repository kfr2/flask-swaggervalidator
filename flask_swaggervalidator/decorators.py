# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
import os
from functools import wraps

import flask

from swagger_validator import SwaggerValidator


_FLASK_DEBUG_VARIABLE = 'FLASK_DEBUG'


def _validate_flask_request(request, swagger_spec_path, operation_id):
    """
    Args:
        request (flask.Request): Flask request to validate.
        swagger_spec_path (string): The path to the Swagger specification file.
        operation_id (string): The name of the operation the request should be
            validated against.


    Returns:
        None

    Raises:
        TODO
    """
    validator = SwaggerValidator(swagger_spec_path)
    validator.validate_request(request, operation_id)


def _validate_flask_response(response, swagger_spec_path, operation_id):
    """
    Validate a Flask Response against a particular Swagger spec operation.

    Args:
        response (flask.Response): The Flask response to validate.
        swagger_spec_path (string): The path to the Swagger specification file.
        operation_id (string): The name of the operation the response should be
            validated against.

    Returns:
        None

    Raises:
        swagger_spec_validator.common.SwaggerValidationError: The Swagger spec did not validate.
            Note: Ensure you are wrapping response codes in quotes (ex: "200")
        jsonschema.exceptions.ValidationError: The response did not meet the specification.
    """
    validator = SwaggerValidator(swagger_spec_path)
    status_code = response.status_code
    body_text = response.data
    content_type = response.content_type
    validator.validate_response(operation_id, status_code, body_text, content_type)


def validate_swagger_request(operation_id, swagger_spec_path='swagger.yaml', debug_only=False):
    """
    Wrap a view function and raise an exception if the request does not conform
    to that which is defined in the Swagger specification file.

    For example, the request may contain an inappropriate content-type
    or could be missing a required parameter.

    Args:
        operation_id (string): The name of the operation the response should be
            validated against.
        swagger_spec_path (string): The path to the Swagger specification file.
        debug_only (boolean): Only validate the request if Flask is in debug mode.

    Returns:
        return value from decorated view function
        HTTP 400 if the request does not validate.

    Raises:
        bravado_core.exception.SwaggerMappingError: required values are not present
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            logging.debug('validate_swagger_request() was called.')
            if debug_only and os.environ.get(_FLASK_DEBUG_VARIABLE):
                _validate_flask_request(flask.request, swagger_spec_path, operation_id)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def validate_swagger_response(operation_id, swagger_spec_path='swagger.yaml', debug_only=False):
    """
    Wrap a view function and return a subclass of ValidationError if its
    response does not conform to the specified operation_id (or if the
    Swagger spec file is invalid for some reason.)

    Args:
        operation_id (string): The name of the operation the response should be
            validated against.
        swagger_spec_path (string): The path to the Swagger specification file.
        debug_only (boolean): Only validate the request if Flask is in debug mode.

    Returns:
        return value from decorated view function

    Raises:
        swagger_spec_validator.common.SwaggerValidationError: The Swagger spec did not validate.
            Note: Ensure you are wrapping response codes in quotes (ex: "200")
        jsonschema.exceptions.ValidationError: The response did not meet the specification.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            logging.debug('validate_swagger_response() was called.')
            resp = f(*args, **kwargs)
            if debug_only and os.environ.get(_FLASK_DEBUG_VARIABLE):
                _validate_flask_response(resp, swagger_spec_path, operation_id)
            return resp
        return decorated_function
    return decorator

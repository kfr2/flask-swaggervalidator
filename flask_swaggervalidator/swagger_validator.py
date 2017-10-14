# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import logging


import yaml
import bravado_core.request
import bravado_core.response
from bravado_core.spec import Spec


DEFAULT_SWAGGER_FILE = 'swagger.yaml'
_swagger_spec_cache = {}


class SpecValidationException(Exception):
    """Generic validation exception from this module."""


class SpecOperationValidationException(SpecValidationException):
    """Raise when desired operation cannot be located."""


class BodyTextValidationError(SpecValidationException):
    """Raise when body_text is an invalid data structure."""


class Request(object):
    """Coerce a Flask request into a bravado_core.request.IncomingRequest."""
    @classmethod
    def from_flask_request(self, request):
        req = bravado_core.request.IncomingRequest()
        req.path = request.path
        req.query = request.args
        req.form = request.form
        req.headers = request.headers
        req.files = request.files
        return req


class JSONOutgoingResponse(bravado_core.response.OutgoingResponse):
    def __init__(self, *args, **kwargs):
        for kwarg in kwargs:
            setattr(self, kwarg, kwargs[kwarg])

    def json(self, **kwargs):
        if isinstance(self.text, str):
            return json.loads(self.text)
        if isinstance(self.text, dict):
            return self.text
        if isinstance(self.text, list):
            return self.text
        raise BodyTextValidationError(
            'body_text should be passed as a JSON string, dictionary, or list.')


class SwaggerValidator(object):
    def __init__(self, swagger_file=DEFAULT_SWAGGER_FILE, lazy_load=False):
        self.swagger_file = swagger_file
        self.operations = None
        if not lazy_load:
            self.load_swagger_spec()

    def load_swagger_spec(self):
        """Load the swagger file into a bravado_core.spec.Spec object."""
        if self.swagger_file not in _swagger_spec_cache:
            logging.debug('Loading Swagger spec file {}'.format(self.swagger_file))
            with open(self.swagger_file, 'r') as f:
                spec_dict = yaml.load(f)
                config = {
                    'validate_swagger_spec': True,
                    'validate_requests': False,
                    'use_models': False
                }
                swagger_spec = Spec.from_dict(spec_dict, config=config)
                _swagger_spec_cache[self.swagger_file] = swagger_spec
        return _swagger_spec_cache[self.swagger_file]

    def load_operations(self):
        """
        Load all the operations contained within the Swagger file into a
        dictionary of operationId -> bravado_core.operation.Operation object.
        """
        swagger_spec = self.load_swagger_spec()
        if self.operations is None:
            ops = {}
            resources = swagger_spec.resources.values()
            for resource in resources:
                for op in resource.operations.values():
                    ops[op.operation_id] = op
            self.operations = ops
        return self.operations

    def operation_from_operation_id(self, operation_id):
        """
        Look up and return a bravado_core.operation.Operation object based on
        its operation_id. Return None if one cannot be located.
        """
        op_key = operation_id.replace('.', '_')
        operation = self.operations.get(op_key)
        if operation is None:
            msg = 'An operation with operationId {} cannot be located.'.format(
                operation_id)
            raise SpecOperationValidationException(msg)
        return operation

    def operation_response_spec(self, operation, status_code):
        """
        Return the response_spec for the operation for a particular status_code.
        Raise bravado_core.exception.MatchingResponseNotFound if it cannot be
        located.
        """
        return bravado_core.response.get_response_spec(
            str(status_code), operation)

    def validate_request(self, request, operation_id):
        """
        Validate a request against the expected request for the operation
        with operation_id in the Swagger specification file.

        Args:
            request (flask.Request): The Flask request to validate
            operation_id (string): The operation whose parameters to validate
                the request.

        Raises:
            bravado_core.exception.SwaggerMappingError:
        """
        req = Request.from_flask_request(request)
        self.load_operations()
        operation = self.operation_from_operation_id(operation_id)
        bravado_core.request.unmarshal_request(req, operation)

    def validate_response(self, operation_id, status_code, body_text,
                          content_type='application/json'):
        """
        Validate a response body against the expected response for the operation
        with operation_id and status_code combination in the swagger file.

        :type operation_id: str
        :type status_code: str
        :type body_text: JSON str or dict
        :type content_type: str
        :type swagger_file: str

        :returns: None if the the validation is successful. Otherwise, a
            `json.exceptions.ValidationError` will be raised.
        """
        self.load_operations()
        operation = self.operation_from_operation_id(operation_id)
        resp_spec = self.operation_response_spec(operation, status_code)
        resp = JSONOutgoingResponse(
            text=body_text, content_type=content_type, headers={})
        bravado_core.response.validate_response(resp_spec, operation, resp)

    def validate_response_body(self):
        # TODO: In the future, we may only care about the body contents. If so,
        # we could use...
        # bravado_core.response.validate_response_body(operation, resp_spec, resp)
        raise NotImplementedError

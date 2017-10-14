# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import os
import unittest

from bravado_core.exception import MatchingResponseNotFound, SwaggerMappingError
from jsonschema.exceptions import ValidationError
from swagger_spec_validator.common import SwaggerValidationError

from flask_swaggervalidator import swagger_validator


THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class SwaggerValidatorTestCase(unittest.TestCase):
    """Tests for swagger_validator.SwaggerValidator"""
    def load_valid_spec_file(self):
        self.v = swagger_validator.SwaggerValidator(os.path.join(THIS_DIR, 'data/swagger.yaml'))

    def test_load_unknown_file(self):
        with self.assertRaises(IOError):
            swagger_validator.SwaggerValidator(os.path.join(THIS_DIR, 'dunno.yaml'))

    def test_load_nonyaml_file(self):
        with self.assertRaises(SwaggerValidationError):
            swagger_validator.SwaggerValidator(os.path.join(THIS_DIR, 'data/notyaml.txt'))

    def test_load_nonswagger_yaml_file(self):
        with self.assertRaises(SwaggerValidationError):
            swagger_validator.SwaggerValidator(os.path.join(THIS_DIR, 'data/notswagger.yaml'))

    def test_operation_can_be_retrieved_by_name(self):
        self.load_valid_spec_file()
        self.v.load_operations()
        op = self.v.operation_from_operation_id('api.views.listSubjects')
        self.assertIsNotNone(op)

    def test_unknown_operation(self):
        self.load_valid_spec_file()
        self.v.load_operations()
        with self.assertRaises(swagger_validator.SpecOperationValidationException):
            self.v.operation_from_operation_id('dunno')

    def test_known_operation_status_code(self):
        self.load_valid_spec_file()
        self.v.load_operations()
        op = self.v.operation_from_operation_id('api.views.listSubjects')
        resp_spec = self.v.operation_response_spec(op, 200)
        self.assertIsNotNone(resp_spec)

    def test_unknown_operation_status_code(self):
        self.load_valid_spec_file()
        self.v.load_operations()
        op = self.v.operation_from_operation_id('api.views.listSubjects')
        with self.assertRaises(MatchingResponseNotFound):
            self.v.operation_response_spec(op, 123)

    def test_valid_response_as_dict(self):
        self.load_valid_spec_file()
        body_text = {
            'id': '123',
            'name': 'dunno'
        }
        self.v.validate_response('api.views.fetchSubject', 200, body_text)

    def test_valid_response_as_list(self):
        self.load_valid_spec_file()
        body_text = [{'id': '123', 'name': 'dunno'}]
        self.v.validate_response('api.views.listSubjects', 200, body_text)

    def test_valid_response_as_text(self):
        self.load_valid_spec_file()
        body_text = json.dumps({
            'id': '123',
            'name': 'dunno',
            'notes': 'optional things are okay too'
        })
        self.v.validate_response('api.views.fetchSubject', 200, body_text)

    def test_extraneous_fields_are_okay(self):
        self.load_valid_spec_file()
        body_text = {
            'id': '123',
            'name': 'dunno',
            'otherfield': 'this is fine too'
        }
        self.v.validate_response('api.views.fetchSubject', 200, body_text)

    def test_invalid_body(self):
        self.load_valid_spec_file()
        body_text = {
            'invalid': 'huzzah'
        }
        with self.assertRaises(ValidationError):
            self.v.validate_response('api.views.fetchSubject', 200, body_text)

    def test_invalid_type(self):
        self.load_valid_spec_file()
        body_text = {
            'id': 123,
            'name': 'dunno'
        }
        with self.assertRaises(ValidationError):
            self.v.validate_response('api.views.fetchSubject', 200, body_text)

    def test_invalid_content_type(self):
        self.load_valid_spec_file()
        body_text = {
            'id': '123',
            'name': 'dunno'
        }
        with self.assertRaises(SwaggerMappingError):
            self.v.validate_response('api.views.fetchSubject', 200, body_text,
                                     content_type='application/xml')

    def test_valid_request(self):
        self.load_valid_spec_file()


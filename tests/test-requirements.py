#!/usr/bin/env python3

import pytest
import json
import re
import multiplex

class TestRequirements:

    requirements_json = "tests/JSON/requirements-good.json"
    req_presets_empty = "tests/JSON/requirements-presets-empty-good.json"

    """Common function to load requirements"""
    @pytest.fixture(scope="function")
    def load_req(self, request):
        req_json = multiplex.load_json_file(request.param)
        return(req_json)

    """Common function to validate param"""
    @pytest.fixture(scope="function")
    def validate_param(self, request):
        multiplex.log = multiplex.logging.getLogger()
        multiplex.validation_dict = { "duration": "^[1-9]+[0-9]*$" }
        validated = multiplex.param_validated(next(iter(multiplex.validation_dict)), request.param)
        return(validated)

    """Test if requirements json file is successfully loaded"""
    @pytest.mark.parametrize("load_req", [ requirements_json ], indirect=True)
    def test_load_requirements(self, load_req):

        assert load_req is not None
        assert 'presets' in load_req

    """Test if validation dict is successfully created"""
    @pytest.mark.parametrize("load_req", [ requirements_json ], indirect=True)
    def test_create_validation_dict(self, load_req):
        multiplex.create_validation_dict(load_req)

        assert multiplex.validation_dict is not {}
        assert 'bs' in multiplex.validation_dict.keys()

    """Test if validation dict has empty presets (which is ok)"""
    @pytest.mark.parametrize("load_req", [ req_presets_empty ], indirect=True)
    def test_empty_presets(self, load_req):
        multiplex.create_validation_dict(load_req)

        assert multiplex.validation_dict is not {}
        assert load_req['presets'] == {}

    """Test invalid vals"""
    @pytest.mark.parametrize("validate_param", [ "bar", "012", "60s" ], indirect=True)
    def test_invalid_val(self, validate_param):
        assert validate_param is False

    """Test valid vals"""
    @pytest.mark.parametrize("validate_param", [ "60", "1", "3600" ], indirect=True)
    def test_valid_val(self, validate_param):
        assert validate_param is True

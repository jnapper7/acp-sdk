test:
	@poetry run pytest --exitfirst -q tests/test_manifest_validator.py::test_manifest_validator
	@poetry run pytest --exitfirst -q tests/test_manifest_validator.py::test_oas_generator
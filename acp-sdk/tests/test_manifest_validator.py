# SPDX-FileCopyrightText: Copyright (c) 2025 Cisco and/or its affiliates.
# SPDX-License-Identifier: Apache-2.0
import os
import pytest
from acp_sdk.manifest.validator import validate_manifest_file
from acp_sdk.manifest.generator import generate_agent_oapi
from openapi_spec_validator.readers import read_from_filename
from deepdiff import diff


@pytest.mark.parametrize(
    "test_filename, test_success, error_message",
    [
        ("manifest_ok.json", True, ""),
        ("manifest_ko.json", False, ""),
        ("manifest_thread_support_ko.json", False,
         "Cannot define `specs.thread_state` if `specs.capabilities.threads` is `false`"),
        ("manifest_no_interrupts_ko.json", False, "Interrupts defined with `spec.capabilities.interrupts=false`")
    ],
)
def test_manifest_validator(test_filename, test_success, error_message):
    curpwd = os.path.dirname(os.path.realpath(__file__))
    fullpath = os.path.join(curpwd, "sample_manifests", test_filename)
    try:
        validate_manifest_file(fullpath)
        assert (test_success)
    except Exception as e:
        assert (not test_success)
        assert (error_message in str(e))


@pytest.mark.parametrize(
    "test_filename, oas_ref_filename",
    [
        ("manifest_ok.json", "oas.manifest_ok.yml"),
    ],
)
def test_oas_generator(test_filename, oas_ref_filename):
    curpwd = os.path.dirname(os.path.realpath(__file__))
    ref_spec, base_uri = read_from_filename(os.path.join(curpwd, "sample_manifests", oas_ref_filename))

    manifest = validate_manifest_file(os.path.join(curpwd, "sample_manifests", test_filename))
    gen_spec = generate_agent_oapi(manifest)
    mapdiff = diff.DeepDiff(gen_spec, ref_spec)
    assert len(mapdiff.affected_paths) == 0

import json

from acp_sdk.models.models import AgentManifest
from .generator import generate_agent_oapi
from .exceptions import ManifestValidationException


def validate_manifest_file(manifest_file_path: str) -> AgentManifest:
    # Load the manifest and validate it
    json_manifest = load_manifest(manifest_file_path)
    return validate_manifest(json_manifest)


def validate_manifest(json_manifest: dict) -> AgentManifest:
    # pydantic validation
    manifest = AgentManifest.model_validate(json_manifest)
    generate_agent_oapi(manifest)
    return manifest


def load_manifest(manifest_file_path: str) -> dict:
    with open(manifest_file_path, "r") as f:
        manifest = json.load(f)
    return manifest
#!bin/sh

docker run --rm \
-v ${PWD}:/local openapitools/openapi-generator-cli generate \
-i local/openapi.yml \
--package-name acp_client \
-g python \
-o local/acp-client
# Agent Connect Protocol SDK

[![Release](https://img.shields.io/github/v/release/agntcy/acp-sdk?display_name=tag)](CHANGELOG.md)
[![Contributor-Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-fbab2c.svg)](CODE_OF_CONDUCT.md)

## About The Project

The "Agent Connect Protocol SDK" is an open-source library designed to facilitate the adoption of the Agent Connect Protocol.
It offers tools for both client and server implementations, enabling seamless integration and communication between multi-agent systems.


## Getting Started

### Clone and update submodules
```sh
git submodule update --init --recursive
```

### Install project dependencies

```sh
cd acp-sdk
poetry install
```

### Generate generic clients and servers
#### Generate generic client 

`make generate_acp_client`

Generate a python client to consume the ACP specification. 
This is a generic client, because schemas for input, output, and configurations are generic objects, i.e. they are not the specific ones supported by a given agent.

To generate a client for a specific agent check the SDK CLI.


#### Generate genericeserver

`make generate_acp_server`

Generate a FastAPI server based on the ACP specification.
This is a generic client, because schemas for input, output, and configurations are generic objects, i.e. they are not the specific ones supported by a given agent.

### ACP SDK CLI

```
cd acp-sdk
poetry run python3 -m acp_sdk --help

Usage: python -m acp_sdk [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  generate-agent-client
  generate-agent-models
  generate-agent-oapi
  validate-manifest
```

## Testing

`make test`


## Roadmap

See the [open issues](https://github.com/agntcy/acp-sdk/issues) for a list of proposed features and known issues.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**. For detailed contributing guidelines, please see [CONTRIBUTING.md](docs/CONTRIBUTING.md).


## Copyright Notice and License

[Copyright Notice and License](./LICENSE)

Copyright (c) 2025 Cisco and/or its affiliates.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


## Acknowledgements

This SDK is developed with the support of the IoA community with the goal of facilitating cross-framework agent interoperability.

# Interrupt Agent

A simple LlamaIndex-based agent which expects human input during its operation.

## Getting Started

```bash
poetry install
python interrupt-li/interrupt.py
```

This sample agent questions the user with 2 simple questions `"How old are you?"` and `"What's your favorite food?"` which the user is expected to answer via CLI

When running with Agent Workflow Server, one can use the `POST /runs/{runId}` endpoint to answer to the Agent:

```sh
  curl -s -H 'content-type: application/json' -H "x-api-key: ${API_KEY}" -d '{"agent_id": "'${AGENT_ID}'", "input": "My favorite food is pizza."}' http://127.0.0.1:${WORKFLOW_SERVER_PORT}/runs/${RUN_ID}
```
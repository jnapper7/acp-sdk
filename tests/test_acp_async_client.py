# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0
import asyncio
import io
from typing import List

from aiohttp import ClientResponse, RequestInfo, StreamReader
from aiohttp.base_protocol import BaseProtocol
from pydantic import BaseModel, RootModel
from yarl import URL

from agntcy_acp import ApiClientConfiguration, AsyncACPClient, AsyncApiClient
from agntcy_acp.models import RunCreateStateless, RunSearchRequest, RunStateless

ListRunStateless = RootModel[List[RunStateless]]

def mock_response_api_client(
    api_client: AsyncApiClient,
    response: BaseModel,
    default_api_key,
    monkeypatch,
):
    class RESTResponseAsync(io.IOBase):
        def __init__(self, status, body: str) -> None:
            cur_loop = asyncio.get_running_loop()
            req_info = RequestInfo(
                URL("http://bogus.org/path/to/bogus"),
                "GET",
                {},
            )
            sse_list = [
                ":this is a test feed\nid: 1\n".encode(),
                "event: agent_event\n".encode(),
            ] + [
                f"data: {line}\n".encode()
                for line in body.splitlines()
            ] + [
                "\n".encode()
            ]
            print(sse_list)

            self.response = ClientResponse(
                req_info.method,
                req_info.url,
                writer=None,
                continue100=None,
                timer=None,
                request_info=req_info,
                traces=[],
                loop=cur_loop,
                session=None,
            )
            stream=StreamReader(
                protocol=BaseProtocol(loop=cur_loop),
                limit=100,
                loop=cur_loop,
            )
            for chunk in sse_list:
                stream.feed_data(chunk)
            stream.feed_eof()

            self.response.content = stream
            self.status = status
            self.reason = None
            self.data = body.encode()

        async def read(self):
            return self.data

        def getheaders(self):
            return {}

        def getheader(self, name, default=None):
            """Returns a given response header."""
            headers = {"content-type": "application/json"}
            return headers.get(name, "bogus")

    # Make sure apis return data
    async def mock_call_api(
        method,
        url,
        header_params=None,
        body=None,
        post_params=None,
        _request_timeout=None,
        response=response,
    ):
        assert header_params is not None
        assert header_params["x-api-key"] == default_api_key
        if hasattr(response, "actual_instance"):
            response = response.actual_instance
        if hasattr(response, "to_json"):
            body = response.to_json()
        else:
            body = response.model_dump_json(by_alias=True, exclude_unset=True)
        
        return RESTResponseAsync(status=200, body=body)

    monkeypatch.setattr(api_client, "call_api", mock_call_api)


async def test_acp_client_stateless_runs_api(default_api_key, default_agent_id, default_run_stateless_response, monkeypatch):
    config = ApiClientConfiguration(retries=2, api_key={"x-api-key": default_api_key})
    run_response = default_run_stateless_response

    async with AsyncACPClient(configuration=config) as client:
        mock_response_api_client(client.api_client, run_response, default_api_key, monkeypatch)

        response = await client.create_stateless_run(run_create_stateless=RunCreateStateless(agent_id=default_agent_id))
        assert response is not None
        assert response.run_id == run_response.run_id
        run_id = response.run_id

        response = await client.get_stateless_run(run_id)
        assert response is not None

        response = await client.wait_for_stateless_run_output(run_id)
        assert response is not None

        response = await client.resume_stateless_run(run_id, {})
        assert response is not None

        list_response = ListRunStateless.model_validate([run_response])
        mock_response_api_client(client.api_client, list_response, default_api_key, monkeypatch)

        response = await client.search_stateless_runs(RunSearchRequest(agent_id=default_agent_id))
        assert response is not None

        mock_response_api_client(client.api_client, run_response, default_api_key, monkeypatch)

        await client.delete_stateless_run(run_id)


async def test_acp_client_stream_stateless_runs_api(default_api_key, default_agent_id, default_run_output_stream, monkeypatch):
    config = ApiClientConfiguration(retries=2, api_key={"x-api-key": default_api_key})

    async with AsyncACPClient(configuration=config) as client:
        mock_response_api_client(client.api_client, default_run_output_stream.data, default_api_key, monkeypatch)
        stream = client.create_and_stream_stateless_run_output(run_create_stateless=RunCreateStateless(agent_id=default_agent_id))
        async for response in stream:
            assert response is not None
            assert response.data.actual_instance.run_id == default_run_output_stream.data.actual_instance.run_id

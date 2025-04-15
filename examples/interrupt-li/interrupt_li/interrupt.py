# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0
import asyncio
from typing import Any

from dotenv import load_dotenv
from llama_index.core.agent.react import ReActChatFormatter, ReActOutputParser
from llama_index.core.llms.llm import LLM
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.tools.types import BaseTool
from llama_index.core.workflow import (
    Context,
    Event,
    HumanResponseEvent,
    InputRequiredEvent,
    StartEvent,
    StopEvent,
    Workflow,
    step,
)

load_dotenv()


class HumanMessage(Event):
    human_answer: str


class FirstEvent(Event):
    ai_answer: str


class SecondEvent(Event):
    ai_answer: str


class ThirdEvent(Event):
    ai_answer: str


class Interrupt(Workflow):
    def __init__(
        self,
        *args: Any,
        llm: LLM | None = None,
        tools: list[BaseTool] | None = None,
        extra_context: str | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.tools = tools or []

        self.llm = llm

        self.memory = ChatMemoryBuffer.from_defaults(llm=llm)
        self.formatter = ReActChatFormatter.from_defaults(context=extra_context or "")
        self.output_parser = ReActOutputParser()
        self.sources = []

    @step
    async def first_step(self, ev: StartEvent) -> FirstEvent:
        print(f"> first_step input: {ev.input}")
        await asyncio.sleep(1)
        return FirstEvent(ai_answer="This is the output of first_step")

    @step
    async def step_interrupt_one(self, ctx: Context, ev: FirstEvent) -> SecondEvent:
        print(f"> step_interrupt_one input : {ev.ai_answer}")
        await asyncio.sleep(1)
        ctx.write_event_to_stream(
            InputRequiredEvent(
                prefix="How old are you?",
            )
        )
        # wait until we see a HumanResponseEvent
        response = await ctx.wait_for_event(HumanResponseEvent)

        return SecondEvent(ai_answer=f"Received human answer: {response.response}")

    @step
    async def step_interrupt_two(self, ctx: Context, ev: SecondEvent) -> ThirdEvent:
        print(f"> step_interrupt_two input : {ev.ai_answer}")
        await asyncio.sleep(1)
        ctx.write_event_to_stream(
            InputRequiredEvent(
                prefix="What's your favorite food?",
            )
        )
        # wait until we see a HumanResponseEvent
        response = await ctx.wait_for_event(HumanResponseEvent)

        return ThirdEvent(ai_answer=f"Received human answer: {response.response}")

    @step
    async def last_step(self, ev: ThirdEvent) -> StopEvent:
        print(f"> last_step input: {ev.ai_answer}")
        await asyncio.sleep(1)
        return StopEvent(result={"ai_answer":"This is the output of last_step"})


def interrupt_workflow() -> Interrupt:
    interrupt_workflow = Interrupt(timeout=300)
    return interrupt_workflow


async def main():
    workflow = interrupt_workflow()

    # print(await workflow.run(email=email_example, target_audience=audience_example))

    handler = workflow.run(input="Hello")

    async for ev in handler.stream_events():
        print(type(ev), ev)
        if isinstance(ev, InputRequiredEvent):
            # capture keyboard input
            response = input(ev.prefix)
            # send our response back
            handler.ctx.send_event(
                HumanResponseEvent(
                    response=response,
                )
            )

    final_result = await handler
    print("Final result: ", final_result)


if __name__ == "__main__":
    asyncio.run(main())

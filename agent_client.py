
import asyncio
from uuid import uuid4

from uagents import Agent, Context, Model


class PriceRequest(Model):
    item: str


class PriceResponse(Model):
    item: str
    prices: str


class AlternativeRequest(Model):
    item: str


class AlternativeResponse(Model):
    item: str
    alternatives: str


PRICE_AGENT_ADDRESS = (
    "agent1qgglacemea2eq79wzvhcuaypu6vxzhwlxaff03uajnpghdu56uc0k84pcjz"
)

ALTERNATIVE_AGENT_ADDRESS = (
    "agent1qdvhtfkysvvcup8y9nrja8rmjxpx0z2rpztzyx2229cv0jqly4z5gh4mt03"
)


async def search_agents(item: str):
    client = Agent(
        name="campuscart_web_client",
        seed="campuscart_web_client_seed_2026",
        port=8003,
        endpoint=["http://127.0.0.1:8003/submit"]
    )

    loop = asyncio.get_running_loop()
    result_future = loop.create_future()
    responses = {}

    @client.on_event("startup")
    async def send_requests(ctx: Context):
        await ctx.send(
            PRICE_AGENT_ADDRESS,
            PriceRequest(item=item)
        )
        await ctx.send(
            ALTERNATIVE_AGENT_ADDRESS,
            AlternativeRequest(item=item)
        )

    @client.on_message(model=PriceResponse)
    async def receive_price(ctx: Context, sender: str, msg: PriceResponse):
        responses["price"] = msg.prices

        if len(responses) == 2 and not result_future.done():
            result_future.set_result(responses)

    @client.on_message(model=AlternativeResponse)
    async def receive_alternative(
        ctx: Context, sender: str, msg: AlternativeResponse
    ):
        responses["alternative"] = msg.alternatives

        if len(responses) == 2 and not result_future.done():
            result_future.set_result(responses)

    async def run_client():
        await client.run_async()

    task = asyncio.create_task(run_client())

    try:
        return await asyncio.wait_for(result_future, timeout=15)
    finally:
        task.cancel()
        await asyncio.gather(task, return_exceptions=True)

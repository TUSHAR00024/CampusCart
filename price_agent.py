
from uagents import Agent, Context, Model


class PriceRequest(Model):
    item: str


class PriceResponse(Model):
    item: str
    prices: str


price_agent = Agent(
    name="price_agent",
    seed="medagent_price_agent_demo_seed_2026",
    port=8001,
    endpoint=["http://127.0.0.1:8001/submit"]
)


item_prices = {
    "notebook": "Store A: Rs 60, Store B: Rs 55, Store C: Rs 65",
    "pen": "Store A: Rs 10, Store B: Rs 8, Store C: Rs 12",
    "sketchbook": "Store A: Rs 120, Store B: Rs 110, Store C: Rs 135"
}


@price_agent.on_query(
    model=PriceRequest,
    replies={PriceResponse}
)
async def handle_request(
    ctx: Context,
    sender: str,
    msg: PriceRequest
):
    name = msg.item.strip().lower()

    prices = item_prices.get(
        name,
        "No sample price data available"
    )

    ctx.logger.info(f"Received request for: {name}")

    await ctx.send(
        sender,
        PriceResponse(
            item=name,
            prices=prices
        )
    )


if __name__ == "__main__":
    price_agent.run()


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


PRICE_AGENT_ADDRESS = "agent1qgglacemea2eq79wzvhcuaypu6vxzhwlxaff03uajnpghdu56uc0k84pcjz"

ALTERNATIVE_AGENT_ADDRESS = "agent1qdvhtfkysvvcup8y9nrja8rmjxpx0z2rpztzyx2229cv0jqly4z5gh4mt03"


orchestrator = Agent(
    name="orchestrator",
    seed="campuscart_orchestrator_seed_2026",
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"]
)


item_name = input(
    "Enter item name (paracetamol/cetirizine/ibuprofen): "
).strip().lower()

price_received = False
alternative_received = False


@orchestrator.on_event("startup")
async def request_data(ctx: Context):
    ctx.logger.info(f"Searching for: {item_name}")

    await ctx.send(
        PRICE_AGENT_ADDRESS,
        PriceRequest(item=item_name)
    )

    await ctx.send(
        ALTERNATIVE_AGENT_ADDRESS,
        AlternativeRequest(item=item_name)
    )


@orchestrator.on_message(model=PriceResponse)
async def handle_price(ctx: Context, sender: str, msg: PriceResponse):
    global price_received
    price_received = True

    ctx.logger.info(f"Item: {msg.item}")

    if msg.prices == "No sample price data available":
        ctx.logger.info("No sample prices found.")
    else:
        ctx.logger.info(f"Sample prices: {msg.prices}")

        price_list = []

        for item in msg.prices.split(","):
            parts = item.strip().split(": Rs ")

            if len(parts) == 2:
                store = parts[0].strip()
                price = float(parts[1].strip())
                price_list.append((price, store))

        if price_list:
            cheapest = min(price_list)
            ctx.logger.info(
                f"Cheapest sample option: {cheapest[1]} "
                f"at Rs {cheapest[0]:g}"
            )

    if price_received and alternative_received:
        ctx.logger.info("Both agents have responded.")


@orchestrator.on_message(model=AlternativeResponse)
async def handle_alternative(
    ctx: Context,
    sender: str,
    msg: AlternativeResponse
):
    global alternative_received
    alternative_received = True

    ctx.logger.info(f"Alternative lookup for: {msg.item}")
    ctx.logger.info(f"Demo catalog: {msg.alternatives}")

    if price_received and alternative_received:
        ctx.logger.info("Both agents have responded.")


if __name__ == "__main__":
    orchestrator.run()

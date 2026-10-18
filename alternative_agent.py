
from uagents import Agent, Context, Model


class AlternativeRequest(Model):
    item: str


class AlternativeResponse(Model):
    item: str
    alternatives: str


alternative_agent = Agent(
    name="alternative_agent",
    seed="medagent_alternative_agent_demo_seed_2026",
    port=8002,
    endpoint=["http://127.0.0.1:8002/submit"]
)


alternatives_data = {
    "notebook": "Spiral notebook; Ruled notebook",
    "pen": "Blue ballpoint pen; Gel pen",
    "sketchbook": "Drawing pad; Plain-paper notebook"
}


@alternative_agent.on_query(
    model=AlternativeRequest,
    replies={AlternativeResponse}
)
async def handle_request(
    ctx: Context,
    sender: str,
    msg: AlternativeRequest
):
    name = msg.item.strip().lower()

    alternatives = alternatives_data.get(
        name,
        "No matching entry in the demo catalog"
    )

    ctx.logger.info(f"Received alternative request for: {name}")

    await ctx.send(
        sender,
        AlternativeResponse(
            item=name,
            alternatives=alternatives
        )
    )


if __name__ == "__main__":
    alternative_agent.run()

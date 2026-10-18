import asyncio
import json

from uagents import Model
from uagents.query import query
from uagents.envelope import Envelope
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel


app = FastAPI(title="CampusCart")


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


async def ask_agent(address: str, message: Model):
    response = await query(
        destination=address,
        message=message,
        timeout=15
    )

    if not isinstance(response, Envelope):
        raise RuntimeError(f"Agent did not return a response: {response}")

    return json.loads(response.decode_payload())



# Fictional demonstration data
catalog = {
    "notebook": {
        "prices": {
            "Store A": 60,
            "Store B": 55,
            "Store C": 65
        },
        "alternatives": [
            "Spiral notebook",
            "Ruled notebook"
        ]
    },
    "pen": {
        "prices": {
            "Store A": 10,
            "Store B": 8,
            "Store C": 12
        },
        "alternatives": [
            "Blue ballpoint pen",
            "Gel pen"
        ]
    },
    "sketchbook": {
        "prices": {
            "Store A": 120,
            "Store B": 110,
            "Store C": 135
        },
        "alternatives": [
            "Drawing pad",
            "Plain-paper notebook"
        ]
    }
}


class SearchRequest(BaseModel):
    item: str


@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport"
              content="width=device-width, initial-scale=1.0">

        <title>CampusCart</title>

        <style>
            * {
                box-sizing: border-box;
            }

            body {
                margin: 0;
                font-family: Arial, sans-serif;
                background: #f3f5fb;
                color: #20243a;
            }

            header {
                background: #282c55;
                color: white;
                padding: 24px;
                text-align: center;
            }

            header h1 {
                margin: 0 0 8px;
            }

            main {
                max-width: 650px;
                margin: 35px auto;
                padding: 20px;
            }

            .card {
                background: white;
                padding: 25px;
                border-radius: 16px;
                box-shadow: 0 5px 20px #20243a12;
                margin-bottom: 20px;
            }

            label {
                display: block;
                margin-bottom: 10px;
                font-weight: bold;
            }

            select, button {
                width: 100%;
                padding: 13px;
                border-radius: 8px;
                font-size: 16px;
            }

            select {
                border: 1px solid #cbd0df;
                margin-bottom: 14px;
                background: white;
            }

            button {
                border: none;
                background: #5558d9;
                color: white;
                cursor: pointer;
                font-weight: bold;
            }

            button:disabled {
                opacity: 0.6;
                cursor: wait;
            }

            .price {
                display: flex;
                justify-content: space-between;
                padding: 12px 0;
                border-bottom: 1px solid #eee;
            }

            .cheapest {
                color: #18794e;
                font-weight: bold;
            }

            .note {
                color: #62677b;
                font-size: 13px;
                line-height: 1.5;
            }

            #results {
                display: none;
            }

            #status {
                margin-top: 14px;
            }
        </style>
    </head>

    <body>
        <header>
            <h1>CampusCart</h1>
            <p>Compare campus stationery prices</p>
        </header>

        <main>
            <section class="card">
                <h2>Find an item</h2>
                <p>Select a product to explore the demo catalog.</p>

                <form id="searchForm">
                    <label for="item">Stationery item</label>

                    <select id="item">
                        <option value="notebook">Notebook</option>
                        <option value="pen">Pen</option>
                        <option value="sketchbook">Sketchbook</option>
                    </select>

                    <button id="searchButton" type="submit">
                        Compare prices
                    </button>
                </form>

                <p id="status" role="status"></p>
            </section>

            <section class="card" id="results">
                <h2 id="resultTitle">Results</h2>
                <div id="prices"></div>

                <h3>Similar items</h3>
                <ul id="alternatives"></ul>

                <p class="note">
                    All prices and product suggestions are fictional
                    demonstration data, not live store listings.
                </p>
            </section>
        </main>

        <script>
            const form = document.getElementById("searchForm");
            const button = document.getElementById("searchButton");
            const status = document.getElementById("status");
            const results = document.getElementById("results");

            form.addEventListener("submit", async (event) => {
                event.preventDefault();

                button.disabled = true;
                status.textContent = "Searching the demo catalog...";
                results.style.display = "none";

                try {
                    const response = await fetch("/api/search", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            item: document.getElementById("item").value
                        })
                    });

                    const data = await response.json();

                    if (!response.ok) {
                        throw new Error(data.detail || "Search failed");
                    }

                    document.getElementById("resultTitle").textContent =
                        data.item.charAt(0).toUpperCase()
                        + data.item.slice(1) + " results";

                    const prices = document.getElementById("prices");
                    prices.replaceChildren();

                    data.prices.forEach((entry) => {
                        const row = document.createElement("div");
                        row.className = "price";

                        const store = document.createElement("span");
                        store.textContent = entry.store;

                        const amount = document.createElement("span");
                        amount.textContent = "Rs " + entry.price;

                        if (entry.store === data.cheapest.store) {
                            row.classList.add("cheapest");
                            amount.textContent += " — Cheapest";
                        }

                        row.append(store, amount);
                        prices.appendChild(row);
                    });

                    const list = document.getElementById("alternatives");
                    list.replaceChildren();

                    data.alternatives.forEach((item) => {
                        const li = document.createElement("li");
                        li.textContent = item;
                        list.appendChild(li);
                    });

                    results.style.display = "block";
                    status.textContent = "Results loaded!";
                } catch (error) {
                    status.textContent = "Error: " + error.message;
                } finally {
                    button.disabled = false;
                }
            });
        </script>
    </body>
    </html>
    """



@app.post("/api/search")
async def search(request: SearchRequest):
    item = request.item.strip().lower()

    allowed_items = {"notebook", "pen", "sketchbook"}

    if item not in allowed_items:
        raise HTTPException(
            status_code=404,
            detail="Item not found in the demo catalog"
        )

    try:
        price_result, alternative_result = await asyncio.gather(
            ask_agent(
                PRICE_AGENT_ADDRESS,
                PriceRequest(item=item)
            ),
            ask_agent(
                ALTERNATIVE_AGENT_ADDRESS,
                AlternativeRequest(item=item)
            )
        )

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Agent communication failed: {exc}"
        )

    prices_text = price_result.get("prices", "")

    prices = []

    for entry in prices_text.split(","):
        parts = entry.strip().split(": Rs ", 1)

        if len(parts) == 2:
            prices.append({
                "store": parts[0].strip(),
                "price": float(parts[1].strip())
            })

    if not prices:
        raise HTTPException(
            status_code=502,
            detail="Price agent returned no usable prices"
        )

    cheapest = min(prices, key=lambda entry: entry["price"])

    alternatives_text = alternative_result.get("alternatives", "")
    alternatives = [
        value.strip()
        for value in alternatives_text.split(";")
        if value.strip()
    ]

    return {
        "item": item,
        "prices": prices,
        "cheapest": cheapest,
        "alternatives": alternatives
    }


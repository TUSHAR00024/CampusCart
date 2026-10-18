# CampusCart 🛒

**A multi-agent AI demonstration built with Fetch.ai uAgents and FastAPI.**

CampusCart demonstrates how multiple specialized AI agents can collaborate to help users compare stationery prices and discover alternatives.

Instead of relying on a single component for everything, CampusCart uses two agents: one for price comparison and another for suggesting alternatives. A FastAPI backend coordinates their responses and presents the combined results through a simple web interface.

> **Note:** CampusCart is a demonstration project. It uses fictional sample stationery prices and predefined alternatives, not live store data.

## ✨ Features

- **Price Comparison:** Compare sample prices across three stores.
- **Alternative Suggestions:** Discover alternative stationery items.
- **Multi-Agent Architecture:** Use two specialized uAgents for separate tasks.
- **Concurrent Execution:** Run both agent requests concurrently using Python's `asyncio.gather()`.
- **Web Interface:** Search for stationery through a FastAPI-powered interface.

## 🏗️ Architecture

```text
              User
               |
               v
        CampusCart UI
               |
               v
        FastAPI Backend
               |
        +------+------+
        |             |
        v             v
   Price Agent   Alternative Agent
        |             |
        v             v
  Sample Prices   Sample Alternatives
        |             |
        +------+------+
               |
               v
       Combined Results
               |
               v
          User Interface
```

## 🛠️ Tech Stack

- **Python** — Application and agent logic
- **Fetch.ai uAgents** — Specialized AI-agent framework
- **FastAPI** — Backend API and web interface
- **Uvicorn** — ASGI server
- **asyncio** — Concurrent agent communication

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or a compatible Python version
- Git

### 1. Clone the repository

```bash
git clone https://github.com/TUSHAR00024/CampusCart.git
cd CampusCart
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

On Windows, use:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Start the agents

Open separate terminals in the project directory. Activate the virtual environment in each terminal if necessary.

**Terminal 1 — Price Agent**

```bash
python price_agent.py
```

**Terminal 2 — Alternative Agent**

```bash
python alternative_agent.py
```

### 5. Start the backend

**Terminal 3**

```bash
python -m uvicorn main:app --reload
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

The two agents must be running locally for agent communication to work.

## 📂 Project Structure

```text
CampusCart/
├── main.py
├── price_agent.py
├── alternative_agent.py
├── requirements.txt
├── .gitignore
└── README.md
```

- `main.py` — FastAPI backend, web interface, and agent orchestration.
- `price_agent.py` — Handles price comparison requests.
- `alternative_agent.py` — Handles alternative suggestion requests.
- `requirements.txt` — Lists Python dependencies.
- `.gitignore` — Specifies files Git should ignore.

## 🧠 What I Learned

Building CampusCart helped me explore multi-agent application design, asynchronous programming, API development, and the coordination of specialized agents through Fetch.ai uAgents.

It also demonstrated how multiple components can work together to provide a unified result through a simple web application.

## 🔮 Future Improvements

- Integrate real stationery product and pricing data.
- Deploy the application and agents for public access.
- Expand the product catalog and alternative recommendations.
- Improve error handling and agent communication.

## 📌 Project Links

- **GitHub Repository:** [TUSHAR00024/CampusCart](https://github.com/TUSHAR00024/CampusCart)

---

*CampusCart is an educational demonstration project built to explore autonomous AI agents and multi-agent collaboration.*
# CarDekho Assistant

AI-powered car buying advisor that helps confused buyers go from **"I don't know what to buy"** to **"I'm confident about my shortlist."**

> **Try it locally:** Please follow the quick start guide.

## What It Does

A single conversational AI agent that:
- Asks smart questions to understand your needs (budget, use case, priorities)
- Searches a curated dataset of 45+ Indian market cars
- Recommends a ranked shortlist with **"why this car for YOU"** reasoning
- Compares cars side-by-side on specs that matter to you

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python, FastAPI |
| **LLM** | OpenRouter (OpenAI-compatible, any model) |
| **Frontend** | React 18, TypeScript, Vite, Tailwind CSS |
| **Icons** | Lucide React |
| **Container** | Docker, Docker Compose |

## Architecture

```
┌────────────────────────────────────────────────┐
│                Docker Compose                  │
│                                                │
│  ┌──────────────┐       ┌───────────────────┐  │
│  │   Frontend    │       │     Backend       │  │
│  │  React + Vite │──────▶│     FastAPI       │  │
│  │  :5173        │ /api  │     :8000         │  │
│  └──────────────┘       │                   │  │
│                          │  ┌─────────────┐  │  │
│                          │  │ AI Agent    │  │  │
│                          │  │ (OpenRouter)│  │  │
│                          │  └──────┬──────┘  │  │
│                          │         │         │  │
│                          │  ┌──────▼──────┐  │  │
│                          │  │  Car Data   │  │  │
│                          │  │  (JSON)     │  │  │
│                          │  └─────────────┘  │  │
│                          └───────────────────┘  │
└────────────────────────────────────────────────┘
```

## Quick Start

### Prerequisites
- Docker & Docker Compose
- An [OpenRouter](https://openrouter.ai/) API key

### 1. Clone & configure

```bash
cd carDekhoAssistant
cp backend/.env.example backend/.env
```

Edit `backend/.env` and add your OpenRouter API key:

```env
OPENROUTER_API_KEY=sk-or-v1-your-key-here
OPENROUTER_MODEL=openai/gpt-4.1-mini
```

### 2. Run

```bash
docker-compose up --build
```

### 3. Open

- **App**: http://localhost:5173
- **API docs**: http://localhost:8000/docs
- **Health check**: http://localhost:8000/health

## API

### `POST /api/chat`

Send a conversation and get a response with optional structured car data.

**Request:**
```json
{
  "messages": [
    { "role": "user", "content": "I need a safe family SUV under 15 lakhs" }
  ]
}
```

**Response:**
```json
{
  "reply": "Here are my top picks for you...",
  "cars": [ { "id": "tata-nexon-xz-plus", "make": "Tata", ... } ],
  "comparison": null
}
```

## Agent Tools

The AI agent has access to three tools via OpenAI-compatible function calling:

| Tool | Purpose |
|------|---------|
| `search_cars` | Filter by budget, body type, fuel, transmission, safety rating, use case |
| `get_car_details` | Full specs, features, pros/cons, review for a specific car |
| `compare_cars` | Side-by-side comparison of 2-4 cars |

## Project Structure

```
carDekhoAssistant/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI app, CORS, /api/chat endpoint
│   │   ├── agent.py          # OpenRouter agent with tool calling loop
│   │   ├── car_data.py       # Search, compare, detail functions
│   │   ├── config.py         # Pydantic settings from .env
│   │   └── models.py         # Request/response schemas
│   ├── data/
│   │   └── cars.json         # 45 cars, Indian market
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env                  # Your API key (git-ignored)
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.tsx            # Main chat interface
│   │   ├── api.ts             # API client
│   │   ├── types.ts           # TypeScript interfaces
│   │   ├── components/
│   │   │   ├── CarCard.tsx        # Rich car result card
│   │   │   ├── ChatMessage.tsx    # Chat bubble with markdown
│   │   │   └── ComparisonTable.tsx # Side-by-side spec table
│   │   └── index.css          # Tailwind + custom styles
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
└── README.md
```

## Product Decisions

- **One agent, not a catalog** — the problem is too many choices, not too few. A guided conversation reduces cognitive load.
- **Opinionated recommendations** — the agent explains *why* each car fits, not just *what* matches.
- **No auth, no DB** — zero friction. Static JSON dataset is sufficient for MVP and keeps deployment simple.
- **Rich cards in chat** — car data is rendered as structured cards, not text dumps. Comparisons are tables, not paragraphs.
- **Indian market focus** — realistic data for the CarDekho context (prices in lakhs, NCAP ratings, real models).

## What Was Deliberately Cut

These were all considered and intentionally dropped to ship a tight MVP:

- **User accounts / auth** — adds zero value to the core "confused → confident" loop. A buyer doesn't need to log in to get a recommendation.
- **Full catalog browse / filter page** — that's the problem, not the solution. Showing 45 cars in a grid doesn't help a confused buyer.
- **Database** — static JSON is fast, deployable anywhere, and sufficient for the dataset size. A DB adds infra overhead with no user benefit at this stage.
- **Review submission / ratings CRUD** — we *consume* review data to inform recommendations, we don't need to *collect* it for the MVP.
- **Admin dashboard** — no content management needed when the dataset is static.
- **Multi-agent orchestration** — one agent with three tools covers search, detail, and compare. Adding a router agent or specialist agents adds latency and complexity for no user gain.
- **Streaming responses** — would improve perceived performance, but adds WebSocket complexity. Acceptable trade-off for MVP.
- **Saved searches / shortlist persistence** — nice-to-have, but requires auth and storage. The conversation itself is the shortlist for now.
- **Image/media for cars** — would make cards prettier but requires asset hosting. Text + specs are sufficient to make a decision.
- **Price comparison across dealers / on-road pricing** — real-time pricing requires external APIs and partnerships. Out of scope for a proof-of-concept.

## If I Had Another 4 Hours

### Multi-Agent Architecture
Move from a single agent to an orchestrated multi-agent system:
- **Router Agent** — understands user intent and delegates to the right specialist
- **Variant Agent** — deep knowledge of trim levels, variant-specific differences, and "which variant is the sweet spot"
- **Mileage Agent** — fuel cost calculations, real-world vs claimed mileage, TCO (total cost of ownership) analysis
- **Safety Agent** — NCAP deep-dives, ADAS feature explanations, crash test comparisons
- **Comparison Agent** — dedicated to structured head-to-head analysis with weighted scoring based on buyer priorities

This reduces hallucination risk (each agent has a narrow, focused context) and enables parallel tool calls.

### Intent-Based API Integration
Replace static JSON filtering with real API calls:
- Extract structured **intents** from the user query (budget, body type, fuel, use case) using the LLM
- Hit a live car data API (e.g., CarDekho's own API) with those intents as query parameters
- Eliminates manual filtering logic — the LLM becomes the intent parser, the API becomes the search engine
- Enables real-time pricing, availability, and dealer-level data

### Voice Support
- Add speech-to-text input (Web Speech API or Whisper) so buyers can talk naturally
- Text-to-speech for agent responses — makes it feel like talking to a knowledgeable friend
- Especially valuable for the Indian market where voice-first interaction is more natural for many buyers

### Other Additions
- **Streaming responses** via WebSocket for perceived speed
- **Session persistence** — save conversation and shortlist to resume later
- **EMI calculator** — inline loan/EMI estimates based on car price
- **On-road price estimation** — add RTO, insurance, and accessory cost estimates by city
- **Car images** — visual cards with actual car photos from a CDN
- **Analytics** — track which cars get recommended most, common budgets, drop-off points
- **Redis caching** — cache LLM responses for frequently asked queries (e.g., "best SUV under 15 lakhs") to reduce latency and API costs. Also useful for rate limiting, session storage, and caching car search results so repeated filters don't recompute

import json
import logging
from openai import OpenAI
from app.car_data import search_cars, get_car_details, compare_cars
from app.config import settings
from app.guardrail import moderate

logger = logging.getLogger(__name__)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.openrouter_api_key,
)

SYSTEM_PROMPT = """You are CarDekho Assistant — an expert car buying advisor for the Indian market.

Your goal: Help confused car buyers go from "I don't know what to buy" to "I'm confident about my shortlist."

BEHAVIOR:
1. Start by understanding the buyer. Ask 2-3 focused questions about:
   - Budget range (in lakhs)
   - Primary use case (city commute, highway, family, off-road, etc.)
   - Must-haves or priorities (safety, mileage, features, performance, space)
   - Any dealbreakers (no diesel, need automatic, etc.)

2. Once you understand their needs, use the search_cars tool to find matching cars.

3. Present a shortlist of 3-5 cars with clear "why this car for YOU" reasoning.

4. If they want to compare specific cars, use the compare_cars tool.

5. If they ask about a specific car, use the get_car_details tool.

PERSONALITY:
- Friendly but not salesy. You're a knowledgeable friend, not a dealer.
- Be opinionated — recommend boldly, explain why.
- Use simple language. Avoid jargon unless the buyer seems knowledgeable.
- Always explain trade-offs honestly (pros AND cons).
- Prices are ex-showroom in lakhs (₹). Always mention this.

SCOPE:
- You ONLY answer questions related to car buying, car comparisons, car features, car recommendations, and automotive topics.
- If a user asks anything unrelated to cars (e.g., general knowledge, coding, recipes, politics, weather, math, jokes, personal advice), politely decline and redirect:
  "I'm specialized in helping you find the right car. I can't help with that topic, but I'd love to help you find your perfect car! What are you looking for?"
- Do NOT engage with off-topic requests even if the user insists. Stay on mission.
- Exception: Basic greetings and pleasantries are fine — respond warmly and steer toward car buying.

IMPORTANT:
- Never make up car data. Only use data from the tools.
- If no cars match, say so honestly and suggest adjusting criteria.
- When presenting cars, always mention: name, price, key highlights, and why it fits their needs.
- Keep responses concise but informative. Use bullet points for clarity.
- For EV mileage, the mileage_kmpl field represents range in km, not kmpl.
"""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_cars",
            "description": "Search and filter cars based on buyer criteria. Returns a list of matching cars with full details.",
            "parameters": {
                "type": "object",
                "properties": {
                    "min_budget": {
                        "type": "number",
                        "description": "Minimum budget in lakhs (e.g., 8 for ₹8 lakh)",
                    },
                    "max_budget": {
                        "type": "number",
                        "description": "Maximum budget in lakhs (e.g., 15 for ₹15 lakh)",
                    },
                    "body_type": {
                        "type": "string",
                        "enum": ["Hatchback", "Sedan", "SUV", "MPV"],
                        "description": "Type of car body",
                    },
                    "fuel_type": {
                        "type": "string",
                        "enum": ["Petrol", "Diesel", "Electric", "Hybrid"],
                        "description": "Fuel type preference",
                    },
                    "transmission": {
                        "type": "string",
                        "enum": ["Manual", "Automatic", "DCT", "CVT", "DSG", "Torque Converter", "eCVT"],
                        "description": "Transmission preference",
                    },
                    "seating_capacity": {
                        "type": "integer",
                        "description": "Minimum seating capacity needed",
                    },
                    "min_safety_rating": {
                        "type": "integer",
                        "description": "Minimum NCAP safety rating (1-5)",
                    },
                    "use_case": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Use case tags like: city_commute, highway, family, safety_first, performance, budget, first_car, off_road, 7_seater, mileage, feature_lovers, premium_feel, ev_enthusiast, lifestyle",
                    },
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_car_details",
            "description": "Get complete details about a specific car including specs, features, pros, cons, and review summary.",
            "parameters": {
                "type": "object",
                "properties": {
                    "car_id": {
                        "type": "string",
                        "description": "The unique car ID (e.g., 'tata-nexon-xz-plus')",
                    },
                },
                "required": ["car_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "compare_cars",
            "description": "Compare 2-4 cars side-by-side on all key specifications, features, pros, and cons.",
            "parameters": {
                "type": "object",
                "properties": {
                    "car_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of car IDs to compare (e.g., ['tata-nexon-xz-plus', 'hyundai-creta-sx'])",
                    },
                },
                "required": ["car_ids"],
            },
        },
    },
]

TOOL_DISPATCH = {
    "search_cars": lambda args: search_cars(**args),
    "get_car_details": lambda args: get_car_details(**args),
    "compare_cars": lambda args: compare_cars(**args),
}


def _execute_tool(name: str, arguments: str) -> str:
    """Parse tool arguments and execute the corresponding function."""
    args = json.loads(arguments)
    handler = TOOL_DISPATCH.get(name)
    if not handler:
        return json.dumps({"error": f"Unknown tool: {name}"})
    result = handler(args)
    return json.dumps(result, default=str)


def chat(messages: list[dict]) -> dict:
    """
    Run a single chat turn with the agent.
    Handles tool calls in a loop until the model produces a final text response.
    Returns dict with 'reply' (str) and optionally 'cars' / 'comparison' data.
    """
    # Llama Guard: moderate the latest user message
    latest_user_msg = next(
        (m["content"] for m in reversed(messages) if m["role"] == "user"), None
    )
    if latest_user_msg:
        moderation = moderate(latest_user_msg)
        if not moderation["safe"]:
            logger.warning(f"Blocked unsafe input. Category: {moderation['category']}")
            return {
                "reply": "I'm sorry, I can't respond to that. I'm here to help you find the right car. How can I assist with your car search?",
                "cars": None,
                "comparison": None,
            }

    openai_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in messages:
        openai_messages.append({"role": msg["role"], "content": msg["content"]})

    collected_data = {"cars": None, "comparison": None}
    max_iterations = 5

    for _ in range(max_iterations):
        response = client.chat.completions.create(
            model=settings.openrouter_model,
            messages=openai_messages,
            tools=TOOLS,
            tool_choice="auto",
        )

        choice = response.choices[0]

        if choice.finish_reason == "tool_calls" or choice.message.tool_calls:
            openai_messages.append(choice.message)

            for tool_call in choice.message.tool_calls:
                tool_name = tool_call.function.name
                tool_result = _execute_tool(tool_name, tool_call.function.arguments)

                # Track structured data for the frontend
                parsed = json.loads(tool_result)
                if tool_name == "search_cars" and isinstance(parsed, list):
                    collected_data["cars"] = parsed
                elif tool_name == "get_car_details" and isinstance(parsed, dict):
                    collected_data["cars"] = [parsed] if "error" not in parsed else None
                elif tool_name == "compare_cars" and isinstance(parsed, dict):
                    if "error" not in parsed:
                        collected_data["comparison"] = parsed

                openai_messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result,
                })
        else:
            return {
                "reply": choice.message.content or "",
                **collected_data,
            }

    return {
        "reply": "I'm having trouble processing that. Could you try rephrasing?",
        **collected_data,
    }

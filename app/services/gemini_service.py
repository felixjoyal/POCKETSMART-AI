import json
from pathlib import Path
from typing import Any
from google import genai
from google.genai import types
from pydantic import ValidationError
from ..config import settings
from ..schemas import HomeRequest, JewelryRequest, PartyRequest, RecommendationResponse

def _client() -> genai.Client:
    if not settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured. Set it in .env or enable DEMO_MODE=true.")
    return genai.Client(api_key=settings.gemini_api_key)

def _generate(prompt: str, image_path: str | None = None) -> RecommendationResponse:
    client = _client()
    contents: list[Any] = [prompt]
    if image_path:
        path = Path(image_path)
        mime_type = {
            ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
            ".png": "image/png", ".webp": "image/webp"
        }.get(path.suffix.lower(), "application/octet-stream")
        contents = [types.Part.from_bytes(data=path.read_bytes(), mime_type=mime_type), prompt]

    config = types.GenerateContentConfig(
        temperature=0.4,
        max_output_tokens=6000,
        response_mime_type="application/json",
        response_schema=RecommendationResponse.model_json_schema(),
    )
    response = client.models.generate_content(
        model=settings.gemini_model, contents=contents, config=config
    )
    raw = getattr(response, "text", None)
    if not raw:
        raise RuntimeError("Gemini returned an empty response.")
    try:
        return RecommendationResponse.model_validate_json(raw)
    except (ValidationError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Gemini returned invalid structured data: {exc}") from exc

def home_recommendations(data: HomeRequest) -> RecommendationResponse:
    prompt = (
        "You are PocketSmart AI, a budget planning assistant for Indian users.\n"
        f"Create a realistic HOME INTERIOR plan. Budget INR {data.budget}. "
        f"Rooms: {', '.join(data.rooms) if data.rooms else 'Not specified'}. "
        f"Lights: {data.lights}. Fans: {data.fans}. Furniture count: {data.furniture_items}. "
        f"Style: {data.style}. Notes: {data.notes or 'None'}.\n"
        "Return JSON matching the schema. Keep estimated_total <= budget. Use INR. "
        "Use Amazon, Flipkart or IKEA where appropriate. search_query must be useful. "
        "Do not claim live stock, exact current prices, ratings, discounts or verified availability. "
        "estimated_price is only an estimate. Make remaining_budget mathematically consistent."
    )
    return _generate(prompt)

def party_recommendations(data: PartyRequest) -> RecommendationResponse:
    prompt = (
        "You are PocketSmart AI, a budget planning assistant for Indian events.\n"
        f"Create a practical PARTY plan. Budget INR {data.budget}. Guests: {data.guests}. "
        f"Event: {data.event_type}. Venue: {data.venue_type}. "
        f"Catering: {data.catering}. Decoration: {data.decoration}. Entertainment: {data.entertainment}. "
        f"Notes: {data.notes or 'None'}.\n"
        "Return JSON matching the schema. Keep estimated_total <= budget. Use INR. "
        "Allocate across selected venue/catering/decoration/entertainment categories. "
        "Use Swiggy, Zomato or OYO where appropriate. Do not claim live vendor availability, "
        "exact current prices, ratings, discounts or reservations. Make remaining_budget consistent."
    )
    return _generate(prompt)

def jewelry_recommendations(data: JewelryRequest, image_path: str | None = None) -> RecommendationResponse:
    prompt = (
        "You are PocketSmart AI, a jewelry styling and budget planning assistant.\n"
        f"Create a jewelry plan. Budget INR {data.budget}. Occasion: {data.occasion}. "
        f"Style: {data.style}. Preferences: {data.preferences or 'None'}.\n"
        "If an outfit image is attached, analyze only visible styling information such as dominant "
        "colors, neckline/shape cues and formality. Do not identify the person or infer sensitive attributes. "
        "Return JSON matching the schema. Keep estimated_total <= budget. Use Amazon or Flipkart. "
        "Do not claim live availability, exact current prices, ratings or authenticity. "
        "Make remaining_budget mathematically consistent."
    )
    return _generate(prompt, image_path)

from ..config import settings
from ..schemas import HomeRequest, JewelryRequest, PartyRequest, RecommendationResponse
from .gemini_service import home_recommendations, jewelry_recommendations, party_recommendations

def _remaining(result: RecommendationResponse) -> RecommendationResponse:
    total = sum(i.estimated_price * i.quantity for s in result.sections for i in s.items)
    if total > result.budget and total > 0:
        factor = result.budget / total
        for section in result.sections:
            section.allocation = round(section.allocation * factor, 2)
            for item in section.items:
                item.estimated_price = round(item.estimated_price * factor, 2)
        total = sum(i.estimated_price * i.quantity for s in result.sections for i in s.items)
    result.estimated_total = round(total, 2)
    result.remaining_budget = max(round(result.budget - result.estimated_total, 2), 0)
    return result

def _demo_home(data: HomeRequest):
    b = float(data.budget)
    sections = [
        {"category": "Lighting", "allocation": b*.12, "items": [{
            "name": "Warm-white LED ceiling light", "category": "Lighting",
            "description": "Energy-efficient warm lighting.",
            "estimated_price": max(round(b*.12/max(data.lights or 2,1),2),900),
            "quantity": max(data.lights,1), "platform": "Amazon",
            "search_query": "warm white LED ceiling light",
            "reason": "Keeps lighting practical and within the plan."
        }]},
        {"category": "Fans", "allocation": b*.15, "items": [{
            "name": "Energy-efficient ceiling fan", "category": "Fans",
            "description": "Standard energy-efficient ceiling fan.",
            "estimated_price": max(round(b*.15/max(data.fans or 2,1),2),1800),
            "quantity": max(data.fans,1), "platform": "Amazon",
            "search_query": "energy efficient ceiling fan",
            "reason": "Provides a useful utility allocation."
        }]},
        {"category": "Furniture & Decor", "allocation": b*.40, "items": [
            {"name": "Compact modern furniture", "category": "Furniture",
             "description": f"Space-conscious furniture suited to {data.style.lower()} style.",
             "estimated_price": round(b*.22,2), "quantity": 1, "platform": "IKEA",
             "search_query": f"{data.style} compact furniture",
             "reason": "Prioritizes useful furniture."},
            {"name": "Minimal wall decor", "category": "Decor",
             "description": "Simple wall decor.",
             "estimated_price": round(b*.18,2), "quantity": 1, "platform": "Amazon",
             "search_query": f"{data.style} wall decor",
             "reason": "Adds style without consuming the whole budget."}
        ]}
    ]
    return _remaining(RecommendationResponse(
        planner_type="home", title="Demo Home Budget Plan", budget=b,
        estimated_total=0, remaining_budget=b,
        summary="Local demo output. Set DEMO_MODE=false and a Gemini API key for AI-generated output.",
        sections=sections,
        tips=["Measure rooms before buying large furniture.",
              "Compare dimensions and warranty details.",
              "Keep a reserve for delivery and installation."]
    ))

def _demo_party(data: PartyRequest):
    b = float(data.budget)
    sections = []
    if data.catering:
        sections.append({"category":"Catering","allocation":b*.45,"items":[{
            "name":"Catering package","category":"Food",
            "description":f"Planning estimate for {data.guests} guests.",
            "estimated_price":round(b*.45,2),"quantity":1,"platform":"Zomato",
            "search_query":f"{data.event_type} catering for {data.guests} guests",
            "reason":"Food is usually a major event expense."
        }]})
    if data.decoration:
        sections.append({"category":"Decoration","allocation":b*.20,"items":[{
            "name":"Basic event decoration","category":"Decoration",
            "description":"Simple decoration package.",
            "estimated_price":round(b*.20,2),"quantity":1,"platform":"Amazon",
            "search_query":f"{data.event_type} party decoration",
            "reason":"Keeps decoration controlled."
        }]})
    if data.entertainment:
        sections.append({"category":"Entertainment","allocation":b*.15,"items":[{
            "name":"Basic entertainment setup","category":"Entertainment",
            "description":"Budget allowance for music or entertainment.",
            "estimated_price":round(b*.15,2),"quantity":1,"platform":"Amazon",
            "search_query":f"{data.event_type} party speaker entertainment",
            "reason":"Provides a controlled entertainment allowance."
        }]})
    sections.append({"category":"Venue","allocation":b*.20,"items":[{
        "name":"Venue search allowance","category":"Venue",
        "description":f"Planning allowance for an {data.venue_type.lower()} event.",
        "estimated_price":round(b*.20,2),"quantity":1,"platform":"OYO",
        "search_query":f"{data.event_type} event venue",
        "reason":"Keeps venue costs visible separately."
    }]})
    return _remaining(RecommendationResponse(
        planner_type="party", title="Demo Party Budget Plan", budget=b,
        estimated_total=0, remaining_budget=b,
        summary="Local demo output. Use Gemini mode for personalized planning.",
        sections=sections,
        tips=["Confirm venue capacity.", "Ask whether taxes and service charges are included.",
              "Keep a contingency amount."]
    ))

def _demo_jewelry(data: JewelryRequest):
    b = float(data.budget)
    sections = [{"category":"Jewelry","allocation":b*.90,"items":[
        {"name":f"{data.style} necklace set","category":"Necklace",
         "description":f"Planning suggestion for a {data.occasion.lower()} occasion.",
         "estimated_price":round(b*.55,2),"quantity":1,"platform":"Amazon",
         "search_query":f"{data.style} necklace set {data.occasion}",
         "reason":"A coordinated necklace can anchor the look."},
        {"name":f"{data.style} earrings","category":"Earrings",
         "description":"Matching earrings for a coordinated appearance.",
         "estimated_price":round(b*.35,2),"quantity":1,"platform":"Flipkart",
         "search_query":f"{data.style} earrings {data.occasion}",
         "reason":"Adds a second coordinated jewelry piece."}
    ]}]
    return _remaining(RecommendationResponse(
        planner_type="jewelry", title="Demo Jewelry Budget Plan", budget=b,
        estimated_total=0, remaining_budget=b,
        summary="Local demo output. Gemini mode can use an outfit image for color/style matching.",
        sections=sections,
        tips=["Check material, dimensions and return policy.",
              "Verify precious-jewelry certification independently.",
              "Treat online prices as changeable estimates."]
    ))

def generate_home(data): return _demo_home(data) if settings.demo_mode else home_recommendations(data)
def generate_party(data): return _demo_party(data) if settings.demo_mode else party_recommendations(data)
def generate_jewelry(data, image_path=None):
    return _demo_jewelry(data) if settings.demo_mode else jewelry_recommendations(data, image_path=image_path)

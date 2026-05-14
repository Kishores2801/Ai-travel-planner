from src.models import TravelPlanRequests
import json
import re

def is_budget_realistic(city: str, daily_budget: float, trip_type: str, accommodation: str) -> bool:
    """
    Calls LLM to verify if a budget is realistic for a specific city.
    Returns True if realistic, False if not.
    """
    
    # 1. Construct the prompt
    # Note: Double curly braces {{ }} are used for literal JSON in f-strings
    prompt = f"""
    Act as a travel cost expert in 2026.
    Destination: {city}
    Daily Budget: ${daily_budget}
    Trip Type: {trip_type}
    Accommodation: {accommodation}

    Is this realistic for food, stay, and local transport?
    Respond ONLY in JSON format: {{"is_realistic": boolean, "reason": "string"}}
    """

    try:
        # 2. Call your LLM here (Using your specific LLM client)
        # response = llm.generate(prompt) 
        
        # MOCK RESPONSE for demonstration:
        raw_output = '{"is_realistic": false, "reason": "Average hotels in Paris are $120+"}'
        
        # 3. Clean and Parse JSON
        # Removes Markdown code blocks if the LLM includes them
        clean_json = re.sub(r"```json|```", "", raw_output).strip()
        data = json.loads(clean_json) # the clean Json will be reused for making sure that cost on API doesn't rise
        
        return data.get("is_realistic", True) # Default to True if key is missing
        
    except (json.JSONDecodeError, Exception):
        # If the LLM fails, we default to True so we don't block the user
        return True
# Building Travel Itinerary
def build_itinerary(request: TravelPlanRequests) -> str:

    """
        We have to include these
         - Destination
         - Days - No of Days that you are willing Spend
         - Month - Planned Month
         - budget_range - Budget they are willing to spend
         - people_count - Number of people in trips
         - trip type -  what kind of trips
         - interests - Experiences that they are want to tryout
         - accommodation_type - What is the accommodation
         - Dietary restrictions - The Dietary Restriction like lactose intolerant, etc
         - near_city_interest - asking a Question to user that are they interested to visit other places near by.

    
    
    """


    prompt = f"""
You are a practical travel planner & have experience in building itinerary for various kind of group in different budget from luxury to bootstrapped you are flexible. Create a realistic, budget-aware itinerary using the user's trip details.

Trip Details:
- Destination: {request.destination}
- Duration: {request.days} days, excluding travel days
- Month: {request.months}
- Budget: {request.budget_range}
- People: {request.people_count}
- Trip Type: {request.trip_type}
- Interests: {request.interests or "Not specified"}
- Accommodation: {request.accommodation_type}
- Dietary Restrictions: {request.dietary_restrictions or "None"}
- Nearby City Interest: {request.near_city_interest}

Rules:
- Match the plan to the trip type, interests, group size, budget, and accommodation.
- Keep the itinerary realistic. Avoid rushed schedules and consider travel time.
- Include sightseeing, culture, food, local transport, leisure, and hidden gems where useful.
- Respect dietary restrictions and mention food warnings only when relevant.
- If the budget seems unrealistic, say so briefly and suggest a more realistic range.
- Give cost estimates in USD and local currency.
- Clearly say whether costs are per person or for the full group.
- If nearby city interest is yes, include only one realistic same-country day trip.
- If an interest is not available in the destination, suggest the nearest realistic alternative.
- Mention visa or entry-cost concerns only when relevant.
- Keep climate, etiquette, and scam notes short, practical, and destination-specific.
- Include 2 to 4 reliable links only if confident. Do not invent links.
- If information is uncertain, say “information unavailable” instead of guessing.
- Don't invent numbers or facts which are not true.

Itinerary Format:
- If trip is 5 days or fewer: use Day 1, Day 2, etc. with Morning, Afternoon, Evening, and Approx. Daily Cost.
- If trip is more than 5 days: group days into maximum 5 blocks and give overall activity suggestions only. Do not use Morning, Afternoon, Evening sections.
- keep the plan more realistic make sure that minimal travel from point a to point b within given time.


Output Format:
# Trip Summary
# Itinerary
# Food Suggestions
# Areas to Visit and Why
# Climate and Things to Know
# Estimated Cost Breakdown
Use a table with: Category, USD Estimate, Local Currency Estimate, Per Person or Group, Notes.
# Conclusion

Keep the response between 700 and 900 words. 
For trips of 5 days or fewer, include day-by-day details.
For trips longer than 5 days, group days into a maximum of 5 blocks and summarize the main activities.
Prioritize itinerary quality, realistic logistics, and cost breakdown over long explanations.
highlight area where they can save cost too, like budget friendly options are available as suggestions.
"""
    return prompt.strip()
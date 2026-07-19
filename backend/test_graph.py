from langchain_core.messages import HumanMessage

from app.graph.builder import travel_graph


result = travel_graph.invoke(
    {
        "messages": [
            HumanMessage(content="Plan a trip to Japan")
        ],
        "user_request": "Plan a trip to Japan",
        "destination": None,
        "days": None,
        "budget": None,
        "itinerary": None,
        "final_response": None,
    }
)

print(result)